import pytest
from pylabeador import pylabeador


@pytest.mark.parametrize('value, expected', [
    ['a', True],
    ['ó', True],
    ['b', False],
    [None, False],
])
def test_is_vowel(value, expected):
    assert pylabeador.is_vowel(value) == expected

