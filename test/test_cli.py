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

import io
from unittest.mock import patch

import pytest

from pylabeador.__main__ import main


def test_cli_normal_operation():
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        main(["pylabeador", "casa"])
    assert mock_stdout.getvalue().strip() == "ca-sa"


def test_cli_multiple_words():
    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        main(["pylabeador", "casa", "perro"])
    output = mock_stdout.getvalue().strip().split("\n")
    assert output == ["ca-sa", "pe-rro"]


def test_cli_invalid_characters_error():
    with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
        with pytest.raises(SystemExit) as exc_info:
            main(["pylabeador", "hello123"])
        assert exc_info.value.code == 1
    error_output = mock_stderr.getvalue().strip()
    assert error_output.startswith("Error:")
    assert "invalid letters" in error_output


def test_cli_invalid_u_diaeresis_error():
    with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
        with pytest.raises(SystemExit) as exc_info:
            main(["pylabeador", "müsica"])
        assert exc_info.value.code == 1
    error_output = mock_stderr.getvalue().strip()
    assert error_output.startswith("Error:")
    assert "does not seem to be Spanish" in error_output


def test_cli_keyboard_interrupt():
    with patch("pylabeador.__main__.syllabify_with_details", side_effect=KeyboardInterrupt):
        with pytest.raises(SystemExit) as exc_info:
            main(["pylabeador", "casa"])
        assert exc_info.value.code == -1
