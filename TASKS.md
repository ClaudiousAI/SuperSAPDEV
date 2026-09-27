# Full product delivery backlog

This is the complete implementation backlog, not an MVP cut. Complete tasks in dependency order through production release. Each task must include tests, documentation, review and a demonstrable acceptance artifact. Record progress and blockers in `docs/MEMORY.md`; do not check off a task based on a placeholder.

| ID | Dependencies | Work and acceptance evidence |
|---|---|---|
| TASK-001 | None | Establish typed Python workspace, lockfile, CI, lint/type/test gates, schema directory, CLI skeleton and sample fixtures; clean install on Windows/macOS/Linux, reproducible smoke run. |
| TASK-002 | 001 | Implement schemas, migration-backed registry, source revision/evidence graph, append-only audit and state machine; invalid transition, duplicate and rollback tests. |
| TASK-003 | 001–002 | Implement source policy and connectors for official SAP pages/samples and GitHub with terms/license metadata, allowlist, cache, pagination, budgets and SSRF defenses; fixture-backed connector tests and performance baseline. |
| TASK-004 | 002–003 | Build durable scheduler/orchestrator, leases, idempotent jobs, retries/dead-letter, page checkpoints and metrics; injected failure/restart test. |
| TASK-005 | 003–004 | Discovery Agent and coverage gap ranking; source diversity/authority scores with explainable candidates; no automatic promotion. |
| TASK-006 | 003–005 | 30-day delta checker plus durable cursor, overlap, outage backfill, full reconciliation and dependency invalidation; >30-day outage, deletion and changed-license tests. |
| TASK-007 | 003–005 | New skill finder with manifest detection, quarantine/static risk and license/overlap report; malicious candidate never executes or installs. |
| TASK-008 | 002–004 | Extraction Agent with atomic typed claims, source spans, model adapter, bounded JSON output and offline fixtures; rejects unsupported spans. |
| TASK-009 | 002, 008 | Verification Agent with authority, edition/release, corroboration, conflict/deprecation and confidence tuple; official-vs-community conflict tests. |
| TASK-010 | 002, 009 | Curation Agent, taxonomy, cross-pack dependencies, saturation/coverage matrix and proposed diffs; cannot publish unreviewed items. |
| TASK-011 | 004, 008–010 | Review API/CLI, RBAC, optimistic approvals, separation of duties and audit; approval gate security tests. |
| TASK-012 | 010–011 | Build all 15 domain packs D01–D15 with reviewed official evidence, examples, anti-patterns, release support and golden scenarios; each passes its coverage contract. Research and implementation can be parallel across domains but the release gate requires all. |
| TASK-013 | 002, 011–012 | Pack compiler, immutable knowledge snapshot, conflict graph, manifest and deterministic build; same inputs produce identical hashes. |
| TASK-014 | 001, 013 | Shared SAP skill core and seven-stage workflow schemas/prompts, architecture approval and deterministic gate CLI; invalid transitions and evidence mislabeling blocked. |
| TASK-015 | 014 | Claude Code adapter and native package; install/discovery/invocation/artifact test on pinned host versions. |
| TASK-016 | 014 | Codex adapter and native package; same conformance suite. |
| TASK-017 | 014 | OpenCode adapter and native skill-tool package; same conformance suite. |
| TASK-018 | 014 | DeepSeek Harness filesystem-provider adapter; pin developer-preview version and pass conformance suite or explicitly block unsupported version. |
| TASK-019 | 013, 015–018 | Cross-platform installer/doctor/uninstall with dry-run, integrity, collisions, backups, idempotence, upgrade and rollback; Windows path tests. |
| TASK-020 | 006–013 | Local review dashboard: overview, source delta, skill candidates, item evidence/conflicts, coverage, benchmarks, release and audit; accessible loading/error/conflict states and role tests. |
| TASK-021 | 012–019 | Expert golden corpus, all-domain/cross-domain and adversarial benchmark runner, host comparison, regression reports; zero critical unsafe recommendations. |
| TASK-022 | 006–007, 011, 013, 019–021 | Release pipeline, protected approvals, versioned manifests, checksums/signatures, SBOM, changelog, revocation, rollback; clean install of release on all hosts. |
| TASK-023 | 004, 020–022 | Production operations: scheduling, backup/restore, migration rehearsal, observability, alerting, retention, incident drill and runbooks; tested outage and recovery. |
| TASK-024 | 001–023 | Full security/privacy/license review, all FR/NFR acceptance, docs/support matrix, usability/accessibility review, failure drills and final release signoff. |

## Definition of done for every task

Mapped requirement and ADR references; implemented code and schemas; positive/negative tests; reviewer-readable output; docs updated; no secrets or unauthorized content; exact commands/results recorded. Dependents may start after the upstream interface is stable, but release publication needs every gate. If source evidence for a domain is unavailable, record a reviewed unsupported release scope rather than fabricating knowledge.

## Task ledger (2026-09-27)

| Task | State | Evidence / next dependency |
|---|---|---|
| TASK-001 | Implemented; cross-platform acceptance pending | [Evidence](docs/evidence/TASK-001.md). Windows Python 3.14: 37 tests and clean package/reproducibility checks pass. Remaining OS/Python CI executions pending. |
| TASK-002–024 | Not started | Full scope and dependency graph above remain unchanged. TASK-002 follows TASK-001; this change stops at the requested task boundary. |

CI/CD follow-up (2026-09-27): TASK-001 automation is extended with retained
evidence and a stable required check. A user-authorized TASK-022 foundation adds
manual **draft-only** delivery without claiming its unmet dependencies complete.
See [CI/CD evidence](docs/evidence/CI-CD.md) and ADR-013. All other task states
and the complete product release contract remain unchanged.
