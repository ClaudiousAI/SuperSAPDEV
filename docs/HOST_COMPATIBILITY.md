# Native host adapters and installation

| Host | Project skill location | Native invocation and adapter notes |
|---|---|---|
| Claude Code | `.claude/skills/super-sap-dev/SKILL.md` | `/super-sap-dev`; allow host discovery/automatic matching where supported, with focused frontmatter and references. |
| Codex | `.agents/skills/super-sap-dev/SKILL.md` | `$super-sap-dev`; preserve repo skill discovery and concise entrypoint. |
| OpenCode | `.opencode/skills/super-sap-dev/SKILL.md` | Host-native `skill` tool loads skill by name; do not assume slash-command parity. |
| DeepSeek Harness | `.dsh/skills/super-sap-dev/SKILL.md` | `/super-sap-dev` with filesystem provider; developer-preview host, pin tested version and disable unverified capabilities. |

The table specifies target project layout based on currently documented host behavior; implementer must verify and record supported host versions. User-scope destinations are discovered from official host configuration and validated in integration tests, not guessed. Native install copies an approved bundle plus manifest and references; duplicate skill names or existing unmanaged directories require conflict resolution.

## Installer protocol

`supersap install --host claude|codex|opencode|deepseek --scope project|user --version X [--dry-run]` determines target and performs preflight (supported host/version, writable path, manifest/hash, existing install, path traversal/symlink safety). Display a diff and backup location, write to a temporary sibling, fsync/atomic rename where available, and record installation metadata. Idempotent reinstall of the same hash is a no-op. Upgrade verifies ownership and backs up previous bundle; failure rolls back. `doctor` checks host discovery and versions, content hashes, missing references and invocation. `uninstall` removes only owned files and restores backed-up unmanaged files when applicable. Support Windows CMD/PowerShell paths and line endings.

## Conformance matrix

For every supported host/version/OS: install, doctor, native discovery, explicit invocation, progressive loading, domain routing, workflow artifacts, deterministic CLI gate invocation, error handling, upgrade, rollback, and uninstall. Evaluate equivalent SAP scenarios and compare artifact semantics, not exact prose. Record host tool restrictions and fallback instructions. DeepSeek Harness preview changes require retest before claiming support. Do not claim automatic skill invocation for a host unless a native test demonstrates it.
