"""MOCK evidence: synthetic fixture validation, never SAP runtime validation."""

import json
import os
import socket
import subprocess
from importlib.resources import files
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from supersap.contracts import CliFailure, ExitCode
from supersap.smoke import MAX_FIXTURE_BYTES, canonical_json, run_smoke


def test_bundled_schema_and_golden_report(monkeypatch: pytest.MonkeyPatch) -> None:
    def no_network(*args: object, **kwargs: object) -> None:
        pytest.fail("Offline smoke attempted network access")

    monkeypatch.setattr(socket, "socket", no_network)
    schema = json.loads(files("supersap").joinpath("schemas/smoke.schema.json").read_text("utf-8"))
    Draft202012Validator.check_schema(schema)
    expected = Path("tests/fixtures/smoke.expected.json").read_text("utf-8").strip()
    assert canonical_json(run_smoke()) == expected


def test_equivalent_json_has_same_hash_across_encodings_and_paths(tmp_path: Path) -> None:
    fixture = tmp_path / "SAP fixture space café.json"
    payload = json.loads(files("supersap").joinpath("fixtures/smoke.json").read_text("utf-8"))
    reordered = dict(reversed(list(payload.items())))
    fixture.write_bytes(json.dumps(reordered, indent=4).replace("\n", "\r\n").encode("utf-8-sig"))
    assert run_smoke(fixture) == run_smoke()


@pytest.mark.parametrize(
    "raw",
    [
        b"{}",
        b"[]",
        b"null",
        b"{",
        b"\xff",
        b'{"x":NaN}',
        b'{"x":Infinity}',
        b'{"x":1,"x":2}',
        b"[" * 2000,
        b" " * (MAX_FIXTURE_BYTES + 1),
    ],
    ids=[
        "empty",
        "array",
        "null",
        "syntax",
        "encoding",
        "nan",
        "infinity",
        "duplicate",
        "deep",
        "oversized",
    ],
)
def test_rejects_invalid_or_oversized_input(tmp_path: Path, raw: bytes) -> None:
    fixture = tmp_path / "invalid.json"
    fixture.write_bytes(raw)
    with pytest.raises(CliFailure) as caught:
        run_smoke(fixture)
    assert caught.value.code == ExitCode.INVALID_INPUT


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("evidence_class", "LIVE"),
        ("evidence_class", "STATIC"),
        ("schema_version", "2.0.0"),
        ("message", ""),
        ("message", "x" * 257),
        ("approved", True),
        ("message", 42),
    ],
)
def test_rejects_mislabeled_evidence_and_unknown_contracts(
    tmp_path: Path, field: str, value: object
) -> None:
    payload = json.loads(files("supersap").joinpath("fixtures/smoke.json").read_text("utf-8"))
    payload[field] = value
    fixture = tmp_path / "invalid.json"
    fixture.write_text(json.dumps(payload), "utf-8")
    with pytest.raises(CliFailure):
        run_smoke(fixture)


def test_untrusted_instructions_remain_data(monkeypatch: pytest.MonkeyPatch) -> None:
    def no_execution(*args: object, **kwargs: object) -> None:
        pytest.fail("Untrusted fixture attempted execution or network access")

    monkeypatch.setattr(subprocess, "Popen", no_execution)
    monkeypatch.setattr(os, "system", no_execution)
    monkeypatch.setattr(socket, "socket", no_execution)
    fixture = Path("tests/fixtures/untrusted.json")
    assert run_smoke(fixture)["evidence_class"] == "MOCK"


@pytest.mark.parametrize("directory", [False, True])
def test_unreadable_input_is_actionable_and_redacted(tmp_path: Path, directory: bool) -> None:
    path = tmp_path if directory else tmp_path / "private-secret-file.json"
    with pytest.raises(CliFailure) as caught:
        run_smoke(path)
    assert caught.value.code == ExitCode.INVALID_INPUT
    assert str(path) not in str(caught.value)
    assert "--fixture" in caught.value.recovery
