# -------------------------------------------------------------------------------------
# Copyright (c) 2020 Jacobo de Vera Hernández
#
# This file is part of Pylabeador.
#
# Pylabeador is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pylabeador is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pylabeador.  If not, see <https://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------------

import pytest

from pylabeador import syllabify_with_details
from .utils import data_file_open


def ids_func(val):
    return f"{str(val).replace('-', '~')}"


def spanish_common_words():
    with data_file_open("spanish-hyphens2.txt") as fin:
        for line in fin:
            if line.startswith("#"):
                continue
            word, hyphenation, stressed, accent_pos = line.strip().split()
            try:
                accent_pos = int(accent_pos)
            except:
                accent_pos = None
            yield word, hyphenation, int(stressed), accent_pos


def parametrize_with_words_from(source):
    return pytest.mark.parametrize('word, hyphenated, stressed, accent_pos', source, ids=ids_func)


@parametrize_with_words_from(spanish_common_words())
def test_hyphenation_of_common_words(word, hyphenated, stressed, accent_pos):
    res = syllabify_with_details(word)    
    accented = accent_pos - 1 if accent_pos is not None else None
    assert res.hyphenated == hyphenated
    assert res.stressed == stressed - 1
    assert res.accented == accented


@parametrize_with_words_from(
    [
        ('Actuáis', 'Ac-tuáis', 2, 5),
        ('Construcción', 'Cons-truc-ción', 3, 11),
        ('Melón', 'Me-lón', 2, 4),
        ('Desagüe', 'De-sa-güe', 2, None),
        ('fugu', 'fu-gu', 1, None),
    ],
)
def test_special_words(word, hyphenated, stressed, accent_pos):
    res = syllabify_with_details(word)
    accented = accent_pos - 1 if accent_pos is not None else None
    assert res.hyphenated == hyphenated
    assert res.stressed == stressed - 1
    assert res.accented == accented
