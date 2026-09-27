# GitHub CI/CD operations

Repository: https://github.com/ClaudiousAI/SuperSAPDEV

## Continuous integration — TASK-001

`ci.yml` runs on branch pushes, pull requests and manual dispatch. It calls
`checks.yml` at the same commit. All nine combinations of Windows/macOS/Linux
and Python 3.12/3.13/3.14 must pass locked installation, Ruff lint/format, strict
mypy, pytest, smoke, reproducible wheel/sdist builds, sdist reconstruction and
clean-wheel installation. The stable branch-protection status is **CI required**;
it fails if any prerequisite fails or is cancelled. New commits cancel obsolete
CI runs on the same branch/PR.

Every matrix cell retains JUnit results for 14 days, including on test failure.
Linux/Python 3.12 retains `verified-candidate` for 14 days: the exact tested wheel
and sdist, hash-locked runtime `requirements.txt`, review limitations and
`SHA256SUMS`. Uploaded candidates are not approved releases. Checks use read-only
repository permission and no personal token. Actions and uv are pinned;
Dependabot proposes weekly action updates.

## Manual draft delivery — TASK-022 foundation only

In GitHub **Actions → Prepare draft delivery → Run workflow**, select `main`.
Other branches cannot prepare drafts. All nine checks rerun against the dispatch
commit. Only after success does an isolated job download that run's verified
candidate, check SHA-256 sums and create an **unpublished draft prerelease**.
It executes no repository code and uses the run-scoped `GITHUB_TOKEN`, with
`contents: write` only in this job. No PAT secret is needed in GitHub Actions.

The candidate tag contains source SHA, run ID and attempt. Draft notes record
the full source SHA and evidence URL. Reruns create a new candidate instead of
overwriting evidence. Inspect the draft in **Releases** while signed in with
repository write access. Download assets and verify on Linux/macOS:

```console
sha256sum --check --strict SHA256SUMS
```

On PowerShell, compare each listed digest using `Get-FileHash -Algorithm SHA256`.
Checksums detect byte changes; they are not signatures or provenance attestations.
Artifacts may be available from a failed overall run when another matrix cell
fails; only a successful complete delivery run may create a draft.

Do not publish a draft as a product release. TASK-022 still requires its upstream
tasks, reviewed domain packs, native host conformance, SBOM/signatures, immutable
product manifest, independent release approval and rollback/revocation.
The project currently implements a Python CLI foundation, not a deployable web
service. No PyPI, cloud, skill-store or SAP deployment is configured.

## Repository setup and recovery

Actions must be enabled and allow pinned official `actions/*` actions. Protect
`main` with **CI required**, strict up-to-date checks, and force pushes/deletion
disabled. Inspect **Settings → Branches**. Workflow definitions alone do not
enforce repository settings; actual setup results are in `evidence/CI-CD.md`.

Inspect failing jobs and JUnit artifacts, reproduce with `DEVELOPMENT.md`, fix on
a branch and rerun CI. A checksum mismatch blocks draft creation. An API failure
leaves the workflow artifact for inspection; rerun after fixing permissions.
Do not bypass checks or replace old assets. A maintainer can delete an incorrect
unpublished draft; published-product rollback remains TASK-022 work.

Local validation uses actionlint 1.7.12 against all three workflow files. To
retain verified local artifacts, choose a new output directory:

```console
uv run --locked python scripts/check_distribution.py --output-dir .local/candidate
```

Sources: [reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows),
[token permissions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication),
[draft release CLI](https://cli.github.com/manual/gh_release_create).
Results are STATIC/MOCK; no LIVE SAP evidence is produced.
