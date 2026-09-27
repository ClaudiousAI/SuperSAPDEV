# Module ownership

Implemented in TASK-001: `cli` (entry point and diagnostics), `contracts` (typed
CLI exits/evidence/report), `smoke` (offline resource/schema check), packaged
`schemas` and `fixtures`. `py.typed` exposes the typed package to consumers.

The following modules will be added with working interfaces in dependency order:

| Modules | Task |
|---|---|
| registry, policy data contracts | TASK-002 |
| connectors, source policy | TASK-003 |
| orchestrator, scheduler | TASK-004 |
| discovery, delta, skill finder | TASK-005–007 |
| extract, verify, curate | TASK-008–010 |
| review_api | TASK-011 |
| compile | TASK-013 |
| workflow | TASK-014 |
| hosts | TASK-015–019 |
| benchmarks | TASK-021 |

No placeholder module implements or claims those capabilities. All 15 domains,
four proposing agents, seven workflow stages, and four native hosts remain in scope.
