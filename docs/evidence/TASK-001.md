# TASK-001 acceptance record — 2026-09-27

Implementation complete for this increment; full acceptance remains pending the
unexecuted OS/Python CI matrix and human review. TASK-002 has not started.

## Requirement mapping and acceptance

| Acceptance criterion | Artifact / evidence | Result |
|---|---|---|
| Typed Python workspace | `pyproject.toml`, `src/supersap`, `py.typed`; strict mypy | STATIC pass, 8 Python files |
| Lockfile | `uv.lock`, pinned uv/build backend, hashed runtime export | STATIC pass; locked installation succeeds |
| CI | `.github/workflows/ci.yml`: Windows/macOS/Linux × Python 3.12/3.13/3.14 | Defined; remote execution pending |
| Lint/type/test gates | Ruff lint/format, mypy strict, pytest | STATIC/MOCK pass: 37 tests, none skipped |
| Schema directory and samples | `schemas/README.md`, packaged Draft 2020-12 schema and synthetic fixtures | MOCK positive/negative tests pass |
| CLI skeleton | Console and module entry points; help/version, smoke, JSON/text, stable errors | STATIC/MOCK pass on Windows 3.14.7 |
| Clean installation | Fresh venv, hash-locked runtime dependencies, built wheel, external working directory | Windows pass; macOS/Linux pending |
| Reproducible smoke | Golden normalized output, repeated installed runs, CRLF/BOM/key-order equivalence | MOCK pass; fixture hash below |
| Reproducible packaging | Two byte-identical wheel/sdist builds; wheel rebuilt from sdist matches | STATIC pass |

Requirements: FR-09 deterministic checks, FR-12 input isolation/redacted diagnostics,
NFR-01 determinism, NFR-03 cross-platform workspace foundation. ADR references:
ADR-001/004 retain product scope, ADR-009 evidence labels, ADR-010 Python proposal,
ADR-012 implementation choices. This task contributes foundations, not complete
FR/NFR product acceptance. All 15 domains D01–D15 and Claude Code, Codex, OpenCode,
DeepSeek Harness remain in scope. Host behavior, SAP edition/release advice,
harvesting and publication are not implemented or certified here.

## Repository inspection

Read `prompts/START_HERE.md` first, then its ordered README/AGENTS/RULES/PRD/
ARCHITECTURE/TRD/DATA_MODEL/DECISIONS/TASKS list. Read DOMAIN_COVERAGE, SECURITY,
HOST_COMPATIBILITY, TEST_PLAN, MEMORY, SOURCE_POLICY, RELEASE_VERSIONING,
BENCHMARKS and the task-index pointer before implementation. `rg --files --hidden
-g '!.git/**'` found specification documents plus `.gitignore` and `.env.example`;
no existing application, tests or project config. `git status --short` returned
128, "not a git repository". No Git initialization, commit or publication was made.
`py --list`, `python --version` and `python -m pip --version` identified Python
3.14.7 / pip 26.2.1; uv was initially absent.

## Exact final verification commands

Run from `C:\Users\arohi\Desktop\Project\SuperSAPDEV` in PowerShell. The explicit
Python path overrides the baseline `.python-version` (3.12).

```powershell
python -m pip install --target .tools uv==0.10.12 --index-url https://pypi.org/simple --disable-pip-version-check
.\.tools\bin\uv.exe lock --default-index https://pypi.org/simple --cache-dir .uv-cache --python C:\Python314\python.exe
.\.tools\bin\uv.exe sync --locked --cache-dir .uv-cache --python C:\Python314\python.exe
.\.tools\bin\uv.exe run --locked --python C:\Python314\python.exe --cache-dir .uv-cache ruff check .
.\.tools\bin\uv.exe run --locked --python C:\Python314\python.exe --cache-dir .uv-cache ruff format --check .
.\.tools\bin\uv.exe run --locked --python C:\Python314\python.exe --cache-dir .uv-cache mypy
.\.tools\bin\uv.exe run --locked --python C:\Python314\python.exe --cache-dir .uv-cache pytest -q --tb=short
.\.tools\bin\uv.exe run --locked --python C:\Python314\python.exe --cache-dir .uv-cache supersap smoke --json
.\.tools\bin\uv.exe run --locked --python C:\Python314\python.exe --cache-dir .uv-cache python scripts/check_distribution.py --uv .tools/bin/uv.exe
```

All final commands exited 0. Results: lock resolved 19 packages; sync installed
the project and 18 development/runtime dependencies. Ruff: "All checks passed!";
format: "8 files already formatted"; mypy: "Success: no issues found in 8 source
files"; pytest: **37 passed in 3.43s**. The distribution checker installed five
runtime dependencies and the wheel in a fresh temporary environment, exercised
module and console entry points twice, and checked bundled schema, fixture and
typing marker. Temporary artifacts were removed after verification.

