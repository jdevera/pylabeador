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

VOWELS = set("aáeéiíoóuúü")
CONSONANTS = set("bcdfghjklmnñpqrstvwxyz")
LETTERS = VOWELS.union(CONSONANTS)

_NOT_PASSED = "-N/A-"


def is_vowel(v: str | None, letter_after: str | None = _NOT_PASSED):
    """
    Check if character is a vowel.
    For 'y', uses context-aware detection if word and pos are provided.
    - 'y' acts as CONSONANT when followed by a vowel
    - 'y' acts as VOWEL otherwise (including when followed by consonant or at word boundaries)
    """
    if v == "y":
        if letter_after == _NOT_PASSED:
            return False
        return letter_after not in VOWELS
    return v in VOWELS


def check_word_for_spanish_chars(word):
    from .errors import HyphenatorError

    bad_letters = set(word.lower()) - LETTERS
    if bad_letters:
        raise HyphenatorError(f"The word {word} contains invalid letters in Spanish: {bad_letters}")
    if "ü" in word:
        pos = word.find("ü")
        follows_g = pos > 0 and word[pos - 1] == "g"
        folowed_by_ei = pos + 1 < len(word) and word[pos + 1] in "eiéí"
        if not follows_g or not folowed_by_ei:
            raise HyphenatorError(f"The word {word} does not seem to be Spanish, where ü can only appear in güe or güi")
