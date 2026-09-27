# Operator and developer experience design

## Information architecture

The local review dashboard has: **Overview** (scan lag, release status, domain coverage and blocked items), **Sources** (authority/license/revision history), **Candidates** (new sources and external skills), **Review queue** (atomic claim, exact evidence span, edition/release, conflicts, proposed pack diff), **Domains** (15-pack coverage and weak concepts), **Benchmarks** (scenario regressions and host comparisons), **Releases** (manifest diff, approval and rollback), **Audit/Settings** (roles, schedules, budget and retention). Search and filters preserve shareable item IDs.

## Critical screens and interactions

| Screen | Required states and action |
|---|---|
| Review item | Side-by-side proposed claim and cited source, revision/hash, license, authority, conflicts, applicability, related items, generated explanation; approve, reject, request evidence with rationale; disabled approval when gate fails. |
| Source delta | Added/changed/deleted/license change, last cursor/window, affected items/packs/releases; recheck job and acknowledged false positive. |
| Skill candidate | Repository/revision, native format, license, overlapping packs, maintenance history, suspicious instructions; quarantine badge and explicit content extraction request only. |
| Coverage matrix | Every domain, concepts and evidence classes, authoritative support, unresolved conflicts, benchmark scenarios; drill to deficient concept and source search. |
| Release preparation | Component pin/diff, failing gates, benchmark deltas, source/pack changes, reviewer identities; approval and publish separated by role. |

## Workflow in coding hosts

The install command displays target path, existing-file conflict, package version and checksum before writing. `doctor` confirms native discovery, manifest integrity and invocation instructions. In a session, the skill begins with landscape/edition/release questions, creates Think and Plan artifacts, and asks for architecture approval before a nontrivial change. Short requests can use compact artifacts but may not skip safety/applicability gates. It gives precise stage status, source references and `STATIC`/`MOCK`/`LIVE` evidence labels. It never presents an offline generated object as deployed SAP behavior.

## Accessibility and recovery

Keyboard navigation, semantic labels, visible focus, accessible color contrast, screen-reader status for jobs, persistent filter state. Show retryable vs permanent failures, source rate-limit reset, missing credential, blocked license, host path collision, and rollback path in plain language. No irreversible bulk approve. Provide audit/export as JSON and human-readable reports. A console-only mode supports the same decision actions and role constraints.

## Design artifacts to implement

Component sketches/stories for each screen, API-backed prototypes with empty/loading/error/conflict states, accessibility checks, and usability walkthroughs for reviewer and developer journeys. Visual styling is subordinate to evidence clarity; never hide source provenance behind a confidence number.
