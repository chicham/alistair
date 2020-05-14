#!/usr/bin/env python
import os
import subprocess
import warnings
import ast
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
            if spawn.find_executable(cmd):
                return f(*args, **kwargs)
            else:
                warnings.warn("Command %s is not in path", cmd)

        return wrapper
    return decorator


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


@command_exists("git")
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


def run_pip(pip, pip_compile):
    subprocess.run(
        pip + ["install", "pip-tools", "pre-commit", "wheel", "setuptools-scm"]
    )

    for req in ("dev", "docs", "tests"):
        subprocess.run(pip_compile + [f"requirements/{req}.in"])
    subprocess.run(pip + ["install", "-e", ".[all]"])

@command_exists('conda')
def install_conda():
    pip = ["conda", "run", "-n", "{{ cookiecutter.project_slug }}", "pip"]
    pip_compile = [
        "conda",
        "run",
        "-n",
        "{{ cookiecutter.project_slug }}",
        "pip-compile",
    ]
    run_pip(pip, pip_compile)


@subprocess_error("Could not install the module {{ cookiecutter.project_slug }}")
def install():
    direnv_layout = "{{ cookiecutter.direnv_layout }}"
    if direnv_layout == "virtualenv":
        prefix = ".direnv/python{{ cookiecutter.pyver }}/bin/"
        pip = ["/".join([prefix, "pip"])]
        pip_compile = ["/".join([prefix, "pip-compile"])]
        run_pip(pip, pip_compile)
    elif direnv_layout == "anaconda":
        install_conda()
    else:
        raise RuntimeError(f"Environment {direnv_layout} is not recognized")


@command_exists("pre-commit")
@subprocess_error("Could not initialize pre-commit")
def pre_commit():
    subprocess.run(["pre-commit", "install"])


@command_exists("direnv")
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
        cmd = create_conda()
    elif layout == "virtualenv":
        cmd = create_virtualenv()
    else:
        warnings.warn(f"Layout {layout} not recognized")

    if cmd:
        subprocess.run(cmd)

@command_exists("conda")
def create_conda():
    return  [
        "conda",
        "create",
        "-y",
        "-c conda-forge",
        "-n",
        "{{ cookiecutter.project_slug }}",
        "python={{ cookiecutter.pyver }}",
    ]

@command_exists("python{{ cookiecutter.pyver }}")
def create_virtualenv():
    return [
        "python{{ cookiecutter.pyver }}",
        "-m",
        "venv",
        ".direnv/python{{ cookiecutter.pyver }}",
    ]


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
