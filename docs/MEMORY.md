# Project memory / handoff

## Current state

As of 2026-09-27 TASK-001's Python workspace, CLI foundation, smoke schema/fixtures,
lockfile and nine-cell CI matrix are implemented. Windows Python 3.14.7 verification
passes: 37 tests, Ruff lint/format, strict mypy, byte-identical wheel/sdist builds,
sdist-to-wheel reconstruction, clean wheel install and both CLI entry points.
See [exact evidence and changed files](evidence/TASK-001.md).

TASK-001 is **not marked fully accepted**: macOS/Linux and Python 3.12/3.13 checks
are configured but remote execution is pending. The user has now authorized
GitHub CI/CD setup for `ClaudiousAI/SuperSAPDEV`; see [CI/CD evidence](evidence/CI-CD.md)
and [operations](CI_CD.md). Initial
Windows Application Control launcher errors disappeared on subsequent required
checks without policy changes; no skipped tests or bypass option remain.

Harvesting, registry, dashboard, domain packs, runtime workflow and native host
installs remain unimplemented. The previous separate `super-sap-dev` execution
platform must not override this full skill-harvesting product dossier.

## Decisions to retain

- All 15 SAP packs; four harvesting agents; deterministic orchestrator; reviewer approval.
- 30-day delta plus durable cursor and outage backfill; external skill discovery never auto-installs.
- Native Claude Code, Codex, OpenCode and DeepSeek Harness installs; shared core, measured host differences.
- SAP Think/Plan/Build/Review/Test/Ship/Reflect with deterministic CLI gates; no live SAP claims without evidence.
- Full product backlog, shipped in reviewable increments, not reduced to an MVP.

## Next action

Run `.github/workflows/ci.yml` when a GitHub repository/runner is available, retain
the actual matrix results and complete TASK-001 acceptance review. TASK-002 is next
in dependency order; it has not been started because this request stops at the
TASK-001 boundary. Validate actual host behavior and current SAP documentation
when implementing each pack. Repository setup credentials are process-only and
must not enter source or workflows. All current evidence is STATIC or MOCK,
never LIVE SAP evidence.

Use `docs/DEVELOPMENT.md` for normal setup. In this workspace uv is installed at
`.tools/bin/uv.exe`, Python at `C:\Python314\python.exe`, dependencies in `.venv`,
and cache in `.uv-cache` (all generated directories ignored). The local commands
explicitly select Python 3.14 because `.python-version` defaults to 3.12. Dependency
downloads required approved network access. Do not commit generated environments.

ADR-012 records workspace choices and the packaged schema catalog. All other
accepted decisions and full backlog requirements remain intact.

ADR-013 adds reusable CI checks, retained JUnit/candidate artifacts, pinned action
updates and manual draft prerelease preparation. The draft job consumes tested
bytes and never publishes; TASK-022's full release gates remain outstanding.

## Open implementation choices

- Exact supported host version matrix and distribution channel: establish via integration test fixtures, not assumptions.
- Per-domain SAP edition/release support ranges: research and explicitly publish support matrix before pack release.
- Dashboard framework and database backend: benchmark against NFRs and ADR-010.
- Legal review of source-specific licenses/terms and deployment retention policy before production ingestion.
