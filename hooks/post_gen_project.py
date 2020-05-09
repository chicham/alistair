#!/usr/bin/env python
import os
import subprocess
import warnings

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
    if "{{ cookiecutter.direnv_layout }}" == "pipenv":
        subprocess.run(["pipenv", "install", "-e", ".[dev,test,docs]"])
    else:
        cmd = ["pip", "install", "-e", ".[dev,test,docs]"]
        if "{{ cookiecutter.direnv_layout }} == conda":
            cmd = ["conda", "run", "-n", "{{ cookiecutter.project_slug }}"] + cmd

        subprocess.run(cmd)


@subprocess_error("Could not initialize pre-commit")
def pre_commit():
    subprocess.run(["pre-commit", "install"])
    subprocess.run(["pre-commit", "install", "--hook-type=pre-push"])


@subprocess_error("Could not initialize direnv")
def dir_env():
    subprocess.run(["direnv", "allow", "."])
    warnings.warn(
        "If the layouts are not configured, go to "
        "https://github.com/direnv/direnv/wiki/Python"
    )


def create_venv():
    layout = "{{ cookiecutter.direnv_layout }}"
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
    elif layout == "pipenv":
        cmd = ["pipenv", "--python", "{{ cookiecutter.pyver }}"]
    else:
        cmd = ["echo", "No venv"]

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
