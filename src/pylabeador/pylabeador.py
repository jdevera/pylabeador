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


from . import syllabify as _syllabify
from .models import SyllabifiedWord
from .util import check_word_for_spanish_chars


def syllabify_with_details(word: str) -> SyllabifiedWord:
    check_word_for_spanish_chars(word)
    return _syllabify.hyphenate(word).to_result()


def syllabify(word: str) -> list[str]:
    res = syllabify_with_details(word)
    return [syl.value for syl in res.syllables]
