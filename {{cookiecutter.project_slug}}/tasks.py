from pathlib import Path

from invoke import task


@task
def update_requirement(ctx, in_file=None):
    in_file = Path(in_file)
    output_file = Path(f"{in_file.parent / in_file.stem}.txt")
    ctx.run(f"pip-compile --upgrade {str(in_file)} --output-file={str(output_file)}")


@task
def update(ctx):
    update_requirement(ctx, "./requirements/reqs.in")
    update_requirement(ctx, "./requirements/dev.in")
    update_requirement(ctx, "./requirements/docs.in")
    update_requirement(ctx, "./requirements/tests.in")


@task
def doc(ctx):
    ctx.run("rm -f docs/{{ cookiecutter.project_slug }}.rst")
    ctx.run("rm -f docs/modules.rst")
    ctx.run("sphinx-apidoc -o docs/{{ cookiecutter.project_slug }}")


@task
def install(ctx, editable=False, extra=None):
    """
    Extra is one of [all, dev, tests, docs]
    """
    cmd = ["pip", "install"]
    if editable:
        cmd += "-e"

    if extra:
        cmd += f".[{extra}]"
    else:
        cmd += "."

    ctx.run(" ".join(cmd))


@task
def lint(ctx):
    ctx.run("pre-commit run --all-files")


@task
def clean(ctx):
    ctx.run("rm -rf build/ dist/ .eggs/")
    ctx.run("find . -name '*.egg-info' -exec rm -fr {} +")
    ctx.run("find . -name '*.egg' -exec rm -f {} +")
    ctx.run("find . -name '*.pyc' -exec rm -f {} +")
    ctx.run("find . -name '*.pyo' -exec rm -f {} +")
    ctx.run("find . -name '*~' -exec rm -f {} +")
    ctx.run("find . -name '__pycache__' -exec rm -fr {} +")
    ctx.run("rm -fr .tox/")
    ctx.run("rm -f .coverage")
    ctx.run("rm -fr htmlcov/")
    ctx.run("rm -fr .pytest_cache")


@task
def test(ctx):
    ctx.run("pytest")
