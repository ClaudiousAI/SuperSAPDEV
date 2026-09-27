# Security and privacy specification

## Trust boundaries and threats

External documents, repositories, skill manifests, and model responses are untrusted. Treat embedded instructions as quoted data; never allow source text to alter system prompts, tool permissions, policy or reviewer identity. Separate quarantined fetch cache from approved knowledge, local customer repositories from the global registry, and generated host skill content from executable installer code. Threats include prompt injection, dependency confusion, malicious install scripts, source poisoning, license laundering, model hallucination, stale/deprecated SAP advice, secret exfiltration, review spoofing, and compromised releases.

## Required controls

| Area | Control and verification |
|---|---|
| Connectors | Allowlisted schemes/domains or explicit reviewed source registration, read-only tokens, HTTP timeouts/size limits, SSRF/IP restrictions, sandboxed parsing, no arbitrary script execution. |
| Credentials | OS secret store or environment, least privilege, rotate/revoke, never log/echo; redact paths/tokens from diagnostics. No `.env` commits. |
| Models | Send minimal licensed/allowed excerpts; no customer source by default; structured outputs validated as data; token/output budgets and provider retention policy review. |
| Knowledge | Source version and license gates, authoritative corroboration, conflict checks, reviewer separation, provenance graph, recheck on source change. |
| Skill finder | Quarantine candidate instructions, prohibit auto-execution/installation/merge, static scan for exfiltration and tool misuse. |
| Installer | Release hashes/signature verification, path normalization, symlink/path-traversal defense, atomic rollback, no privilege escalation. |
| Dashboard/API | Loopback default; team auth/RBAC, CSRF and session hardening, audit decisions, optimistic concurrency, encrypted transport for remote use. |
| Runtime | No live SAP write capability in base product; local CLI validates artifacts, but host tool execution obeys host/user permissions. Never claim the prompt alone enforces a security boundary. |
| Supply chain | Pinned dependencies, dependency/scanner checks, SBOM, CI provenance, protected release approvals, revocation process. |

## Roles and approval

Operator registers sources and schedules jobs; reviewer approves knowledge with rationale; release maintainer prepares artifacts; independent approver signs release; developer consumes packages. Team mode enforces separation of approval duties. Single-user mode records identity and explicit approval and discloses reduced separation. Neither an agent nor a model may grant itself a role. All state changes have append-only audit events.

## Data handling

Do not harvest customer systems, private repositories, credentials, proprietary ABAP code or personal data into shared packs. Explicit feedback submission requires scrub, license check and reviewer action. Classify source cache and audit retention; provide deletion/revocation workflows without breaking manifest traceability. Store hashes or redacted metadata if content retention is prohibited. Telemetry is off by default. Review source terms before crawling, caching, or redistributing excerpts.

## Incident response

On malicious source, invalid license, compromised dependency or faulty SAP rule: stop relevant ingestion/release, mark dependents `RECHECK_REQUIRED`, quarantine artifacts, revoke affected release manifest, publish impact notice and safe rollback, rotate exposed secrets, preserve redacted audit, and add regression cases. Drill this procedure before production release.
