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

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List

from .util import is_vowel


@dataclass
class Syllable:
    onset: str = ''
    nucleus: str = ''
    coda: str = ''
    accented: bool = False
    stressed: bool = False

    @property
    def value(self):
        return f"{self.onset}{self.nucleus}{self.coda}"


@dataclass
class WordProgress:
    original_word: str
    pos: int = 0
    len: int = field(init=False, default=0)
    accent: Optional[int] = None
    stress_found: bool = None
    stressed: Optional[int] = None
    syllables: List[Syllable] = field(default_factory=list)
    word: str = field(init=False)

    def __post_init__(self):
        self.word = self.original_word.lower()
        self.len = len(self.word)

    @property
    def char(self):
        try:
            return self.word[self.pos]
        except IndexError:
            return None

    @property
    def one_ahead(self):
        return self.look_ahead(1)

    def look_ahead(self, steps=1):
        if self.has_next(steps):
            return self.word[self.pos + steps]

    @property
    def one_behind(self):
        return self.look_behind(1)

    def look_behind(self, steps=1):
        if self.pos - steps >= 0:
            return self.word[self.pos - steps]

    @property
    def ended(self):
        return self.pos >= self.len

    def next(self, steps=1):
        for i in range(steps):
            if not self.has_next():
                self.pos = self.len
                return None
            self.pos += 1
        return self.char

    def previous(self):
        if self.pos > 0:
            self.pos -= 1
            return self.char

    def has_next(self, steps=1):
        return self.pos + steps < self.len

    def __getitem__(self, item):
        return self.word[item]

    @property
    def hyphenated(self):
        return "-".join(s.value for s in self.syllables)

    def hyphenate(self, with_stressed=False):
        def value(s):
            return s.value if not s.stressed or not with_stressed else f">{s.value}<"
        return "-".join(value(s) for s in self.syllables)

    def check(self):
        if self.stress_found:
            assert self.syllables[self.stressed - 1].stressed
            assert len(list(filter(None, (s.stressed for s in self.syllables)))) == 1, self.syllables

    def add_syllable(self):
        syllable = Syllable()
        self.syllables.append(syllable)
        return syllable

    @property
    def current_syllable(self):
        if self.syllables:
            return self.syllables[-1]


class VowelType(Enum):
    OPEN = 'aeo'
    OPEN_WITH_ACCENT = 'áéó'
    CLOSED = 'iuü'
    CLOSED_WITH_ACCENT = 'íú'

    @classmethod
    def from_char(cls, c) -> 'VowelType':
        if not is_vowel(c):
            raise ValueError(f"{c} is not a vowel")
        for val in cls:
            if c in val.value:
                return val

    @property
    def has_accent(self):
        return self in (self.OPEN_WITH_ACCENT, self.CLOSED_WITH_ACCENT)

    @property
    def is_closed(self):
        return self in (self.CLOSED, self.CLOSED_WITH_ACCENT)

    @property
    def is_open(self):
        return self in (self.OPEN_WITH_ACCENT, self.OPEN)