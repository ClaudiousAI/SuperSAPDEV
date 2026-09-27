# CI/CD implementation evidence — 2026-09-27

Scope: TASK-001 automation and a bounded TASK-022 draft-delivery foundation,
authorized by the user's GitHub CI/CD request. ADR-013 resolves the release
dependency boundary. Full TASK-022 and product acceptance remain incomplete.

## Local verification (STATIC / MOCK)

Windows Python 3.14.7 with locked uv 0.10.12:

- Ruff lint and format pass (8 Python files).
- Strict mypy passes (8 source files).
- pytest: 37 passed in 4.08s, no skips.
- actionlint 1.7.12 accepts all three workflows. Download digest checked against
  the official GitHub release asset SHA-256. Local ShellCheck is unavailable;
  `-shellcheck=` disables that optional integration only.
- Distribution verification passes: two byte-identical wheel/sdist builds,
  reconstruction from sdist, isolated wheel installation, both CLI entry points
  matching the synthetic golden twice, packaged typing marker present.
- Candidate export retains verified bytes, requirements, review limitations and
  SHA-256 sums; it refuses an existing output directory.

Commands use the development guide's local uv prefix with explicit Python 3.14:

```console
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv run --locked pytest -q
uv run --locked python scripts/check_distribution.py --uv .tools/bin/uv.exe --output-dir .local/cicd-candidate
actionlint -shellcheck= .github/workflows/ci.yml .github/workflows/checks.yml .github/workflows/delivery.yml
```

One initial Ruff line-length/format issue was corrected with the formatter and
the full lint/format/type checks rerun successfully. The workflow validator
reported no errors.

The sandbox denied one overwrite-refusal invocation; repeating the identical
check with approved execution returned the expected exit 2 without changing
the existing candidate. Independent `Get-FileHash` checks matched all four
entries in `SHA256SUMS`.

## GitHub execution

Before setup, the public repository existed with no refs or commits. The local
workspace had no Git metadata. Initialized `main`, configured a credential-free
HTTPS origin and pushed 51 source files after a staged secret scan. The supplied
credential was used only through process memory, never stored in project files,
Git remote URLs or workflow secrets.

Source commit: `43a88110ebaa26647dd7506b56148fa6abf4f9fe`.
[CI run 36296468996](https://github.com/ClaudiousAI/SuperSAPDEV/actions/runs/36296468996):
all nine OS/Python matrix jobs and **CI required** passed on GitHub-hosted runners. This covers
Windows/macOS/Linux × Python 3.12/3.13/3.14, with all required steps enabled.
These are STATIC/MOCK executions, not SAP or coding-agent host conformance.

[Manual delivery run 36296503951](https://github.com/ClaudiousAI/SuperSAPDEV/actions/runs/36296503951)
passed all nine matrix jobs and the draft job for the same source commit.
GitHub reports ten retained artifacts: nine JUnit bundles and the verified
candidate. Authenticated inspection confirms `draft: true`, `prerelease: true`
and five attached assets (wheel, sdist, requirements, REVIEW.md, SHA256SUMS).
Candidate tag: `candidate-43a88110ebaa-36296503951-1`.
[Unpublished draft](https://github.com/ClaudiousAI/SuperSAPDEV/releases/tag/untagged-0760765baf1ee51f0f32)
requires repository write access to view. Delivery verifies checksums before
creating it and records the source commit and successful run in its notes.

Repository protection configuration is applied after the evidence commit is
pushed: `main` requires **CI required**, strict up-to-date checks, enforcement
for administrators, and no force pushes or deletions. Check the repository's
branch settings for the current server-side state; these controls are not
implemented by YAML alone. No production environment or publishing secret exists.

No harvested content, package release or SAP change has been published. There
is no LIVE SAP evidence. Current pipeline artifacts contain development tooling
and synthetic fixtures, not approved domain packs or host skill bundles.
