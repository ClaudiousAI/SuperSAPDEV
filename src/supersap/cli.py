"""CLI foundation with stable exit codes and machine-readable diagnostics."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Never

from supersap import __version__
from supersap.contracts import CliFailure, ExitCode
from supersap.smoke import canonical_json, run_smoke


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> Never:
        # argparse's message may contain sensitive user-supplied argument values.
        raise CliFailure(
            ExitCode.INVALID_INPUT,
            "Invalid command or arguments.",
            "Run supersap --help or supersap smoke --help for supported options.",
        )


def _parser() -> Parser:
    parser = Parser(description="Super SAP Dev tooling (TASK-001 workspace).", allow_abbrev=False)
    parser.add_argument("--version", action="version", version=f"supersap {__version__}")
    parser.add_argument(
        "--json", action="store_true", help="emit structured JSON results and errors"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    smoke = commands.add_parser(
        "smoke",
        help="validate a synthetic fixture offline; produces MOCK evidence",
        allow_abbrev=False,
    )
    smoke.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
    smoke.add_argument("--fixture", type=Path, help="local JSON fixture (maximum 64 KiB)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    json_output = "--json" in args
    try:
        options = _parser().parse_args(args)
        report = run_smoke(options.fixture)
        if options.json:
            print(canonical_json(report))
        else:
            print(f"MOCK smoke passed: {report['fixture_sha256']}")
            print("Scope: 15 SAP domains; Claude Code, Codex, OpenCode, DeepSeek Harness.")
            print("Synthetic workspace check only; domain and host conformance remain pending.")
        return ExitCode.SUCCESS
    except CliFailure as error:
        failure = error
    except Exception:
        failure = CliFailure(
            ExitCode.INTERNAL_ERROR,
            "Internal workspace check failed.",
            "Reinstall from uv.lock and retry; report the command and versions if it persists.",
        )
    if json_output:
        print(
            canonical_json(
                {
                    "status": "error",
                    "code": failure.code.value,
                    "message": failure.message,
                    "recovery": failure.recovery,
                }
            ),
            file=sys.stderr,
        )
    else:
        print(f"Error: {failure.message} {failure.recovery}", file=sys.stderr)
    return failure.code
