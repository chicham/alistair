#!/usr/bin/env python

"""The setup script."""

from setuptools import setup

# entry_points={
#     'console_scripts': [
#         '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main',
#     ],
# },

setup(
    use_scm_version={
        "write_to": "src/{{ cookiecutter.project_slug }}/version.py",
        "write_to_template": '__version__ = "{version}"',
        "tag_regex": r"^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$",
    }
)
