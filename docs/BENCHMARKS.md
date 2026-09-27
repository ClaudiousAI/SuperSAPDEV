# Benchmarks and quality metrics

## Corpus construction

Maintain expert-authored scenarios for each D01–D15 pack and cross-domain paths. Each case pins landscape/edition/release, user requirement, allowed source snapshot, expected decision points, rejected anti-patterns, security/privacy constraints, required artifact schemas, and evidence label. Include straightforward, ambiguous, adversarial, outdated-source and no-answer cases. Keep hidden evaluation cases separate from agent prompts to reduce overfitting.

## Metrics

| Metric | Calculation and target gate |
|---|---|
| Citation traceability | Approved normative statements with valid source revision/span and applicability ÷ all normative statements; target 100%. |
| Domain coverage | Mandatory concept/evidence cells satisfied or approved exception ÷ all mandatory cells; target 100% for a releasable pack. |
| Unsafe guidance | Critical prohibited recommendations per golden corpus; target zero. |
| Decision quality | Expert rubric for standard-vs-custom, released API, auth, tests, tradeoffs; baseline and release threshold approved by reviewers per corpus version. |
| Workflow adherence | Required artifacts/gates satisfied in valid scenarios, and correctly blocked in invalid scenarios; target 100% for deterministic gates. |
| Delta recovery | Synthetic changes detected after partial failure/outage; target 100% including >30-day backfill. |
| Host conformance | Native install/invocation/artifact checks passing ÷ supported host/OS/version cases; target 100%. |
| Reproducibility | Same pinned inputs yielding same manifest/file hashes; target 100%. |

Report per-domain results, confidence intervals where sample sizes warrant, case counts, regression diffs, model/provider and prompt version, host version, snapshot/policy version, run time/cost, and failure traces. Do not hide weak domains behind aggregate averages. Human expert adjudication resolves ambiguous answer rubrics. Tune thresholds before a release candidate and record changes in a decision entry; never lower a gate silently to pass CI.

## Operational monitoring

Track scan lag, cursor gap, source error rates, token/cost budget, queue age, reviewer throughput, stale approved item count, revocation response time, installer failure rate (opt-in local aggregation only), and benchmark drift. Alerts route to maintainers; no customer project content is needed.
