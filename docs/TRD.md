# Technical requirements and contracts

## Proposed stack and repository

Python 3.12+ owns CLI, scheduling, connectors, orchestration, schemas, pack compilation, and deterministic gates. Use a lockfile and typed interfaces. Start with transactional SQLite/WAL for local use and an explicit repository interface/migration path to PostgreSQL for concurrent teams. JSON Schema validates interchange and release artifacts. The review UI is a local web app using server-side authentication for team deployments; keep all decisions through the same service API. GitHub Actions runs tests and signed release preparation, not automatic approval. Versioned LLM adapters support OpenAI primary and optional Gemini fallback; an offline deterministic mode supports rebuild and tests without an API key.

Suggested modules: `connectors`, `discovery`, `extract`, `verify`, `curate`, `orchestrator`, `registry`, `policy`, `compile`, `hosts`, `workflow`, `benchmarks`, `review_api`, `cli`. Put schema migrations under `migrations/`; never infer DB tables from free-form model output.

## CLI contracts (to implement)

| Command | Required behavior |
|---|---|
| `supersap source add/list/check` | Validate URI, terms/license, source kind, allowed domain, credentials and provenance. |
| `supersap scan --mode full|delta|skills [--since ...]` | Durable job, pagination, overlap, rate-limit recovery, idempotent results, dry-run option. Delta defaults to cursor + 30-day window. |
| `supersap review list/show/approve/reject` | Reviewer identity, rationale, optimistic version, audit; approval cannot skip policy gates. |
| `supersap pack validate/build --domain ...` | Schema and source graph checks, applicability, conflict detection, deterministic output. |
| `supersap benchmark run --snapshot ...` | Golden scenarios, negative/adversarial cases, host matrix, versioned metrics. |
| `supersap release prepare/publish/revoke/rollback` | Prepare immutable manifest and diff; publish only with human approval and CI evidence. |
| `supersap install/doctor/uninstall --host ... --scope project|user` | Native paths, dry-run, backup, atomic install, integrity check, reversible uninstall. |
| `supersap workflow init/check --stage ...` | Validate artifacts, applicability, evidence labels and stage gates without calling an LLM. |

All commands return stable exit codes: 0 success, 2 invalid input, 3 policy gate, 4 transient source/host failure, 5 internal error. Structured JSON output is available via `--json`; human output must include actionable recovery. Credentials may be in environment or OS secret store, never CLI arguments or logs.

## Job and agent interface

`Job {id, kind, idempotency_key, source_id?, cursor_start?, window_start?, status, attempts, lease_until, created_at}`; `AgentProposal {schema_version, job_id, agent, model_id, prompt_version, input_hashes, items[], evidence_refs[], uncertainty[], token_usage?}`. The orchestrator validates and commits proposals transactionally. A lease expiry retries the same idempotency key; task effects use upserts. Rate limits use connector-specific budget and conditional requests. Model responses are bounded in size, JSON constrained, separately logged by hash, and never granted filesystem or network execution rights.

## API contracts

Version `/api/v1` provides source inventory, scans, items, evidence graph, diffs, review queue/actions, domain coverage, benchmark results, release manifests, health and audit. GETs paginate and filter; writes require reviewer/operator roles, CSRF protection for cookie auth, idempotency keys for state changes, and optimistic concurrency. Export uses reviewed facts and source references only. Dashboard is optional for a CLI-only machine but is required in the full product release.

## Package format

A release manifest contains `skill_version`, `knowledge_snapshot_id`, `policy_version`, `core_version`, `adapter_versions`, `schema_version`, `source_digest`, `benchmark_run_id`, `review_approval_id`, build toolchain and SHA-256 per file. `skill/core/SKILL.md` holds concise routing instructions; domain detail is split into referenced files to avoid loading all 15 packs into every conversation. Compiled host bundles contain only approved content. Reject mismatched hashes or missing dependencies.

## Operation and recovery

Run initial full scan, then daily delta; the 30-day window is a default rolling overlap, not the only cursor. Queue a separate weekly skill-finder search and periodic full reconciliation. Expose last successful scan, lag, source failures, pending reviews, revocations, benchmark regressions, and release health. Keep retry/dead-letter handling, tested backup/restore, migration rehearsal, and documented retention. Use UTC timestamps and stable content hashes throughout.

## Performance targets

Set measurable baselines during TASK-003: ingest pagination without duplicates; a delta run resumes after injected failure; local CLI gate checks finish within 10 seconds for a normal single change-set on reference hardware; installation within 30 seconds excluding downloads; dashboard queues paginate at 100+ items. Measure rather than assume LLM latency; timeouts and budgets are configurable. These are engineering targets, not claims of current performance.
