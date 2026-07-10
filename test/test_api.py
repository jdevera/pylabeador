import pytest

import pylabeador


def test_empty_word_raises_hyphenator_error():
    with pytest.raises(pylabeador.HyphenatorError):
        pylabeador.syllabify("")


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
