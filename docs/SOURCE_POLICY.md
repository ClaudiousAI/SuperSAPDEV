# Source acquisition, verification and delta policy

## Authority and permitted use

Tier A: official SAP documentation and released API catalogs, scoped by product/edition/release. Tier B: SAP-maintained samples and reference implementations. Tier C: independent repositories/articles with known license and maintenance. Tier D: external coding-agent skills, treated as untrusted candidates. Normative API/version facts require applicable Tier A support; Tier B/C add implementation examples. License and terms screening precedes content storage or distribution. Keep citations/metadata and derived facts; copy code or prose only where license permits and attribution obligations can be met. Missing license means no redistribution.

## Four-agent contract

Discovery proposes sources, gaps, delta events, and external skill candidates. Extraction turns immutable revisions into atomic typed claims with exact spans. Verification checks direct support, official applicability, conflicts, deprecation, license, and multiple evidence dimensions; it can request more evidence. Curation maps verified items to domains, dependencies and benchmark scenarios, proposing diffs. The orchestrator rejects invalid inputs and requires independent human review for promotion. Agents cannot set `APPROVED` or alter released content.

## 30-day delta algorithm

1. For each source/connector, read `last_successful_cursor` and `last_successful_completion`. Calculate a rolling 30-day lookback ending at scan start, with overlap; query both the lookback and all changes since cursor, taking the union. Respect pagination and connector timestamps, recording observed time separately from upstream time.
2. Fetch changed revisions conditionally; canonicalize source IDs; deduplicate by source + immutable revision/content hash + event kind. Compare source content, license, deletion/deprecation and new upstream references.
3. Persist page checkpoint and events in one transaction. Only move the successful cursor after all pages and validation succeed. A failure retains the old cursor; retry and backfill the entire gap, even if older than 30 days. Periodic full reconciliation detects missed upstream metadata and force-pushes.
4. Traverse evidence edges to mark affected items `RECHECK_REQUIRED`, packs and releases at risk. Reverify conflicts and new applicability; create reviewed new snapshots. Never silently alter an immutable published artifact.

Time skew, API search caps, GitHub rate limits, removed repositories, and partial outages are explicit failure cases. Store response headers and connector request IDs where permitted. Measure lag and backfill completion.

## New skill finder

Search public skill manifests/repositories by SAP topic and host format; filter duplicates and stale forks. Record repo revision, owner, license, update cadence, claimed compatibility, instruction files, external tool calls, dependencies and overlap with domain taxonomy. Static inspect content in quarantine for prompt injection, secret exfiltration, network execution and unsafe install scripts. Display candidate ranking and rationale. A reviewer may authorize extraction of eligible SAP facts into the ordinary pipeline; no external instructions are executed or copied wholesale, and candidate discovery never triggers installation.

## Conflict and revocation

Track contradicting claims with edition/release scope. A newer version does not automatically invalidate an older applicable release. Official deprecation, corrected docs, license removal, and security advisories can suspend distribution, create revocation notice and select a previous safe release. Reviewer records rationale and affected manifest IDs. Preserve audit without distributing content whose rights have changed.