Resolved primary tools: uv/uv_build 0.10.12, Ruff 0.15.22, mypy 1.20.2,
pytest 9.1.1, jsonschema 4.26.0. `uv.lock` contains exact transitive pins/hashes.

MOCK smoke fixture SHA-256:
`1037888df52a95f7d57116abc10184bfe2033021b7dfc40bf374f0d4d0fceb58`.

STATIC verified development wheel SHA-256:
`de84d64290f16d4bf906613e118e90639926c91f9f4ab4e7b359b2da4ef95920`.
This identifies the package source/README bytes at verification, not a signed or
human-approved skill release. Evidence documents are outside wheel contents.

## Iteration and failure record

- Initial sandbox bootstrap command (`python -m pip install --target .tools
  uv==0.10.12 --disable-pip-version-check`) could not resolve a distribution.
  Repeated with approved network access and explicit public index; succeeded.
- Initial sandbox uv lock invocation reported access denied. The same command
  succeeded with approved execution/network access; no security policy changed.
- Ran `ruff check . --fix` and `ruff format .` through the same locked uv prefix.
  Initial lint reported six long lines; formatter and a shortened diagnostic fixed
  them. Strict mypy found an `ArgumentParser.error` return annotation mismatch;
  changing it to `Never` fixed the actual contract.
- Initial `pytest` run had 35 passes, a launcher failure and two errors caused by
  huge parametrized test names during Windows temp-directory handling. Explicit
  short case IDs fixed the names. Focused command `uv run ... pytest
  tests/test_cli.py::test_entrypoints_work_outside_repository -q --tb=short`
  confirmed WinError 4551 (Application Control) on the generated launcher. Later
  full tests and fresh-wheel console checks passed without policy changes. Final
  tests contain no skips or local bypass options.
- Distribution verification first selected unavailable Python 3.12 because of
  `.python-version`; it now explicitly uses its running interpreter for child
  uv commands. The second attempt counted uv's generated `.gitignore` as a build
  artifact; excluding that metadata fixed the checker. Final strict verification
  passes with two actual artifacts and both entry points.
- The golden fixture digest was independently calculated once with Python
  `hashlib.sha256` over explicitly constructed, sorted compact JSON; it is retained
  as a reviewed test expectation, not regenerated by tests.

## Files changed

Existing files updated:

- `.gitignore` — ignore local tool/cache/test artifacts.
- `README.md` — current implementation, setup and accurate pending scope.
- `TASKS.md` — visible task ledger; full backlog retained.
- `docs/DECISIONS.md` — ADR-012.
- `docs/MEMORY.md` — handoff, results and outstanding acceptance.
- `docs/TEST_PLAN.md` — link to implemented workspace evidence.

New files:

- `.gitattributes`, `.python-version`, `pyproject.toml`, `uv.lock`.
- `.github/workflows/ci.yml`.
- `src/supersap/__init__.py`, `src/supersap/__main__.py`, `src/supersap/cli.py`.
- `src/supersap/contracts.py`, `src/supersap/smoke.py`, `src/supersap/py.typed`.
- `src/supersap/README.md` (module ownership and dependency plan).
- `src/supersap/schemas/smoke.schema.json`, `src/supersap/fixtures/smoke.json`.
- `schemas/README.md` (catalog; canonical schemas ship inside the package).
- `tests/test_cli.py`, `tests/test_smoke.py`.
- `tests/fixtures/README.md`, `tests/fixtures/untrusted.json`, `tests/fixtures/smoke.expected.json`.
- `scripts/check_distribution.py`.
- `docs/DEVELOPMENT.md`, `docs/evidence/TASK-001.md` (this record).

Generated `.tools`, `.venv`, `.uv-cache`, `.local` and Python/test caches are local
artifacts, not source changes or release content. This inventory comes from the
initial document-only tree and recorded edits; Git diff is unavailable.

## Blockers and next dependencies

The nine-cell CI workflow is ready but not executed: no Git metadata/remote or
macOS/Linux runners are available in this checkout. Python 3.12/3.13 likewise
remain untested locally. Retain actual CI run evidence before marking TASK-001
fully accepted. No LIVE SAP evidence is produced or needed for this task.

Next is TASK-002: entity schemas, migrations, registry/evidence graph, append-only
audit, state transitions, duplicate handling and rollback tests. No later task
was started, and no knowledge/skill release was promoted or published.
