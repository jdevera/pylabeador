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
    with data_file_open("spanish-hyphens.txt") as fin:
        for line in fin:
            word, hyphenation, stressed = line.strip().split()
            yield word, hyphenation, int(stressed)


def parametrize_with_words_from(source):
    return pytest.mark.parametrize('word, hyphenated, stressed', source, ids=ids_func)


@parametrize_with_words_from(spanish_common_words())
def test_hyphenation_of_common_words(word, hyphenated, stressed):
    res = syllabify_with_details(word)
    assert res.hyphenated == hyphenated
    assert res.stressed == stressed


@pytest.mark.parametrize(
    'word, hyphenated, stressed, accented',
    [
        ('Actuáis', 'Ac-tuáis', 2, 4),
        ('Construcción', 'Cons-truc-ción', 3, 10),
        ('Melón', 'Me-lón', 2, 3),
        ('Desagüe', 'De-sa-güe', 2, None),
        ('fugu', 'fu-gu', 1, None),
    ]
)
def test_special_words(word, hyphenated, stressed, accented):
    res = syllabify_with_details(word)
    assert res.hyphenated == hyphenated
    assert res.stressed == stressed
    assert res.accented == accented