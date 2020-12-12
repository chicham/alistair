#!/usr/bin/env python

import os
import subprocess
import warnings
from distutils import spawn

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
SETUP_DEPENDENCIES = ["pip-tools", "invoke", "pre-commit"]


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


def run(cmd):
    return subprocess.run(cmd, check=True)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def update_requirements(in_reqs=None):
    args = [
        "piptools",
        "compile",
    ]
    if in_reqs is None:
        args.append("--output-file=requirements.txt")
    else:
        out_txt = f"{in_reqs}.txt"
        args.append(f"--output-file=requirements/{out_txt}")
        args.append(f"requirements/{in_reqs}.in")

    return args


@command_exists("conda")
def create_conda():
    create_cmd = [
        "conda",
        "create",
        "-y",
        "-n",
        "{{ cookiecutter.project_slug }}",
        "python={{ cookiecutter.pyver }}",
    ]
    run(create_cmd)
    prefix = [
        "conda",
        "run",
        "-n",
        "{{ cookiecutter.project_slug }}",
        "python",
        "-m",
    ]
    return prefix


@command_exists("python{{ cookiecutter.pyver}}")
def create_venv():
    warnings.warn(
        f"Creating venv at {PROJECT_DIRECTORY}/.{{ cookiecutter.project_slug }}",
    )
    run(
        [
            "python{{ cookiecutter.pyver }}",
            "-m",
            "venv",
            ".{{ cookiecutter.project_slug }}",
        ],
    )
    prefix = [
        ".{{ cookiecutter.project_slug }}/bin/python{{ cookiecutter.pyver }}",
        "-m",
    ]
    return prefix


@command_exists("git")
@subprocess_error("Could not initialize git repository")
def init_git():
    run(["git", "init", "."])
    run(["git", "add", "."])
    run(
        ["git", "remote", "add", "origin", "{{ cookiecutter.project_remote }}"],
    )
    run(
        [
            "git",
            "remote",
            "set-url",
            "--push",
            "origin",
            "{{ cookiecutter.project_remote }}",
        ],
    )

    run(
        [
            "git",
            "remote",
            "set-url",
            "--push",
            "origin",
            "{{ cookiecutter.project_remote }}",
        ],
    )


@command_exists("direnv")
def direnv_allow():
    run(["direnv", "allow"])


if __name__ == "__main__":

    if "{{ cookiecutter.create_author_file }}" != "y":
        remove_file("AUTHORS.rst")
        # remove_file("docs/authors.rst")

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")

    init_git()

    venv = "{{ cookiecutter.virtual_env }}"

    if venv == "anaconda":
        prefix = create_conda()
    elif venv == "venv":
        prefix = create_venv()
        remove_file("environment.yml")

    else:
        raise ValueError("a virtual env must be used")
    run(
        prefix + ["pip", "install"] + SETUP_DEPENDENCIES,
    )

    run(prefix + update_requirements())
    run(prefix + update_requirements("dev"))
    run(prefix + update_requirements("docs"))
    run(prefix + update_requirements("tests"))

    run(
        prefix
        + [
            "pre_commit",
            "install",
            "--hook-type",
            "pre-merge-commit",
            "--install-hooks",
            "--overwrite",
        ],
    )

    if "{{ cookiecutter.create_envrc }}" == "y":
        direnv_allow()
    else:
        remove_file(".envrc")
    run(prefix + ["pip", "install", "-e", ".[dev]"])
