# Alistair
A [cookiecutter](https://www.github.com/audreyr/cookiecutter "cookiecutter") template for
python development

## Features

 - Automatic versioning with setuptools_scm (requires git annotated tags before it'll work)
 - setup.cfg with flake8 opinions, pytest/pytest-cov configuration (including fixed PYTHONHASHSEED), isort compatibility with black, pytype configuration
 - `dev`, `docs`, `test` options for installation
 - Choice of virtual environment handler  between `conda` or `virtualenv`
 - Generation of `.envrc` file to use with direnv (auto activate virtual
   environment)
 - Generation of a basic Dockerfile
 - Initialisation of the git repository
 - A `pre-commit` configuration file and auto initialisation of `pre-commit`

## Installation

Prior to installing alistair, the cookiecutter package must be installed in your environment. This is achieved via the following command::

    $ conda install cookiecutter

With cookiecutter installed, the alistair template can be installed with::

    $ cookiecutter https://github.com/chicham/alistair.git

Also [direnv](https://direnv.net/) must be installed and configured (https://github.com/direnv/direnv/wiki/Python) to allow auto activation of virtual environment.

Once cookiecutter clones the template, you will be asked a series of questions related to your project::

## Usage

After answering the questions asked during installation, a python module will be
created in your current working directory.
