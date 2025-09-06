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


def lines_from(filename):
    with data_file_open(filename) as fin:
        for line in fin:
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            yield clean_line


def spanish_common_words():
    for line in lines_from("spanish-hyphens.txt"):
        word, hyphenation, stressed, accent_pos = line.split()
        accent_pos = int(accent_pos) if accent_pos != "-" else None
        yield word, hyphenation, int(stressed), accent_pos


def parametrize_with_words_from(source):
    return pytest.mark.parametrize(
        "word, hyphenated, stressed, accent_pos",
        (
            pytest.param(word, hyphenation, stressed, accent_pos, id=word)
            for word, hyphenation, stressed, accent_pos in source
        ),
    )


@parametrize_with_words_from(spanish_common_words())
def test_hyphenation_of_common_words(word, hyphenated, stressed, accent_pos):
    res = syllabify_with_details(word)
    assert res.hyphenated == hyphenated
    assert res.stressed == stressed
    assert res.accented == accent_pos


@parametrize_with_words_from(
    [
        ("Actuáis", "Ac-tuáis", 1, 4),
        ("Construcción", "Cons-truc-ción", 2, 10),
        ("Melón", "Me-lón", 1, 3),
        ("Desagüe", "De-sa-güe", 1, None),
        ("fugu", "fu-gu", 0, None),
        ("paraguay", "pa-ra-guay", 2, None),
        ("paraguayo", "pa-ra-gua-yo", 2, None),
    ]
)
def test_special_words(word, hyphenated, stressed, accent_pos):
    res = syllabify_with_details(word)
    assert res.hyphenated == hyphenated
    assert res.stressed == stressed
    assert res.accented == accent_pos
