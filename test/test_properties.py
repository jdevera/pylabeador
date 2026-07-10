"""Property-based tests: invariants that must hold for any input, not just the golden-file corpus."""

from hypothesis import assume, given
from hypothesis import strategies as st

import pylabeador
from pylabeador.errors import HyphenatorError

# ü is excluded because it is only valid in güe/güi and would make most generated words invalid
SPANISH_LETTERS = "abcdefghijklmnñopqrstuvwxyzáéíóú"

words = st.text(alphabet=SPANISH_LETTERS, min_size=1, max_size=15)


@given(words)
def test_only_hyphenator_errors_escape(word):
    """The API either succeeds or raises HyphenatorError, never a raw internal error."""
    try:
        pylabeador.syllabify_with_details(word)
    except HyphenatorError:
        pass


def syllabify_valid_word(word):
    try:
        return pylabeador.syllabify_with_details(word)
    except HyphenatorError:
        assume(False)


@given(words)
def test_syllables_concatenate_to_original(word):
    result = syllabify_valid_word(word)
    assert "".join(s.value for s in result.syllables) == word


@given(words)
def test_every_syllable_has_a_nucleus(word):
    result = syllabify_valid_word(word)
    assert all(s.nucleus for s in result.syllables)


@given(words)
def test_exactly_one_stressed_syllable(word):
    result = syllabify_valid_word(word)
    stressed = [i for i, s in enumerate(result.syllables) if s.stressed]
    assert stressed == [result.stressed]
