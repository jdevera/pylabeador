# Test cases for letter 'y' syllabification

import pytest

import pylabeador


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

    @pytest.mark.parametrize(
        ["word", "expected"],
        [
            pytest.param("coadyuvar", "co-ad-yu-var"),
            pytest.param(
                "cónyuge",
                "cón-yu-ge",
                marks=pytest.mark.xfail(reason="Known issue with consonant clustering before 'y'"),
            ),
            pytest.param(
                "inyección",
                "in-yec-ción",
                marks=pytest.mark.xfail(reason="Known issue with consonant clustering before 'y'"),
            ),
        ],
    )
    def test_y_complex_cases(self, word, expected):
        """More complex cases with 'y' as vowel"""
        assert pylabeador.syllabify_with_details(word).hyphenated == expected
