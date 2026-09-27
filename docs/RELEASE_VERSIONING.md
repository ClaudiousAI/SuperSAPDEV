# Versioning, CI and distribution

The current [CI/CD implementation](CI_CD.md) prepares unpublished development
drafts only (ADR-013). The full product release gates below remain mandatory;
TASK-022 is not complete.

## Independent versions

`skill_version` uses SemVer for user-visible behavior. `knowledge_snapshot_id` is immutable content-addressed pack composition. `policy_version`, `core_version`, `adapter_versions` (per host), `schema_version`, `benchmark_corpus_version`, and build toolchain are separate manifest fields. A content refresh may change the knowledge snapshot without altering workflow semantics; a host adapter fix need not rewrite SAP facts. Any compatibility break increments the relevant major version and includes migration guidance.

## Release pipeline

1. PR changes source/knowledge/core/adapter with task IDs, evidence, license status, applicability and tests.
2. CI validates schemas, all 15 pack gates, deterministic build, host conformance, adversarial tests, benchmark regression, dependency/SBOM and manifest hashes.
3. Reviewer resolves content conflicts and approves each promotion; independent release approver examines diff and signs immutable manifest.
4. Publish versioned bundles, checksums/signature, changelog, support matrix, installation instructions, benchmark report and provenance index. Git tag references exact manifest.
5. Verify a clean install on each host. Monitor post-release source deltas and regressions. Rollback changes distribution pointer to a known good manifest; never mutate existing version bytes.

`publish` rejects missing approvals, stale critical source events, expired host conformance, mismatched hash, or failing quality gate. Revocation records reason and affected versions; clients show warning and safe replacement. Pin source commit/document revision to permit reproduction even when upstream moves. Keep secrets and raw restricted source text out of release artifacts.

## Compatibility policy

Maintain a tested support matrix with host version, OS, adapter version, native trigger, and capability gaps. DeepSeek Harness developer-preview support is explicitly labeled and pin-tested. An unsupported host version is not silently treated as supported. Installer upgrades compare manifest compatibility and preserve backup/rollback.
