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

from .util import is_vowel


@dataclass
class Syllable:
    onset: str = ""
    nucleus: str = ""
    coda: str = ""
    accented: bool = False
    stressed: bool = False

    @property
    def value(self):
        return f"{self.onset}{self.nucleus}{self.coda}"


@dataclass(frozen=True)
class SyllabifiedWord:
    original: str
    syllables: list[Syllable]
    stressed: int | None = None
    accented: int | None = None

    @property
    def hyphenated(self):
        return "-".join(s.value for s in self.syllables)

    def hyphenate(self, with_stressed=False):
        def value(s):
            return s.value if not s.stressed or not with_stressed else f">{s.value}<"

        return "-".join(value(s) for s in self.syllables)


@dataclass
class WordProgress:
    original_word: str
    pos: int = 0
    len: int = field(init=False, default=0)
    accent: int | None = None
    stress_found: bool = None
    stressed: int | None = None
    syllables: list[Syllable] = field(default_factory=list)
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
    def one_ahead(self) -> str | None:
        return self.look_ahead(1)

    def look_ahead(self, steps=1) -> str | None:
        if self.has_next(steps):
            return self.word[self.pos + steps]
        return None

    @property
    def one_behind(self):
        return self.look_behind(1)

    def look_behind(self, steps=1):
        if self.pos - steps >= 0:
            return self.word[self.pos - steps]
        return None

    @property
    def ended(self):
        return self.pos >= self.len

    @property
    def at_end(self) -> bool:
        return self.pos == self.len - 1

    def next(self, steps=1):
        for _ in range(steps):
            if not self.has_next():
                self.pos = self.len
                return None
            self.pos += 1
        return self.char

    def previous(self):
        if self.pos > 0:
            self.pos -= 1
            return self.char
        return None

    def has_next(self, steps=1):
        return self.pos + steps < self.len

    def __getitem__(self, item):
        return self.word[item]

    def check(self):
        if self.stress_found:
            if not self.syllables[self.stressed - 1].stressed:
                raise ValueError("Stressed syllable is not stressed")
            if len(list(filter(None, (s.stressed for s in self.syllables)))) != 1:
                raise ValueError("Multiple stressed syllables")

    def add_syllable(self):
        syllable = Syllable()
        self.syllables.append(syllable)
        return syllable

    @property
    def current_syllable(self):
        if self.syllables:
            return self.syllables[-1]
        return None

    def to_result(self) -> SyllabifiedWord:
        if not self.ended:
            raise ValueError("Word is not ended")
        if not self.stress_found:
            raise ValueError("Stress is not found")
        return SyllabifiedWord(self.original_word, self.syllables, self.stressed, self.accent)


class VowelType(Enum):
    OPEN = "aeo"
    OPEN_WITH_ACCENT = "áéó"
    CLOSED = "iuü"
    CLOSED_WITH_ACCENT = "íú"

    @classmethod
    def from_char(cls, c) -> "VowelType":
        if c.lower() == "y":
            # 'y' when acting as vowel behaves like 'i' (closed vowel)
            return cls.CLOSED
        if is_vowel(c):
            for val in cls:
                if c in val.value:
                    return val
        raise ValueError(f"{c} is not a vowel")

    @property
    def has_accent(self):
        return self in (self.OPEN_WITH_ACCENT, self.CLOSED_WITH_ACCENT)

    @property
    def is_closed(self):
        return self in (self.CLOSED, self.CLOSED_WITH_ACCENT)

    @property
    def is_open(self):
        return self in (self.OPEN_WITH_ACCENT, self.OPEN)
