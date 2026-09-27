# Architecture decision record

| ID | Status | Decision | Rationale and consequence |
|---|---|---|---|
| ADR-001 | Accepted | Build the full skill harvesting and portable SAP skill product; postpone full SAP execution platform. | Keeps this product cohesive while retaining all 15 domain packs and full operational lifecycle. |
| ADR-002 | Accepted | Four specialized agents under one deterministic orchestrator and human approval. | Models generate candidates; code enforces transitions, provenance, and releases. |
| ADR-003 | Accepted | Discovery owns 30-day delta checker and new skill finder, with dedicated scheduled jobs. | One source inventory and durable cursor; neither flow bypasses verification. |
| ADR-004 | Accepted | One shared skill core with versioned Claude Code, Codex, OpenCode, DeepSeek Harness adapters. | Portable behavior with native packaging and measured host differences. |
| ADR-005 | Accepted | SAP-specific Think → Plan → Build → Review → Test → Ship → Reflect. | Adopt the architecture-first review rhythm inspired by gstack; author original SAP guidance and enforce critical gates in code. |
| ADR-006 | Accepted | Official SAP sources and maintained examples anchor normative facts. | Community sources illustrate patterns but cannot override release-specific official rules without review. |
| ADR-007 | Accepted | No hard repository count; use concept coverage, source diversity, authority, and saturation. | Prevents superficial completeness and allows different evidence needs by domain. |
| ADR-008 | Accepted | A skill release pins knowledge snapshot, policy, adapter and benchmark versions independently. | Reproducibility and targeted rollback. |
| ADR-009 | Accepted | Static and mock evidence must be labeled; live SAP checks are optional external integration. | Avoids false activation, ATC, and deployment claims. |
| ADR-010 | Proposed for implementation | Python 3.12+ CLI/orchestrator, SQLite local metadata with migration path to PostgreSQL, JSON Schema contracts, local review web UI. | Small operational footprint and inspectable records; benchmark concurrency and add PostgreSQL backend if deployment requires it. Do not treat proposed technology as a product requirement. |
| ADR-011 | Accepted | Primary OpenAI model, optional Gemini fallback, with versioned prompts and schema output; model choice configurable. | Avoids model lock-in; failures go to review, not automatic approval. |

Change an accepted decision only through a new dated ADR with migration effects and reviewer approval. Validate all host path and behavior assumptions against official host docs during implementation.

## ADR-012 — TASK-001 workspace implementation (2026-09-27)

Status: implemented within the user-authorized TASK-001 scope; no change to an
accepted product decision. Implements the Python portion of proposed ADR-010;
database and UI choices remain open for their tasks.

Use Python 3.12–3.14, `src/supersap`, uv/uv_build 0.10.12, a universal `uv.lock`
with artifact hashes, Ruff, strict mypy, pytest and JSON Schema Draft 2020-12.
Python 3.15+ requires a future dependency/CI compatibility check. CI runs nine
OS/Python combinations. Action revisions and build backend are pinned. CI only
validates; there is no publishing job. The package is a development prerelease,
not an approved skill release.

Bundle schemas and a synthetic smoke fixture under the Python package and index
them in `schemas/README.md`, avoiding duplicated contracts and source-tree path
dependencies in wheels. Smoke output uses canonical UTF-8 JSON and a normalized
fixture hash, no timestamps or local paths, and always labels evidence MOCK.
All 15 domains and four hosts are scope declarations only. Entity/state schemas
remain TASK-002; no database or approval behavior is stubbed into this increment.

CLI supports text/JSON diagnostics and exit codes 0/2/3/4/5. This increment uses
0/2/5 naturally; tests inject typed failures to verify future 3/4 handling without
pretending that policy or connectors exist. Unknown commands fail explicitly.

Verification sources (checked 2026-09-27): [uv lock/sync semantics](https://docs.astral.sh/uv/concepts/projects/sync/),
[build backend/resource inclusion](https://docs.astral.sh/uv/concepts/build-backend/),
[CI guidance](https://docs.astral.sh/uv/guides/integration/github/).
Behavior is additionally checked against the pinned local toolchain. No SAP
release or coding-agent host behavior assumptions are introduced by this task.

## ADR-013 — GitHub CI and draft delivery (2026-09-27)

Status: accepted within the user's explicit CI/CD setup request for
`ClaudiousAI/SuperSAPDEV`. Extends ADR-012's validation-only CI with manual draft
delivery; it does not authorize a product release or complete TASK-022 early.

TASK-001 owns the nine OS/Python gates and retained test evidence. A reusable
workflow validates the exact caller commit and retains the verified wheel/sdist
from Linux/Python 3.12. Manual delivery on `main` reruns all gates, then a separate
job with repository write permission creates an unpublished draft prerelease
from those exact artifacts. No package registry credentials or SAP credentials
are used. Source execution happens only in read-only jobs. The draft tag includes
commit and run identity, so retries never overwrite a prior candidate.

This resolves the requested CI/CD scope against TASK-022's unmet dependencies:
deliver reviewable development candidates now; keep public package/skill
publication, signing, SBOM, domain/host conformance and independent release
approval blocked on the full release contracts. A GitHub draft is preparation,
not approval. There is no automatic publish path. Repository administration and
source push are authorized by this request; knowledge promotion is not.

Acceptance: lint, format, strict types, tests, reproducible builds and clean
wheel installation on all nine cells; stable aggregate status; retained reports;
workflow syntax validation; draft preparation consumes tested bytes with SHA-256
and source/run metadata. Evidence remains STATIC/MOCK, never LIVE SAP.
