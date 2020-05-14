#!/usr/bin/env python

"""The setup script."""

from setuptools import setup

# entry_points={
#     'console_scripts': [
#         '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:main',
#     ],
# },

extras_require = {}

with open("./requirements/docs.txt") as src:
    extras_require["docs"] = src.read().splitlines()

with open("./requirements/tests.txt") as src:
    extras_require["tests"] = src.read().splitlines()

with open("./requirements/dev.txt") as src:
    extras_require["dev"] = src.read().splitlines()

extras_require["all"] = {v for req in extras_require.values() for v in req}

setup(
    use_scm_version={
        "write_to": "src/{{ cookiecutter.project_slug }}/version.py",
        "write_to_template": '__version__ = "{version}"',
        "tag_regex": r"^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$",
    },
    extras_require=extras_require,
)
