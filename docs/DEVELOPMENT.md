# Workspace development — TASK-001

See [CI/CD operations](CI_CD.md) for GitHub triggers, retained evidence and manual
draft delivery. The matrix now lives in the reusable `checks.yml` workflow.

Requires Python 3.12, 3.13 or 3.14 and uv 0.10.12. Python 3.12 is the default in
`.python-version`. Use `--python 3.14` on each uv invocation to select an already
installed 3.14 interpreter, or set `UV_PYTHON` for the session. No API key, SAP
system, Docker, host installation or `.env` file is needed.

From the repository root, on PowerShell, macOS or Linux:

```console
python -m pip install uv==0.10.12
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv run --locked pytest
uv run --locked python -m supersap smoke --json
uv run --locked python scripts/check_distribution.py
```

Use `python3` for bootstrap if the OS does not expose `python`. `uv sync --locked`
checks manifest/lock consistency and installs the default development group.
It may download Python if the selected interpreter is absent. Initial dependency
installation requires network access; subsequent smoke/test checks use no remote
services. Dependencies and their wheels/sdists are pinned with hashes in
`uv.lock`; intentionally refresh with `uv lock --upgrade` and review/retest the
change. Tool bootstrap and build backend are pinned separately in this document
and `pyproject.toml`.

`supersap --help`, `supersap --version`, `supersap smoke [--fixture FILE] [--json]`
and `python -m supersap ...` are the current CLI surface. `--json` may precede
the subcommand. Success goes to stdout, errors to stderr with a recovery hint.
Exit codes: 0 success, 2 invalid input, 3 policy gate, 4 transient failure, 5
internal error. Help/version remain plain text. No future command reports fake
success. Fixture diagnostics do not print file paths, input values or tracebacks.

The bundled sample is original synthetic content. User fixtures are bounded at
64 KiB and validated with a bundled schema, never executed or fetched. Unknown
versions, extra properties, duplicate keys, nonfinite numbers and non-MOCK
evidence labels are rejected. UTF-8/BOM, CRLF, whitespace and JSON key order do
not alter the normalized hash. No telemetry or source upload exists.

The distribution checker builds wheel/sdist twice, compares bytes, rebuilds the
wheel from the sdist, installs hash-locked runtime dependencies and the wheel in
a fresh environment under `.local`, then compares both CLI entry points against
the golden output repeatedly from a different working directory. It checks
the packaged typing marker too. Temporary artifacts are cleaned up. This is
Python package verification; four-host installation belongs to TASK-015–019.

CI applies these checks to Windows/macOS/Linux × Python 3.12/3.13/3.14 using
read-only GitHub permissions. A configured matrix is not execution evidence;
record actual results in `docs/evidence/TASK-001.md`. The official
[uv locking documentation](https://docs.astral.sh/uv/concepts/projects/sync/)
explains why checks use `--locked` rather than silently updating dependencies.

If Windows Application Control blocks a newly generated launcher (WinError 4551),
record the failed invocation and use `python -m supersap` for module diagnostics.
Do not weaken machine security policy or claim console acceptance from module
success. Console tests and the distribution checker fail on that error; they do
not skip the check. See the evidence log for the current workstation's results.
