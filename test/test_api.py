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


def test_error_message_is_just_the_message():
    with pytest.raises(pylabeador.HyphenatorError) as exc_info:
        pylabeador.syllabify("pm")
    message = str(exc_info.value)
    assert "no nucleus" in message
    assert "WordProgress" not in message
    # The word state is still available for debugging
    word_state = exc_info.value.word
    assert word_state is not None
    assert word_state.original_word == "pm"


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
        res.original = "otra"  # ty: ignore[invalid-assignment]
    with pytest.raises(AttributeError):
        res.syllables.append(pylabeador.Syllable())  # ty: ignore[unresolved-attribute]
