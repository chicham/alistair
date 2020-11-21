"""The setup script."""

from setuptools import setup

extras_require = {}

with open("./requirements/docs.txt") as src_docs:
    extras_require["docs"] = src_docs.read().splitlines()

with open("./requirements/tests.txt") as src_tests:
    extras_require["tests"] = src_tests.read().splitlines()

with open("./requirements/dev.txt") as src_dev:
    extras_require["dev"] = src_dev.read().splitlines()

extras_require["all"] = {
    requirement
    for requirements in extras_require.values()
    for requirement in requirements
}

setup(
    use_scm_version=True,
    extras_require=extras_require,
)
