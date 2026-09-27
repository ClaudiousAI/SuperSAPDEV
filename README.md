# Super SAP Dev — full product implementation dossier

[![CI](https://github.com/ClaudiousAI/SuperSAPDEV/actions/workflows/ci.yml/badge.svg)](https://github.com/ClaudiousAI/SuperSAPDEV/actions/workflows/ci.yml)

GitHub runs cross-platform checks on pushes and pull requests. Manual draft
delivery prepares verified development artifacts for review. See the
[CI/CD runbook](docs/CI_CD.md) for triggers, artifacts and release limitations.

This repository defines a production-quality **SAP development skill factory and portable runtime skill**. It is a complete product specification, not an MVP specification. It does not specify the postponed FSD-to-transport execution platform. Implement the full backlog in `TASKS.md` through bounded, reviewable changes.

## Product boundaries

1. **Harvesting service:** discover, fetch, extract, verify, curate, benchmark, and version SAP knowledge from permitted sources. Four specialized agents operate under a deterministic orchestrator; human reviewers approve promotions and releases.
2. **Knowledge product:** 15 versioned domain packs with cited, release-aware rules, patterns, examples, tests, and anti-patterns. Keep source revision, license, applicability, confidence, and review status with each item.
3. **Portable development skill:** `super-sap-dev` guides Think → Plan → Build → Review → Test → Ship → Reflect, with SAP-specific artifacts and deterministic local checks. Native installers target Claude Code, Codex, OpenCode, and DeepSeek Harness.
4. **Operations:** scheduled 30-day delta scans with durable cursors/backfill, new-skill discovery, review dashboard, CI, benchmarks, signed/checksummed releases, audit, rollback, and maintenance.

The runtime can generate code and evidence in a local repository. It must never claim SAP activation, ATC, ABAP Unit, transport release, or production deployment without corresponding live tool evidence. A live SAP connector is a separately approved future integration, not a prerequisite.

## Read in this order

| Purpose | File |
|---|---|
| Coding agent entry | `prompts/START_HERE.md`, `AGENTS.md`, `RULES.md` |
| Product and delivery | `docs/PRD.md`, `TASKS.md`, `docs/DECISIONS.md` |
| Design and implementation | `docs/ARCHITECTURE.md`, `docs/TRD.md`, `docs/DATA_MODEL.md`, `docs/DESIGN.md` |
| Knowledge and workflow | `docs/DOMAIN_COVERAGE.md`, `docs/SOURCE_POLICY.md`, `docs/WORKFLOW.md` |
| Native hosts and distribution | `docs/HOST_COMPATIBILITY.md`, `docs/RELEASE_VERSIONING.md` |
| Quality and operations | `docs/TEST_PLAN.md`, `docs/BENCHMARKS.md`, `docs/SECURITY.md`, `docs/MEMORY.md` |

## Implementation status

TASK-001 provides the typed Python workspace, locked dependencies, CLI/schema
smoke check, tests and cross-platform CI definition. This is the foundation for
the complete backlog; harvesting, packs, host adapters and SAP execution are not
implemented. See [development instructions](docs/DEVELOPMENT.md) and
[TASK-001 evidence](docs/evidence/TASK-001.md) for commands, results and blockers.

```console
python -m pip install uv==0.10.12
uv sync --locked
uv run --locked python -m supersap smoke --json
```

The smoke command works offline after installation and emits synthetic `MOCK`
evidence. It lists product scope, not domain coverage or host certification.

## Implementation layout

`src/supersap/` contains the typed CLI foundation and packaged smoke schema/fixture;
`schemas/` indexes those contracts; `tests/` contains the quality suite;
`scripts/` checks distribution reproducibility and clean installation. Future
tasks add `packs/` for reviewed SAP knowledge, `skill/core/` for shared instructions,
`skill/hosts/` for adapters, `dashboard/` for reviewer UI and `releases/` for manifests.

## Getting started

Give the coding agent `prompts/START_HERE.md` and this repository. Follow the task
ledger and implement in dependency order, retaining full-product scope.
`.env.example` names optional credentials; do not commit `.env` or downloaded
proprietary material. Only `supersap smoke`, help and version are implemented;
other documented commands remain proposed contracts and are rejected by the CLI.

## Design authority

The user-provided [Vibe Coding guide](https://docs.google.com/document/d/12u0wXE0u0o5FNGj2sGy8OvOPHEtPSwD8ltwN0UcvqH4/edit) supplies the documentation and engineering workflow structure. The Think/Plan/Build/Review/Test/Ship/Reflect practice is inspired by [gstack](https://github.com/garrytan/gstack); create original SAP-specific instructions and do not copy its prompts. The product decisions in `docs/DECISIONS.md` take precedence over generic guidance. Where SAP edition or release is unknown, ask or declare an explicit assumption before offering implementation advice.
