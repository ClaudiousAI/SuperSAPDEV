# Synthetic evidence

All fixtures are original, synthetic MOCK data with no SAP claims, customer code,
source credentials, or copied source content. The positive input is bundled at
`src/supersap/fixtures/smoke.json`; `smoke.expected.json` freezes the entire expected
normalized CLI output. `untrusted.json` contains inert adversarial text. Negative
schema, encoding, size, and evidence-label cases are generated in tests.

Updating the golden file requires reviewing the changed fixture/hash and scope;
do not regenerate expected output just to silence a regression.
