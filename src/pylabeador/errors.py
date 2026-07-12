# -------------------------------------------------------------------------------------
# Copyright (c) 2020 Jacobo de Vera Hernández
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


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import WordProgress


class HyphenatorError(Exception):
    """
    Error during syllabification.

    The in-progress word state, when available, is kept in `word` for debugging
    but stays out of the message shown to users.
    """

    def __init__(self, message: str, word: "WordProgress | None" = None) -> None:
        super().__init__(message)
        self.message = message
        self.word = word
