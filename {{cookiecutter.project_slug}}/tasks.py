from invoke import task
from pathlib import Path


@task
def update_requirement(ctx, in_file=None):
    in_path = Path(in_file)
    output_file = f"{in_path.parent / in_path.stem}.txt"
    ctx.run(f"pip-compile --upgrade {in_file} --output-file={output_file}", pty=True)


@task
def update(ctx):
    ctx.run("pip-compile --upgrade --output-file=./requirements/reqs.txt", pty=True)
    update_requirement(ctx, "./requirements/dev.in")
    update_requirement(ctx, "./requirements/docs.in")
    update_requirement(ctx, "./requirements/tests.in")


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
