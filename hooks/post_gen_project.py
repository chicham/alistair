#!/usr/bin/env python
import os
import subprocess
import warnings

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def init_git():
    try:
        subprocess.run(["git", "init", "."])
        subprocess.run(["git", "add", "."])
    except subprocess.CalledProcessError:
        warnings.warn("Can't initialize git")


def install():
    try:
        subprocess.run(["pip", "install", "-e", ".[dev,test,docs]"])
    except subprocess.CalledProcessError:
        warnings.warn("Could not install the module {{ cookiecutter.project_slug }}")


def pre_commit():
    try:
        subprocess.run(["pre-commit install"])
        subprocess.run(["pre-commit install --hook-type push"])
    except subprocess.CalledProcessError:
        warnings.warn("Could not initialize pre-commit")


if __name__ == "__main__":

    if "{{ cookiecutter.create_author_file }}" != "y":
        remove_file("AUTHORS.rst")
        remove_file("docs/authors.rst")

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")

    init_git()
    install()
