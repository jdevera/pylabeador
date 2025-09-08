# -------------------------------------------------------------------------------------
# Copyright (c) 2025 Jacobo de Vera Hernández
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

from pylabeador.errors import HyphenatorError
from pylabeador.util import check_word_for_spanish_chars


@pytest.mark.parametrize(
    "word, expected_error_substring",
    [
        # Valid Spanish words - should not raise any exception
        ("hola", None),
        ("tenacidad", None),
        ("niño", None),
        ("güero", None),
        ("Güero", None),
        ("GÜERO", None),
        ("güe", None),
        ("güi", None),
        ("pingüino", None),
        ("bilingüe", None),
        ("Bilingüe", None),
        ("BILINGÜE", None),
        # Invalid characters
        ("café@", "invalid letters"),
        ("word123", "invalid letters"),
        ("señor!", "invalid letters"),
        ("test&word", "invalid letters"),
        # Invalid ü usage
        ("müsica", "ü can only appear in güe or güi"),
        ("tü", "ü can only appear in güe or güi"),
        ("ürsula", "ü can only appear in güe or güi"),
        ("güa", "ü can only appear in güe or güi"),
        ("güo", "ü can only appear in güe or güi"),
        ("gü", "ü can only appear in güe or güi"),
        ("büggy", "ü can only appear in güe or güi"),
    ],
)
def test_check_word_for_spanish_chars(word, expected_error_substring):
    """Test Spanish character validation with various inputs"""
    if expected_error_substring is None:
        # Should not raise any exception
        check_word_for_spanish_chars(word)
    else:
        # Should raise HyphenatorError with expected substring
        with pytest.raises(HyphenatorError) as exc_info:
            check_word_for_spanish_chars(word)
        assert expected_error_substring in str(exc_info.value)
