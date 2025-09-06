# Test cases for letter 'y' syllabification

import pytest

import pylabeador
from pylabeador.util import is_vowel, is_y_vowel


class TestYVowelDetection:
    """Test the is_y_vowel utility function"""

    def test_y_between_consonants_is_vowel(self):
        """'y' between consonants should be treated as vowel"""
        assert is_y_vowel("bypass", 1) is True
        assert is_y_vowel("byte", 1) is True

    def test_y_at_boundaries_is_vowel(self):
        """'y' at word boundaries should be treated as vowel"""
        assert is_y_vowel("yeso", 0) is True  # start of word
        assert is_y_vowel("curry", 4) is True  # end of word
        assert is_y_vowel("muy", 2) is True  # end of word

    def test_y_between_vowels_is_consonant(self):
        """'y' between vowels should be treated as consonant"""
        assert is_y_vowel("mayor", 2) is False
        assert is_y_vowel("ayer", 1) is False
        assert is_y_vowel("payaso", 2) is False
        assert is_y_vowel("playa", 3) is False

    def test_y_edge_cases(self):
        """Test edge cases for 'y' detection"""
        # Invalid positions
        assert is_y_vowel("mayo", -1) is False
        assert is_y_vowel("mayo", 10) is False

        # Non-'y' characters
        assert is_y_vowel("mesa", 1) is False

    def test_context_aware_is_vowel(self):
        """Test updated is_vowel function with context"""
        # 'y' as vowel
        assert is_vowel("y", "bypass", 1) is True
        assert is_vowel("y", "curry", 4) is True

        # 'y' as consonant
        assert is_vowel("y", "mayor", 2) is False
        assert is_vowel("y", "ayer", 1) is False

        # Regular vowels should still work
        assert is_vowel("a") is True
        assert is_vowel("e") is True

        # Backward compatibility
        assert is_vowel("y") is False  # without context, 'y' is consonant


class TestYSillabification:
    @pytest.mark.parametrize(
        ["word", "expected"],
        [
            ("bypass", "by-pass"),
            ("byte", "by-te"),
            ("byroniano", "by-ro-nia-no"),
            ("Tytonidae", "Ty-to-ni-da-e"),
        ],
    )
    def test_y_between_consonants(self, word, expected):
        """'y' between consonants acts as vowel"""
        assert pylabeador.syllabify_with_details(word).hyphenated == expected

    @pytest.mark.parametrize(
        ["word", "expected"],
        [
            ("curry", "cu-rry"),
            ("muy", "muy"),
            ("estoy", "es-toy"),
        ],
    )
    def test_y_at_end_of_word(self, word, expected):
        """'y' at end of word acts as vowel"""
        assert pylabeador.syllabify_with_details(word).hyphenated == expected

    @pytest.mark.xfail(reason="Known issue with consonant clustering before 'y'")
    @pytest.mark.parametrize(
        ["word", "expected"],
        [
            ("coadyuvar", "co-ad-yu-var"),
            ("cónyuge", "cón-yu-ge"),
            ("inyección", "in-yec-ción"),
        ],
    )
    def test_y_complex_cases(self, word, expected):
        """More complex cases with 'y' as vowel"""
        assert pylabeador.syllabify_with_details(word).hyphenated == expected
