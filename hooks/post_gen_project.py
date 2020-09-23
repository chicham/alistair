#!/usr/bin/env python

import os
import subprocess
import warnings
from distutils import spawn

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


def command_exists(cmd):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if spawn.find_executable(cmd.strip()):
                return f(*args, **kwargs)
            else:
                warnings.warn(f"Command {cmd} not found")

        return wrapper

    return decorator


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


@command_exists("conda")
def create_conda():
    subprocess.run(
        [
            "conda",
            "create",
            "-y",
            "-n",
            "{{ cookiecutter.project_slug }}",
            "python={{ cookiecutter.pyver }}",
        ],
        check=True,
    )


@command_exists("python{{ cookiecutter.pyver}}")
def create_venv():
    warnings.warn(
        f"Creating venv at {PROJECT_DIRECTORY}/.{{ cookiecutter.project_slug }}",
    )
    subprocess.run(
        [
            "python{{ cookiecutter.pyver }}",
            "-m",
            "venv",
            ".{{ cookiecutter.project_slug }}",
        ],
        check=True,
    )


@command_exists("pyenv")
def create_pyenv():
    warnings.warn("")
    subprocess.run(
        [
            "pyenv",
            "virtualenv",
            "{{ cookiecutter.pyver }}",
            "{{ cookiecutter.project_slug }}.{{ cookiecutter.pyver }}",
        ],
        check=True,
    )


@command_exists("git")
@subprocess_error("Could not initialize git repository")
def init_git():
    subprocess.run(["git", "init", "."], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(
        ["git", "remote", "add", "origin", "{{ cookiecutter.project_remote }}"],
        check=True,
    )
    subprocess.run(
        [
            "git",
            "remote",
            "set-url",
            "--push",
            "origin",
            "{{ cookiecutter.project_remote }}",
        ],
        check=True,
    )

    subprocess.run(
        [
            "git",
            "remote",
            "set-url",
            "--push",
            "origin",
            "{{ cookiecutter.project_remote }}",
        ],
        check=True,
    )


@command_exists("direnv")
def direnv_allow():
    subprocess.run(["direnv", "allow"], check=True)


@command_exists("pre-commit")
def pre_commit_install():
    subprocess.run(
        "pre-commit",
        "install",
        "--install-hooks",
        "--overwrite",
        check=True,
    )


if __name__ == "__main__":

    if "{{ cookiecutter.create_author_file }}" != "y":
        remove_file("AUTHORS.rst")
        # remove_file("docs/authors.rst")

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")

    init_git()

    venv = "{{ cookiecutter.virtual_env }}"

    if venv == "anaconda":
        create_conda()
    elif venv == "venv":
        create_venv()
    else:
        pass
    if "{{ cookiecutter.use_direnv }}" == "y":
        direnv_allow()
    else:
        subprocess.run(["rm", "-f", ".envrc"], check=True)
