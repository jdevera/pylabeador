# coding=utf-8
import dataclasses

import pytest

from pylabeador.pylabeador import WordProgress, onset, nucleus, hyphenate


def test_onset():
    w = WordProgress("queso")
    res = onset(w)
    assert res == "qu"
    w.pos = 3
    res = onset(w)
    assert res == "s"

def test_nucleus():
    w = WordProgress("tras")
    onset_res = onset(w)
    assert onset_res == "tr"
    nucleus_res = nucleus(w)
    assert nucleus_res == "a"

    w = WordProgress("huesca")
    onset_res = onset(w)
    assert onset_res == "h"
    nucleus_res = nucleus(w)
    assert nucleus_res == "ue"

def test_hypenate():
    res = hyphenate("televisión")
    print(dataclasses.asdict(res))
    assert res.hyphenated == 'te-le-vi-sión'


def split(*args):
    for arg in args:
        yield arg.split()

def ids_func(val):
    return f"{str(val).replace('-', '~')}"


@pytest.mark.parametrize('word, hyphenated, stressed', [
    ('Actuáis', 'Ac-tuáis', 2),
    ('Desagüe', 'De-sa-güe', 2),
], ids=ids_func)
def test_special_words(word, hyphenated, stressed):
    res = hyphenate(word)
    assert res.ended
    assert res.hyphenated == hyphenated
    assert res.stressed == stressed
