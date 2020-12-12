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


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def update_dev():
    return [
        "piptools",
        "compile",
        "--output-file=requirements/dev.txt",
        "requirements/dev.in",
    ]


@command_exists("conda")
def create_conda():
    args = [
        "conda",
        "create",
        "-y",
        "-n",
        "{{ cookiecutter.project_slug }}",
        "python={{ cookiecutter.pyver }}",
    ]
    args.extend(SETUP_DEPENDENCIES)
    subprocess.run(args, check=True)
    prefix = [
        "conda",
        "run",
        "-n",
        "{{ cookiecutter.project_slug }}",
        "python",
        "-m",
    ]
    subprocess.run(prefix + update_dev(), check=True)
    subprocess.run(
        prefix
        + [
            "pip",
            "install",
            "-r",
            "requirements/dev.txt",
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
    prefix = [
        ".{{ cookiecutter.project_slug }}/bin/python{{ cookiecutter.pyver }}",
        "-m",
    ]
    subprocess.run(
        prefix + ["pip", "install"] + SETUP_DEPENDENCIES,
        check=True,
    )
    subprocess.run(
        prefix + update_dev(),
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


def pre_commit_install(prefix=None):
    if not prefix:
        prefix = ["python", "-m"]
    args = [
        "pre_commit",
        "install",
        "--hook-type",
        "pre-merge-commit",
        "--install-hooks",
        "--overwrite",
    ]
    subprocess.run(
        prefix + args,
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
        pre_commit_install(
            [
                "conda",
                "run",
                "-n",
                "{{ cookiecutter.project_slug }}",
                "python",
                "-m",
            ],
        )
    elif venv == "venv":
        create_venv()
        pre_commit_install(
            prefix=[
                ".{{ cookiecutter.project_slug }}/bin/python{{ cookiecutter.pyver }}",
            ],
        )
    else:
        pass
    if "{{ cookiecutter.use_direnv }}" == "y":
        direnv_allow()
    else:
        subprocess.run(["rm", "-f", ".envrc"], check=True)
