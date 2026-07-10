import dataclasses

import pytest

import pylabeador


def test_empty_word_raises_hyphenator_error():
    with pytest.raises(pylabeador.HyphenatorError):
        pylabeador.syllabify("")


@pytest.mark.parametrize("word", ["b", "bcd"])
def test_word_without_vowels_raises_hyphenator_error(word):
    with pytest.raises(pylabeador.HyphenatorError):
        pylabeador.syllabify(word)


def test_syllabify():
    res = pylabeador.syllabify("tenacidad")
    assert res == ["te", "na", "ci", "dad"]


def test_hyphenate():
    assert pylabeador.hyphenate("tenacidad") == "te-na-ci-dad"


def test_public_api_exports():
    for name in pylabeador.__all__:
        assert hasattr(pylabeador, name)
    assert "hyphenate" in pylabeador.__all__


def test_syllabify_with_details():
    res = pylabeador.syllabify_with_details("tenacidad")
    assert res.hyphenated == "te-na-ci-dad"
    assert res.stressed == 3
    assert not res.accented


def test_syllabified_word_is_immutable():
    res = pylabeador.syllabify_with_details("tenacidad")
    with pytest.raises(dataclasses.FrozenInstanceError):
        res.original = "otra"
    with pytest.raises(AttributeError):
        res.syllables.append(pylabeador.Syllable())
