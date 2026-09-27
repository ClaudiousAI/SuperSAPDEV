# Schema catalog

TASK-001 introduces JSON Schema Draft 2020-12 for synthetic workspace fixtures.
The canonical [smoke schema](../src/supersap/schemas/smoke.schema.json) lives in
the Python package so wheel installs can validate offline from any directory.
Do not maintain a second copy here. Schema IDs are identifiers, never fetch URLs.

The schema requires MOCK evidence and rejects extra fields. It does not validate
knowledge, sources, approvals, or releases. Their versioned schemas and lifecycle
contracts are TASK-002 and subsequent work. Unknown versions fail closed.
