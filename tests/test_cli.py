"""STATIC/MOCK CLI contract tests, including the actual installed entry points."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from supersap import __version__
from supersap.cli import main
from supersap.contracts import CliFailure, ExitCode


@pytest.mark.parametrize("args", [["--json", "smoke"], ["smoke", "--json"]])
def test_json_success(args: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    assert main(args) == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == Path("tests/fixtures/smoke.expected.json").read_text("utf-8")


def test_human_output_states_limitations(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["smoke"]) == 0
    assert "conformance remain pending" in capsys.readouterr().out


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["publish"],
        ["smoke", "--fixture"],
        ["smoke", "--secret=private-token"],
        ["smoke", "--fi", "private-token"],
        ["--j", "smoke"],
    ],
)
def test_bad_arguments_are_redacted_json(
    args: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["--json", *args]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "private-token" not in captured.err
    assert json.loads(captured.err)["recovery"]


@pytest.mark.parametrize("code", [ExitCode.POLICY_GATE, ExitCode.TRANSIENT_FAILURE])
def test_typed_failures_preserve_exit_codes(
    code: ExitCode, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail(fixture: Path | None) -> None:
        raise CliFailure(code, "Operation blocked.", "Review the local configuration.")

    monkeypatch.setattr("supersap.cli.run_smoke", fail)
    assert main(["smoke", "--json"]) == code
    assert json.loads(capsys.readouterr().err)["code"] == code


def test_internal_errors_do_not_leak_payloads(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail(fixture: Path | None) -> None:
        raise RuntimeError("private-token customer-code")

    monkeypatch.setattr("supersap.cli.run_smoke", fail)
    assert main(["smoke", "--json"]) == 5
    captured = capsys.readouterr()
    assert "private-token" not in captured.err
    assert "customer-code" not in captured.err
    assert json.loads(captured.err)["code"] == 5


@pytest.mark.parametrize("flag", ["--help", "--version"])
def test_help_and_version(flag: str, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as caught:
        main([flag])
    assert caught.value.code == 0
    output = capsys.readouterr().out
    assert "smoke" in output if flag == "--help" else __version__ in output


def test_entrypoints_work_outside_repository(tmp_path: Path) -> None:
    executable = Path(sys.executable).parent / (
        "supersap.exe" if sys.platform == "win32" else "supersap"
    )
    module = subprocess.run(
        [sys.executable, "-m", "supersap", "smoke", "--json"],
        cwd=tmp_path,
        capture_output=True,
        check=True,
        text=True,
    )
    console = subprocess.run(
        [str(executable), "--json", "smoke"],
        cwd=tmp_path,
        capture_output=True,
        check=True,
        text=True,
    )
    assert module.stdout == console.stdout
    assert module.stderr == console.stderr == ""
    assert json.loads(module.stdout)["evidence_class"] == "MOCK"
