import pytest
from pylabeador import pylabeador
from .utils import data_file_open


def ids_func(val):
    return f"{str(val).replace('-', '~')}"


def words():
    with data_file_open("spanish-hyphens.txt") as fin:
        for line in fin:
            word, hyphenation, stressed = line.strip().split()
            yield word, hyphenation, int(stressed)


@pytest.mark.parametrize('word, hyphenated, stressed', words(), ids=ids_func)
def test_hyphenation(word, hyphenated, stressed):
    res = pylabeador.hyphenate(word)
    assert res.ended
    assert res.hyphenated == hyphenated
    assert res.stressed == stressed



