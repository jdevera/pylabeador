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
from pylabeador.util import is_vowel


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


def do_test_is_y_vowel(word, expected):
    y_pos = word.find("y")
    assert y_pos != -1
    char_after = word[y_pos + 1] if y_pos < len(word) - 1 else None
    assert is_vowel("y", char_after) is expected


class TestIsYVowelFunction:
    """Test the is_y_vowel utility function"""

    @pytest.mark.parametrize(
        "word, expected",
        [
            ("bypass", True),
            ("byte", True),
        ],
    )
    def test_y_between_consonants_is_vowel(self, word, expected):
        """'y' between consonants should be treated as vowel"""
        do_test_is_y_vowel(word, expected)

    @pytest.mark.parametrize(
        "word, expected",
        [
            ("curry", True),
            ("muy", True),
            ("estoy", True),
        ],
    )
    def test_y_at_word_end_is_vowel(self, word, expected):
        """'y' at word end should be treated as vowel"""
        do_test_is_y_vowel(word, expected)

    @pytest.mark.parametrize(
        "word, expected",
        [
            ("mayor", False),
            ("ayer", False),
            ("payaso", False),
            ("yeso", False),
            ("playa", False),
            ("cónyuge", False),
        ],
    )
    def test_y_followed_by_vowel_is_consonant(self, word, expected):
        """'y' followed by vowel should be treated as consonant"""
        do_test_is_y_vowel(word, expected)

    @pytest.mark.parametrize(
        "word, pos",
        [
            ("bypass", 1),
            ("curry", 4),
        ],
    )
    def test_y_with_context_as_vowel(self, word, pos):
        """Test 'y' with context where it should be vowel"""
        char_after = word[pos + 1] if pos < len(word) - 1 else None
        assert is_vowel("y", char_after) is True

    @pytest.mark.parametrize(
        "word, pos",
        [
            ("mayor", 2),
            ("ayer", 1),
            ("payaso", 2),
        ],
    )
    def test_y_with_context_as_consonant(self, word, pos):
        """Test 'y' with context where it should be consonant"""
        assert is_vowel("y", word[pos + 1]) is False

    @pytest.mark.parametrize("char", ["a", "e", "i", "o", "u"])
    def test_backward_compatibility_regular_vowels(self, char):
        """Test that existing behavior is preserved for regular vowels"""
        assert is_vowel(char) is True

    @pytest.mark.parametrize("char", ["b", "c"])
    def test_backward_compatibility_consonants(self, char):
        """Test that existing behavior is preserved for consonants"""
        assert is_vowel(char) is False

    def test_backward_compatibility_y(self):
        """Test that 'y' without context should be consonant (backward compatibility)"""
        assert is_vowel("y") is False
