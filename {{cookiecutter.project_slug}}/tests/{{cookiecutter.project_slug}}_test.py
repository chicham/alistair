#!/usr/bin/env python

"""Tests for `{{ cookiecutter.project_slug }}` package."""

import importlib
import pytest


def test_import():
    try:
        importlib.import_module("{{ cookiecutter.project_slug }}")
    except ModuleNotFoundError:
        pytest.fail()
