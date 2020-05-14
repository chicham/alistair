#!/usr/bin/env python
import os
import subprocess
import warnings
import ast

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def subprocess_error(msg):
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except subprocess.CalledProcessError as e:
                warnings.warn(f"{msg}: {e}")

        return wrapper

    return decorator


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


@subprocess_error("Could not initialize git repository")
def init_git():
    subprocess.run(["git", "init", "."])
    subprocess.run(["git", "add", "."])
    subprocess.run(
        ["git", "remote", "add", "origin", "{{ cookiecutter.project_remote }}"]
    )
    subprocess.run(
        [
            "git",
            "remote",
            "set-url",
            "--push",
            "origin",
            "{{ cookiecutter.project_remote }}",
        ]
    )


@subprocess_error("Could not install the module {{ cookiecutter.project_slug }}")
def install():
    direnv_layout = "{{ cookiecutter.direnv_layout }}"

    def run_pip(pip, pip_compile):
        subprocess.run([pip] + ["install", "pip-tools", "pre-commit", "wheel", "setuptools-scm"])

        for req in ("dev", "docs", "tests"):
            subprocess.run([pip_compile] + [f"requirements/{req}.in"])
        subprocess.run([pip] + ["install", "-e", ".[all]"])

    if direnv_layout == "virtualenv":
        prefix = ".direnv/python{{ cookiecutter.pyver }}/bin/"
        pip = "/".join([prefix, "pip"])
        pip_compile = "/".join([prefix, "pip-compile"])
        run_pip(pip, pip_compile)
    elif direnv_layout == "conda":
        pip = ["conda", "run", "-n", "{{ cookiecutter.project_slug }}", "pip"]
        pip_compile = ["conda", "run", "-n", "{{ cookiecutter.project_slug }}", "pip-compile"]
        run_pip(pip, pip_compile)
    else:
        raise RuntimeError(f"Environment {direnv_layout} is not recognized")


@subprocess_error("Could not initialize pre-commit")
def pre_commit():
    subprocess.run(["pre-commit", "install"])


@subprocess_error("Could not initialize direnv")
def dir_env():
    subprocess.run(["direnv", "allow", "."])
    warnings.warn(
        "If the layouts are not configured, go to "
        "https://github.com/direnv/direnv/wiki/Python"
    )


def create_venv():
    layout = "{{ cookiecutter.direnv_layout }}"
    cmd = None
    if layout == "anaconda":
        cmd = [
            "conda",
            "create",
            "-y",
            "-c conda-forge",
            "-n",
            "{{ cookiecutter.project_slug }}",
            "python={{ cookiecutter.pyver }}",
        ]
    elif layout == "virtualenv":
        cmd = [
            "python{{ cookiecutter.pyver }}","-m", "venv", ".direnv/python{{ cookiecutter.pyver }}"
        ]
    else:
        pass

    if cmd:
        subprocess.run(cmd)


if __name__ == "__main__":

    if "{{ cookiecutter.create_author_file }}" != "y":
        remove_file("AUTHORS.rst")
        remove_file("docs/authors.rst")

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")

    create_venv()
    init_git()
    install()
    dir_env()
    pre_commit()
