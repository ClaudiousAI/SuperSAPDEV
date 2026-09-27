# Product requirements

## Vision and users

Super SAP Dev turns verifiable SAP engineering knowledge into an installable skill that helps coding agents design and implement SAP application changes. Users are SAP developers and architects, knowledge curators, release maintainers, security reviewers, and teams using Claude Code, Codex, OpenCode, or DeepSeek Harness. The complete product includes every capability below; task phases describe delivery order only.

## Outcomes and measurable acceptance

| ID | Requirement | Product acceptance |
|---|---|---|
| FR-01 | Discover and ingest permitted official SAP, SAP-maintained, and independent sources | Search, deduplicate, pin revisions, classify authority/license, retain source metadata and retrieval evidence; reject restricted/unknown redistribution. |
| FR-02 | Four-agent harvesting pipeline | Discovery, Extraction, Verification, Curation produce schema-valid proposals; deterministic orchestrator persists retries and state; no LLM can approve itself. |
| FR-03 | Continuous currency | Scheduled 30-day lookback plus last-success cursor, pagination, overlap, idempotent upsert, outage backfill; changed/deleted/deprecated sources flag affected facts and releases. |
| FR-04 | New skill finder | Detect and assess compatible external skills; report provenance, license, trust, overlap, maintenance, and proposed domain use; manual approval required before importing content. |
| FR-05 | Full SAP coverage | All 15 domain packs in `DOMAIN_COVERAGE.md` reach defined release gates, with cross-pack consistency and explicit supported SAP applicability. |
| FR-06 | Evidence-driven knowledge | Each item has type, source revision, edition/release applicability, confidence dimensions, status, reviewer, tests, and supersession history. Conflicts are surfaced, not silently merged. |
| FR-07 | Portable skill | Native install, discovery, invocation, upgrade, and uninstall on four hosts, from one reviewed core and versioned adapters. Host-specific limitations documented. |
| FR-08 | SAP development lifecycle | Think, Plan, Build, Review, Test, Ship, Reflect with artifact contracts, bounded changes, gates, and human decisions; apply SAP Clean Core and released API checks where applicable. |
| FR-09 | Deterministic checks | CLI validates manifest, citations, policy, applicability, artifact gates, host builds, package integrity, and evidence labels independently of model output. |
| FR-10 | Review and operations | Local reviewer dashboard/CLI shows queues, diffs, source graph, conflict resolution, benchmark outcomes, audits, scheduler health, retry and rollback controls. |
| FR-11 | Release distribution | Versioned packs/core/adapters/policy/snapshot, reproducible build, checksums, CI benchmarks, human signoff, changelog and rollback. |
| FR-12 | Security and privacy | Source isolation, prompt injection defense, least-privilege credentials, license checks, no customer data in global packs, no unapproved SAP writes. |

## Nonfunctional requirements

| ID | Target and test |
|---|---|
| NFR-01 | Same inputs and pinned revisions produce byte-identical normalized manifests and content hashes; nondeterministic agent prose cannot alter approved records. |
| NFR-02 | Scan restart resumes without loss or duplicate promotion; checkpoint and transaction tests cover partial pages, rate limits, and outage backfill. |
| NFR-03 | CLI works on current Windows, macOS, Linux Python-supported environments; installation tests include Windows path/line-ending behavior. |
| NFR-04 | Every approved statement can be traced to source URI/revision, review, benchmark, pack and release; no unsupported normative statement ships. |
| NFR-05 | Dashboard binds loopback by default; credential and audit redaction verified; no telemetry or source upload enabled by default. |
| NFR-06 | Host adapters pass golden invocation and package integrity tests on pinned supported host versions; degraded capability is explicit. |

## End-to-end journeys

1. Maintainer registers a source and domain; scan obtains immutable revision and license evidence; extraction proposes items; verifier checks official evidence, conflicts and applicability; curator proposes pack placement; reviewer approves; benchmark and CI release a pinned snapshot.
2. Scheduled scan finds a source changed within its rolling window or since cursor; impacted items become `RECHECK_REQUIRED`; release health surfaces warnings; reviewer resolves and creates a new snapshot. Failed scans keep prior cursor and backfill on recovery.
3. New skill finder reports a candidate skill. Reviewer inspects the repository and license, quarantines its instructions, explicitly authorizes eligible content extraction, and routes extracted claims through normal verification.
4. Developer installs a host-native skill, invokes it on a SAP requirement, supplies landscape and release, reviews architecture options, implements a bounded change, receives static test evidence and a PR package; any unavailable SAP live validation is called out.

## Exclusions and constraints

No broad autonomous FSD-to-deployed-object orchestration, mandatory SAP connection, production transport/release, or unsupervised ingestion of external skill instructions. Runtime recommendations require contextual qualification; no universal rule can be inferred from one sample. The product may later integrate a separately authorized SAP tool broker with distinct permissions and evidence contracts.

## Release definition

The product release requires all FR and NFR gates, every domain and host conformance suite, reviewer UX, scheduled operation, reproducible artifacts, security review, install/upgrade/uninstall recovery, and documented support matrix. “Implemented” never means a prompt alone or a stub package.
