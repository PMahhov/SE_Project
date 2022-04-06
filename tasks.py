import shlex
import sys

from invoke import task


@task(help={"python": "Set the python version (default: current version)"})
def bootstrap(ctx, python="3.10.2"):
    """Install required conda packages."""

    def ensure_packages(*packages):
        clean_packages = sorted({shlex.quote(package) for package in sorted(packages)})
        ctx.run(
            "conda install --quiet --yes " + " ".join(clean_packages),
            pty=sys.platform != "win32",
            echo=True,
        )

    try:
        import jinja2
        import yaml
    except ModuleNotFoundError:
        ensure_packages("jinja2", "pyyaml")
        import jinja2
        import yaml

    with open("meta.yaml") as file:
        template = jinja2.Template(file.read())

    meta_yaml = yaml.safe_load(
        template.render(load_setup_py_data=lambda: {}, python=python)
    )
    develop_packages = meta_yaml["requirements"]["develop"]
    build_packages = meta_yaml["requirements"]["build"]
    run_packages = meta_yaml["requirements"]["run"]

    ensure_packages(*develop_packages, *build_packages, *run_packages)


@task(
    incrementable=["verbose"],
    help={
        "behavioral": "Run behavioral tests too (default: False)",
        "performance": "Run performance tests too (default: False)",
        "external": "Run external tests too (default: False)",
        "x": "Exit instantly on first error or failed test (default: False)",
        "junit-xml": "Create junit-xml style report (default: False)",
        "failed-first": "run all tests but run the last failures first (default: False)",
        "quiet": "Decrease verbosity",
        "verbose": "Increase verbosity (can be repeated)",
    },
)
def test(
    ctx,
    behavioral=False,
    performance=False,
    external=False,
    x=False,
    junit_xml=False,
    failed_first=False,
    quiet=False,
    verbose=0,
):
    """Run tests."""
    markers = []
    if not behavioral:
        markers.append("not behavioral")
    if not performance:
        markers.append("not performance")
    if not external:
        markers.append("not external")
    args = []
    if markers:
        args.append("-m '" + " and ".join(markers) + "'")
    if not behavioral and not performance and not external:
        args.append(f"--cov={PACKAGE}")
        args.append(f"--cov-fail-under={REQUIRED_COVERAGE}")
    if x:
        args.append("-x")
    if junit_xml:
        args.append("--junit-xml=junit.xml")
    if failed_first:
        args.append("--failed-first")
    if quiet:
        verbose -= 1
    if verbose < 0:
        args.append("--quiet")
    if verbose > 0:
        args.append("-" + ("v" * verbose))
    ctx.run("pytest tests " + " ".join(args), pty=True, echo=True)


@task(
    help={
        "style": "Check style with flake8, isort, and black",
        "typing": "Check typing with mypy",
    }
)
def check(ctx, style=True, typing=False):
    """Check for style and static typing errors."""
    paths = ["tasks.py", "source"]
    # if Path("tests").is_dir():
    #     paths.append("tests")
    if style:
        ctx.run("flake8 " + " ".join(paths), echo=True)
        ctx.run("isort --diff --check-only " + " ".join(paths), echo=True)
        ctx.run("black --diff --check " + " ".join(paths), echo=True)
    # if typing:
    #     ctx.run(f"mypy --no-incremental --cache-dir=/dev/null {PACKAGE}", echo=True)


@task(name="format", aliases=["fmt"])
def format_(ctx):
    """Format code to use standard style guidelines."""
    # paths = ["setup.py", "tasks.py", PACKAGE]
    paths = ["tasks.py", "source"]
    # if Path("tests").is_dir():
    #     paths.append("tests")
    autoflake = "autoflake -i --recursive --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables"
    ctx.run(f"{autoflake} " + " ".join(paths), echo=True)
    ctx.run("isort " + " ".join(paths), echo=True)
    ctx.run("black " + " ".join(paths), echo=True)
