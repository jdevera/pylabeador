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

from pylabeador import WordProgress
from pylabeador.syllabify import nucleus, onset


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


@pytest.mark.parametrize(
    "word, syllable_to_check, expected_hyphenation, expected_nucleus",
    [("paraguay", 3, "pa-ra-guay", "uay")],
)
def test_uncommon_nucleus(word, syllable_to_check, expected_hyphenation, expected_nucleus):
    from pylabeador.syllabify import hyphenate

    # Test the full hyphenation
    result = hyphenate(word)
    hyphenated = "-".join(s.value for s in result.syllables)
    assert hyphenated == expected_hyphenation

    # Test the specific syllable's nucleus
    target_syllable = result.syllables[syllable_to_check - 1]  # Convert to 0-based index
    assert target_syllable.nucleus == expected_nucleus
