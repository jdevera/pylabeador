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


def test_end():
    w = WordProgress("radio")
    w.pos = 3
    assert w.char == "i"
    assert w.next() == "o"
    assert w.char == "o"
    assert not w.ended
    assert w.one_ahead is None


def test_lookahead():
    w = WordProgress("que")
    assert w.char == "q"
    assert w.one_ahead == "u"
    w.next()
    assert w.char == "u"
    assert w.one_ahead == "e"
