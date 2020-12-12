"""The setup script."""

from setuptools import setup

extras_require = {}


def read_requirements(extra):
    with open(f"./requirements/{extra}.txt") as src:
        return [line for line in src.read().splitlines() if not line.startswith("#")]


try:
    extras_require["docs"] = read_requirements("docs")
except FileNotFoundError:
    pass


try:
    extras_require["tests"] = read_requirements("tests")
except FileNotFoundError:
    pass

try:
    extras_require["dev"] = read_requirements("dev")
except FileNotFoundError:
    pass

extras_require["all"] = {
    requirement
    for requirements in extras_require.values()
    for requirement in requirements
}

setup(
    use_scm_version=True,
    extras_require=extras_require,
)
