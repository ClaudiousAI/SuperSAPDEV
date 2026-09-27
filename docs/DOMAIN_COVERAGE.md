# SAP domain pack coverage contract

All 15 packs below are required for the full product. Each pack declares edition/release support; concept taxonomy; official sources and revisions; patterns, anti-patterns and tests; cross-pack dependencies; benchmark scenarios; and reviewed gaps. A domain is releasable when every mandatory concept has authoritative evidence or an explicit, approved unsupported designation, no blocking conflict, and passing scenario tests. Counts of repositories are diagnostic only; evidence quality, diversity and saturation determine coverage.

| ID | Pack | Mandatory concept families and validation scenarios |
|---|---|---|
| D01 | Modern/Core ABAP | Expressions, internal tables, Open SQL, typing, exceptions, performance, released language features; release-sensitive syntax and SQL scenario. |
| D02 | OO ABAP | Interfaces, classes, dependency injection, testability, exception contracts, inheritance/composition; refactoring scenario. |
| D03 | ABAP Cloud / Clean Core | Language version, released APIs, extensibility levels, upgrade-safe boundaries, forbidden dependencies; cloud-versus-on-premise decision scenario. |
| D04 | CDS | View entities, associations, annotations, access control, analytical modeling, performance; authorization and model evolution scenario. |
| D05 | RAP | Behavior definition/implementation, managed/unmanaged, draft, determinations, validations, EML, authorization; transactional lifecycle scenario. |
| D06 | OData | Service definition/binding, protocol versions, metadata, paging, errors, authorization, contract evolution; API consumer scenario. |
| D07 | Fiori/UI5 | App patterns, annotations, routing/state, accessibility, localization, security, testing; RAP-to-Fiori scenario. |
| D08 | HANA/AMDP | Pushdown decisions, SQLScript/AMDP applicability, performance, authorization, portability; ABAP-vs-pushdown tradeoff. |
| D09 | Enhancements/BAdIs | Released extension points, filter/implementation lifecycle, clean-core classification, upgrade impact; standard-vs-custom choice. |
| D10 | IDoc/Interfaces | IDoc structures/status/error handling, integration patterns, retries/idempotency, security, interface monitoring; failure recovery scenario. |
| D11 | CAP (Node/Java) | CDS model, services, authorization, events, persistence, deployment boundaries, Node/Java differences; BTP extension scenario. |
| D12 | BTP | Subaccounts, destinations, connectivity, identity, service bindings, deployment topology, tenant/security concerns; integration design scenario. |
| D13 | ECC→S/4 modernization | Simplification analysis, obsolete APIs, data model change, custom code adaptation, compatibility; migration assessment scenario. |
| D14 | Testing/ATC | ABAP Unit, test doubles, ATC checks, static/CI evidence, quality gates, test isolation; offline vs connected validation scenario. |
| D15 | AI+ABAP | AI service integration boundaries, prompt/data safety, authorization, cost, evaluation, deterministic fallback; privacy-preserving integration scenario. |

## Cross-pack graph

D03 applies Clean Core constraints across ABAP, CDS, RAP, enhancements, and modernization. D04→D05→D06→D07 covers data to UX, with authorization at every boundary. D10/D11/D12 cover interfaces and extensions; D14 applies test evidence throughout; D15 inherits security/privacy and BTP integration constraints. Packs must refer to other packs by pinned version rather than duplicate rules; conflicts block the release.

## Coverage scoring and research policy

For each concept, track official normative support, maintained sample, independent corroboration, anti-pattern, release applicability, negative test, benchmark. Begin with a diverse candidate pool, expand until new sources yield negligible new concepts across two review cycles, and keep a reviewer-approved coverage exception for genuinely unavailable evidence. Never invent a precise minimum repo quota. Knowledge items must use consistent types (`RULE`, `PATTERN`, `EXAMPLE`, `ANTI_PATTERN`, `API_FACT`, `VERSION_FACT`, `TEST_PATTERN`) and cite revisioned evidence. A static example does not prove live runtime behavior.
