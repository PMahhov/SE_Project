import shlex
import sys

from invoke import task


@task
def bootstrap(ctx, python="3.10.4"):
    """Install required conda packages."""

    def ensure_packages(*packages):
        clean_packages = sorted({shlex.quote(package) for package in sorted(packages)})
        ctx.run(
            "conda install --quiet --yes " + " ".join(clean_packages),
            pty=sys.platform != "win32",
            echo=True,
        )

    def ensure_from_channel(*packages):
        for package in packages:
            ctx.run(f"conda install --quiet --yes -c {' '.join(package.split())}")

    def ensure_pip(*packages):
        for package in packages:
            ctx.run(f"pip3 install {package}")

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
    run_packages = meta_yaml["requirements"]["run"]
    channel_packages = meta_yaml["requirements"]["channel"]
    pip_packages = meta_yaml["requirements"]["pip"]

    ensure_packages(*develop_packages, *run_packages)
    ensure_from_channel(*channel_packages)
    ensure_pip(*pip_packages)


@task
def test(ctx,):
    """Run tests."""
    args = []
    ctx.run("pytest tests/setup_test.py tests " + " ".join(args), pty=True, echo=True)


@task
def check(ctx, style=True, typing=True):
    """Check for style and static typing errors."""
    paths = ["tests", "source"]
    if style:
        ctx.run("flake8 " + " ".join(paths), echo=True)
        ctx.run("isort --diff --check-only " + " ".join(paths), echo=True)
        ctx.run("black --diff --check " + " ".join(paths), echo=True)
    if typing:
        ctx.run(f"mypy --no-incremental --cache-dir=/dev/null {paths}", echo=True)


@task
def format_(ctx):
    """Format code to use standard style guidelines."""
    paths = ["tests", "source"]
    autoflake = "autoflake -i --recursive --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables"
    ctx.run(f"{autoflake} " + " ".join(paths), echo=True)
    ctx.run("isort " + " ".join(paths), echo=True)
    ctx.run("black --line-length 100" + " ".join(paths), echo=True)
