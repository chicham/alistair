from invoke import task


@task
def update_requirement(ctx, in_file=None):
    output_file = f"{in_file.parent / in_file.stem}.txt"
    ctx.run(f"pip-compile --upgrade {in_file} --output-file={output_file}")


@task
def update(ctx):
    ctx.run("pip-compile --upgrade --output-file=./requirements/reqs.txt")
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
        cmd.append("-e")

    if extra:
        cmd.append(f".[{extra}]")
    else:
        cmd.append(".")

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
    ctx.run("find . -name '__pycache__' -exec rm -fr {} +")


@task
def test(ctx):
    ctx.run("pytest")
