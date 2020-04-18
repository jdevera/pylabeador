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

from pylabeador import WordProgress
from pylabeador.syllabify import onset, nucleus


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
