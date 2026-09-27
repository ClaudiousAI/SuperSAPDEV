"""Offline smoke probe of installed resources, schemas, and stable serialization."""

import hashlib
import json
from importlib.resources import files
from pathlib import Path
from typing import cast

from jsonschema import Draft202012Validator

from supersap.contracts import CliFailure, EvidenceClass, ExitCode, SmokeReport

MAX_FIXTURE_BYTES = 65_536


def canonical_json(value: object) -> str:
    """Stable UTF-8 JSON, independent of filesystem paths, clocks, and key order."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise ValueError("Non-finite JSON number")


def run_smoke(fixture: Path | None = None) -> SmokeReport:
    """Validate synthetic data only; never fetch, execute, promote, or publish it."""
    if fixture is None:
        raw = files("supersap").joinpath("fixtures/smoke.json").read_bytes()
    else:
        try:
            with fixture.open("rb") as stream:
                raw = stream.read(MAX_FIXTURE_BYTES + 1)
        except OSError:
            raise CliFailure(
                ExitCode.INVALID_INPUT,
                "Cannot read smoke fixture.",
                "Pass --fixture with a readable local JSON file.",
            ) from None
    if len(raw) > MAX_FIXTURE_BYTES:
        raise CliFailure(
            ExitCode.INVALID_INPUT,
            "Smoke fixture exceeds 65536 bytes.",
            "Use a smaller synthetic fixture.",
        )
    try:
        payload: object = json.loads(
            raw.decode("utf-8-sig"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (ValueError, UnicodeError, RecursionError):
        raise CliFailure(
            ExitCode.INVALID_INPUT,
            "Smoke fixture is not valid UTF-8 JSON.",
            "Use one JSON object with unique keys and finite values.",
        ) from None

    schema = json.loads(files("supersap").joinpath("schemas/smoke.schema.json").read_text("utf-8"))
    Draft202012Validator.check_schema(schema)
    if not Draft202012Validator(schema).is_valid(payload):
        raise CliFailure(
            ExitCode.INVALID_INPUT,
            "Smoke fixture does not match schema 1.0.0.",
            "Use the bundled smoke fixture contract; evidence_class must be MOCK.",
        )
    normalized = canonical_json(cast(dict[str, object], payload)).encode("utf-8")
    return SmokeReport(
        schema_version="1.0.0",
        status="ok",
        evidence_class=EvidenceClass.MOCK.value,
        fixture_sha256=hashlib.sha256(normalized).hexdigest(),
        domains_in_scope=[f"D{number:02d}" for number in range(1, 16)],
        hosts_in_scope=["claude", "codex", "opencode", "deepseek"],
    )
