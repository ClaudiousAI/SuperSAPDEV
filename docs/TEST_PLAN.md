# Full product test plan

## Levels and evidence

TASK-001's implemented checks and OS/Python execution ledger are recorded in
[`evidence/TASK-001.md`](evidence/TASK-001.md); commands are in
[`DEVELOPMENT.md`](DEVELOPMENT.md). Its synthetic smoke/schema checks validate
the workspace only. They do not satisfy domain, host or live SAP conformance.

The executed nine-cell GitHub matrix and draft-delivery checks are recorded in
[`evidence/CI-CD.md`](evidence/CI-CD.md). CI retains JUnit reports and a verified
development candidate; draft delivery checks its hashes before attaching it.

| Level | Representative tests | Gate |
|---|---|---|
| Unit/schema | Canonical URIs, hashes, applicability interval, state transitions, conflicting claims, license and prompt-injection classification, CLI error codes. | No schema bypass or invalid transition. |
| Connector/integration | Pagination, ETag, rate limits, renamed/deleted sources, 30-day overlap, last-success cursor, outage >30 days, failure mid-page, duplicate event replay. | No missed or duplicate promotion; cursor advances only after success. |
| Agent/orchestrator | Malformed/adversarial model output, inconsistent citations, source text instructing agent, independent review requirement, retries/dead-letter. | No model-only approval or instruction execution. |
| Pack/compiler | All 15 coverage matrices, source/release provenance, conflict dependency graph, immutable snapshot, byte-identical builds. | Every domain gate passes with no unsupported normative claim. |
| Workflow | Think/Plan approvals, stage artifacts, Clean Core applicability, blocking review, static/mock/live labeling, no SAP deployment claim. | Cannot advance with missing required evidence. |
| Host E2E | Four hosts across supported OS/version matrix, native invocation, domain routing, install/upgrade/rollback/uninstall, path collision. | Native discovery and semantic artifacts on each supported host. |
| Security | Prompt injection corpus, SSRF, path traversal/symlink, malicious package, RBAC/CSRF, log redaction, compromised source revocation. | Zero critical/high open findings and tested recovery. |
| Performance/operations | Large source pagination, concurrent jobs, DB migration/backup restore, scheduler lag, release rollback, UI accessibility. | Meets documented SLO and recovery thresholds. |

## SAP answer quality

Use a versioned expert-reviewed golden corpus spanning all 15 packs and cross-pack scenarios. Include contradictory sources, obsolete ABAP patterns, ABAP Cloud released API checks, RAP/CDS authorization, IDoc retries, CAP/BTP tenancy, modernization, and AI data safety. For each scenario assert required decisions, prohibited suggestions, cited evidence, edition/release qualifier, and evidence class; do not depend on exact response wording. Blind review samples by SAP experts, track regressions across model/prompt/pack/host versions, and block release on critical unsafe guidance.

## Live versus offline

Static checks and mocks are first-class product tests. Optional connected validation may later run on a separately approved isolated SAP landscape with traceable release and tool evidence; only those results are `LIVE`. CI cannot relabel static parser success as ABAP activation, ABAP Unit or ATC. Where live integration is absent, release notes state the limitation and provide developer validation steps.

## Release gate

All required tests pass, every domain and host has a current benchmark, no untriaged source conflict or critical security issue, license/provenance audit passes, build is reproducible, reviewer and release approver sign off, rollback drill passes. Failures produce specific task IDs and block publication; no blanket override without documented risk acceptance and independent approval.
