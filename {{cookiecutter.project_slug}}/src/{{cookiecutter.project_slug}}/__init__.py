"""Top-level package for {{ cookiecutter.project_name }}."""
from pkg_resources import get_distribution

__author__ = """{{ cookiecutter.full_name }}"""
__email__ = "{{ cookiecutter.email }}"
__version__ = get_distribution("{{ cookiecutter.project_slug }}").version
