# Alistair
A [cookiecutter](https://www.github.com/audreyr/cookiecutter "cookiecutter") template for
python development

## Features

 - Automatic versioning with setuptools_scm (based on git tags)
 - setup.cfg with wemake-python-styleguide/flake8/ opinions, pytest/pytest-cov configuration (including fixed PYTHONHASHSEED), isort compatibility with black, pytype configuration
 - `dev`, `docs`, `test` extras for installation
 - Choice of virtual environment handler  between `anaconda` or `venv`
 - Generation of `.envrc` file to use with direnv (auto activate virtual
   environment)
 - Generate docker environment with `repo2docker` ( ex: repo2docker --config environment.yml --editable --image-name <my_image_name> . )
 - Initialisation of the git repository
 - A `pre-commit` configuration file and auto initialisation of `pre-commit`
 - Pre-configured `sphinx` for documenation ( with possibility to use notebooks)

## Installation

Prior to installing alistair, the cookiecutter package must be installed in your environment. This is achieved via the following command::

    $ conda install cookiecutter

With cookiecutter installed, the alistair template can be installed with::

    $ cookiecutter https://github.com/chicham/alistair.git


Once cookiecutter clones the template, you will be asked a series of questions related to your project::

## Usage

After answering the questions asked during installation, a python module will be
created in your current working directory.


## Recommendation

- Use [conda](https://docs.conda.io/en/latest/) to manage your virtual environment ( always create a virtualenv !!)
- Use [direnv](https://direnv.net/) to automatically activate your virtualenv
- Use [](https://direnv.net/) to automatically activate your virtualenv
- Look at [pre-commit](https://pre-commit.com/) website to configure hooks
- Look at [wemake-python.styleguide](https://wemake-python-stylegui.de/en/latest/) website to configure flake8 violations
