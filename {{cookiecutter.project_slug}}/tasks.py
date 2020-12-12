from pathlib import Path

from invoke import task


def update_requirement(ctx, in_path: Path = None, out_path: Path = None, upgrade=True):
    if out_path is None:
        if in_path is None:
            raise ValueError("in_path and out_path can't be `None` at the same time")
        out_path = f"{in_path.parent / in_path.stem}.txt"
    args = ["pip-compile"]
    if upgrade:
        args.append("--upgrade")
    if out_path:
        args.append(f"--output-file={out_path}")

    if in_path:
        args.append(f"{in_path}")

    ctx.run(" ".join(args), pty=True)


@task
def deps(ctx):
    current_path = Path(__file__).absolute().parent
    requirements_path = current_path / "requirements"
    update_requirement(ctx, out_path="requirements.txt")
    update_requirement(ctx, in_path=requirements_path / "dev.in")
    update_requirement(ctx, in_path=requirements_path / "docs.in")
    update_requirement(ctx, in_path=requirements_path / "tests.in")


@task
def doc(ctx, target="html"):
    ctx.run(
        "rm -f docs/{{ cookiecutter.project_slug }}.rst && rm -f docs/modules.rst",
        pty=True,
    )
    ctx.run(f"cd docs/ && make {target}", pty=True)


@task
def install(ctx, editable=False, extra=None):
    """
    Extra is one of [all, dev, tests, docs]
    """
    cmd = ["pip", "install"]
    if editable:
        cmd.append("-e")

    if extra:
        cmd.append(f".[{extra}]")
    else:
        cmd.append(".")

    ctx.run(" ".join(cmd), pty=True)


@task
def lint(ctx):
    ctx.run("pre-commit run --all-files", pty=True)


@task
def clean(ctx):
    ctx.run("rm -rf build/ dist/ .eggs/")
    ctx.run("find . -name '*.egg-info' -exec rm -fr {} +")
    ctx.run("find . -name '*.egg' -exec rm -f {} +")
    ctx.run("find . -name '*.pyc' -exec rm -f {} +")
    ctx.run("find . -name '*.pyo' -exec rm -f {} +")
    ctx.run("find . -name '__pycache__' -exec rm -fr {} +")


@task
def test(ctx):
    ctx.run("pytest", pty=True)
