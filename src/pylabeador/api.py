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


from .engine import parse_word
from .models import SyllabifiedWord
from .util import check_word_for_spanish_chars


def syllabify_with_details(word: str) -> SyllabifiedWord:
    """
    Syllabify a word and provide detailed information about the syllable structure.

    Args:
        word: The word to syllabify.

    Returns:
        A SyllabifiedWord object containing the syllable structure, stress, and accent information.

    Examples:
        >>> import pylabeador
        >>> from pprint import pprint
        >>> pprint(pylabeador.syllabify_with_details("encuentro"))
        SyllabifiedWord(original='encuentro',
                syllables=[Syllable(onset='',
                                    nucleus='e',
                                    coda='n',
                                    accented=False,
                                    stressed=False),
                           Syllable(onset='c',
                                    nucleus='ue',
                                    coda='n',
                                    accented=False,
                                    stressed=True),
                           Syllable(onset='tr',
                                    nucleus='o',
                                    coda='',
                                    accented=False,
                                    stressed=False)],
                stressed=1,
                accented=None)
    """

    check_word_for_spanish_chars(word)
    return parse_word(word).to_result()


def syllabify(word: str) -> list[str]:
    """
    Syllabify a word and return the syllables as a list of strings.

    Args:
        word: The word to syllabify.

    Returns:
        A list of strings containing the syllables of the word.

    Examples:
        >>> import pylabeador
        >>> pylabeador.syllabify("encuentro")
        ['en', 'cuen', 'tro']
    """

    res = syllabify_with_details(word)
    return [syl.value for syl in res.syllables]


def hyphenate(word: str) -> str:
    """
    Syllabify a word and return the hyphenated word as a string.

    Args:
        word: The word to syllabify.

    Returns:
        A string containing the hyphenated word.

    Examples:
        >>> import pylabeador
        >>> pylabeador.hyphenate("encuentro")
        'en-cuen-tro'
    """

    return syllabify_with_details(word).hyphenated
