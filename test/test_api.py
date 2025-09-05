import pylabeador


def test_syllabify():
    res = pylabeador.syllabify("tenacidad")
    assert res == ["te", "na", "ci", "dad"]


def test_syllabify_with_details():
    res = pylabeador.syllabify_with_details("tenacidad")
    assert res.hyphenated == "te-na-ci-dad"
    assert res.stressed == 3
    assert not res.accented
