"""Run the examples in docstrings and READMEs as doctests, so the documentation stays honest."""

import doctest
import importlib
from pathlib import Path
import pkgutil

import pytest

import pylabeador

PROJECT_ROOT = Path(__file__).parent.parent

MODULES = [importlib.import_module(f"pylabeador.{module.name}") for module in pkgutil.iter_modules(pylabeador.__path__)]

READMES = ["README.md", "README.es.md"]


@pytest.mark.parametrize("module", MODULES, ids=lambda m: m.__name__)
def test_module_doctests(module):
    results = doctest.testmod(module)
    assert results.failed == 0


@pytest.mark.parametrize("readme", READMES)
def test_readme_examples(readme):
    results = doctest.testfile(str(PROJECT_ROOT / readme), module_relative=False)
    assert results.failed == 0
