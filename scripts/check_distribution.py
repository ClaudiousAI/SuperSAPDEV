"""Build twice, rebuild sdist, install a wheel cleanly, and compare smoke bytes.

Uses only the standard library so it can run independently of the source package.
Temporary environments stay in .local; no install touches the user's agent hosts.
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path) -> str:
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment["UV_CACHE_DIR"] = str(ROOT / ".uv-cache")
    environment["UV_PYTHON_DOWNLOADS"] = "never"
    environment["UV_PYTHON"] = sys.executable
    result = subprocess.run(command, cwd=cwd, env=environment, check=True, capture_output=True)
    if result.stderr:
        print(result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout.decode("utf-8").replace("\r\n", "\n")


def require_equal(actual: object, expected: object, description: str) -> None:
    if actual != expected:
        raise RuntimeError(description)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uv", default="uv", help="uv executable path or PATH command")
    parser.add_argument(
        "--output-dir", type=Path, help="Retain verified candidate in a NEW directory"
    )
    options = parser.parse_args()
    if options.output_dir is not None and options.output_dir.exists():
        parser.error("Candidate directory already exists; choose a new directory.")
    uv = str(Path(options.uv).resolve()) if Path(options.uv).is_file() else options.uv
    (ROOT / ".local").mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="distribution space-", dir=ROOT / ".local") as directory:
        work = Path(directory)
        first, second, rebuilt = work / "first", work / "second", work / "rebuilt"
        for target in (first, second):
            run([uv, "build", "--out-dir", str(target)], ROOT)
        artifacts = sorted(path.name for path in first.iterdir() if path.name != ".gitignore")
        require_equal(len(artifacts), 2, "Expected wheel and source distribution")
        for name in artifacts:
            require_equal(
                (first / name).read_bytes(),
                (second / name).read_bytes(),
                f"Nondeterministic artifact: {name}",
            )
        sdist = next(first.glob("*.tar.gz"))
        run([uv, "build", str(sdist), "--wheel", "--out-dir", str(rebuilt)], ROOT)
        wheel = next(first.glob("*.whl"))
        require_equal(
            wheel.read_bytes(),
            (rebuilt / wheel.name).read_bytes(),
            "Wheel rebuilt from sdist differs",
        )
        requirements = work / "requirements.txt"
        run(
            [
                uv,
                "export",
                "--locked",
                "--no-dev",
                "--no-emit-project",
                "--output-file",
                str(requirements),
            ],
            ROOT,
        )
        environment = work / "clean environment"
        run([uv, "venv", "--python", sys.executable, str(environment)], ROOT)
        scripts = environment / ("Scripts" if sys.platform == "win32" else "bin")
        python = scripts / ("python.exe" if sys.platform == "win32" else "python")
        run(
            [
                uv,
                "pip",
                "install",
                "--python",
                str(python),
                "--require-hashes",
                "-r",
                str(requirements),
            ],
            ROOT,
        )
        run([uv, "pip", "install", "--python", str(python), "--no-deps", str(wheel)], ROOT)
        executable = scripts / ("supersap.exe" if sys.platform == "win32" else "supersap")
        expected = (ROOT / "tests/fixtures/smoke.expected.json").read_text("utf-8")
        for command in (
            [str(python), "-I", "-m", "supersap", "--json", "smoke"],
            [str(executable), "smoke", "--json"],
        ):
            for _ in range(2):
                result = run(command, work)
                require_equal(result, expected, "Installed smoke differs from golden")
        run(
            [
                str(python),
                "-I",
                "-c",
                "from importlib.resources import files; "
                "assert files('supersap').joinpath('py.typed').is_file()",
            ],
            work,
        )
        print(
            f"STATIC reproducible wheel SHA-256: {hashlib.sha256(wheel.read_bytes()).hexdigest()}"
        )
        print("MOCK clean wheel install: both entry points match golden on repeated runs.")
        if options.output_dir is not None:
            output = options.output_dir
            output.mkdir(parents=True, exist_ok=False)
            for source in (wheel, sdist, requirements):
                shutil.copyfile(source, output / source.name)
            version = tomllib.loads((ROOT / "pyproject.toml").read_text("utf-8"))["project"][
                "version"
            ]
            (output / "REVIEW.md").write_text(
                f"# Development candidate {version}\n\n"
                "Unapproved development package; not a released SAP skill.\n\n"
                "STATIC: reproducible wheel/sdist, wheel reconstructed from sdist, "
                "hash-locked runtime dependencies.\n"
                "MOCK: clean wheel installation and repeated synthetic CLI checks.\n"
                "No LIVE SAP evidence or native coding-agent host certification.\n\n"
                "Human release review and TASK-022 dependencies remain required. "
                "Do not publish this draft as a product release.\n",
                encoding="utf-8",
                newline="\n",
            )
            checksums = "".join(
                f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
                for path in sorted(output.iterdir())
            )
            (output / "SHA256SUMS").write_text(checksums, encoding="utf-8", newline="\n")
            print("STATIC verified candidate retained with SHA256SUMS; not published.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(error.stderr.decode("utf-8", errors="replace"), file=sys.stderr)
        raise SystemExit(error.returncode) from None
