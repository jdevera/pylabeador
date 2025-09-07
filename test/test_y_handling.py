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
            ("coadyuvar", "co-ad-yu-var"),
            ("abyecto", "ab-yec-to"),
            ("adyacente", "ad-ya-cen-te"),
            ("ilyección", "il-yec-ción"),
            ("inyección", "in-yec-ción"),
            ("conyugal", "con-yu-gal"),
            ("enyugado", "en-yu-ga-do"),
            ("circunyacente", "cir-cun-ya-cen-te"),
            ("interyacente", "in-ter-ya-cen-te"),
            ("disyuntiva", "dis-yun-ti-va"),
            ("desyerbar", "des-yer-bar"),
        ],
    )
    def test_y_complex_cases(self, word, expected):
        """More complex cases with 'y' as vowel"""
        assert pylabeador.syllabify_with_details(word).hyphenated == expected


class TestYStressDetection:
    @pytest.mark.parametrize(
        ["word", "expected_stressed"],
        [
            ("caray", 1),
            ("estoy", 1),
            ("whisky", 0),
            ("curry", 0),
        ],
    )
    def test_y_stress_detection(self, word, expected_stressed):
        assert pylabeador.syllabify_with_details(word).stressed == expected_stressed
