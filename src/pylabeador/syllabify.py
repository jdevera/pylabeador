# -------------------------------------------------------------------------------------
# Copyright (C) 2009 TIP: Text & Information Processing (http://tip.dis.ulpgc.es)
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

from .errors import HyphenatorError
from .models import VowelType, WordProgress
from .util import CONSONANTS, is_vowel

CONSONANTS_BAR_Y = CONSONANTS - set("y")


def hyphenate(word: str) -> WordProgress:
    word = WordProgress(word)

    while not word.ended:
        syllable = word.add_syllable()
        start_pos = word.pos

        # All initial consonants belong to the onset (in the case of y, only the first)
        syllable.onset = onset(word)
        syllable.nucleus = nucleus(word)
        syllable.coda = coda(word)

        end_pos = word.pos
        syllable.accented = word.accent is not None and start_pos <= word.accent < end_pos

        num_syl = len(word.syllables)
        if word.stress_found and word.stressed is None:
            word.stressed = num_syl - 1

    # If the word does not have a graphical accent, then find the stressed
    # syllable according to the Spanish rules
    if not word.stress_found:
        num_syl = len(word.syllables)
        # If the word has only one syllable, that's the one!
        if num_syl == 1:
            word.stressed = num_syl - 1
        else:
            end = word[-1]
            prev = word[-2]
            if end == "y":
                # When the word ends in y, it is treated as a vowel, unless it is preceded by a vowel
                if is_vowel(prev, letter_after=end):
                    # y is preceded by a vowel, so it is treated as a consonant
                    word.stressed = num_syl - 1
                else:
                    # y is preceded by a consonant, so it is treated as a vowel
                    word.stressed = num_syl - 2
            # Ends in vowel or n or s (y is treated as consonant for stress rules)
            elif is_vowel(end) or end in "ns" and is_vowel(prev):
                word.stressed = num_syl - 2
            else:
                word.stressed = num_syl - 1
    word.syllables[word.stressed].stressed = True
    word.stress_found = True
    return word


def return_section(f):
    def wrapped(word: WordProgress):
        initial_pos = word.pos
        f(word)
        final_pos = word.pos
        return word.original_word[initial_pos:final_pos]

    return wrapped


@return_section
def onset(word: WordProgress):
    while not word.ended and word.char in CONSONANTS_BAR_Y:
        word.next()

    if not word.ended and word.one_behind is not None:
        last_two = word.one_behind + word.char
        if last_two == "qu" or (last_two == "gu" and str(word.one_ahead) in "eiéí"):
            # qu is always in the onset
            # gu is only in the onset if it is followed by i or e
            word.next()
        elif last_two == "gü":  # not gu
            # gü is always in the onset
            word.next()


@return_section
def nucleus(word: WordProgress):  # noqa: C901
    start_pos = word.pos

    if word.ended:
        return

    if word.char == "y":
        # Check if 'y' should be treated as vowel in this context
        if is_vowel(word.char, word.one_ahead):
            # 'y' is acting as vowel, continue with normal vowel processing
            pass
        else:
            # 'y' is acting as consonant, move past it
            word.next()

    if word.ended:
        return

    if not is_vowel(word.char, word.one_ahead):
        raise HyphenatorError("Nucleus expects a vowel!", word)

    vowel_type: VowelType = VowelType.from_char(word.char)
    if vowel_type.has_accent:
        word.accent = word.pos
        word.stress_found = True
    word.next()

    if vowel_type is VowelType.CLOSED_WITH_ACCENT:
        # An accented closed vowel breaks a possible diphthong
        return

    #  An h in the nucleus is not enough to determine whether this is a diphtong, and thus we need to
    #  continue in the nucleus, like in prohi-bir, or it is a new syllable, like in a-ho-ra.
    found_h = word.char == "h"
    if found_h:
        word.next()

    if word.ended:
        return

    # If we have not moved forward, it might mean we have strange characters in the word
    if start_pos == word.pos:
        raise HyphenatorError(
            "Expected to move forward in first stage of nucleus. Perhaps invalid chars?",
            word,
        )

    previous = vowel_type

    if not is_vowel(word.char, word.one_ahead):
        return

    # Second vowel:
    second_vowel = VowelType.from_char(word.char)
    if second_vowel.is_open:
        if previous.is_open:  # Two open vowels can't form a syllable
            if found_h:
                word.previous()
            return

        # The previous is closed
        if second_vowel.has_accent:
            word.accent = word.pos
            word.stress_found = True
        word.next()

    # Closed-vowel with written accent, can't be a triphthong, but could be a diphthong
    elif second_vowel is VowelType.CLOSED_WITH_ACCENT:
        word.accent = word.pos
        if previous.is_closed:  # diphthong
            word.stress_found = True
            word.next()
        elif found_h:
            word.previous()
        return

    # Closed vowel
    elif second_vowel is VowelType.CLOSED:
        if word.one_ahead and is_vowel(word.one_ahead, word.look_ahead(2)):
            # Vowel - Closed vowel - vowel can never be a triphthong. This syllable is over, and the currently evaluated
            # second vowel belongs to the next syllable
            if found_h:
                word.previous()
                # The current letter was a weak vowel, it was followed by a vowel
                # and preceded by an h, so we go back 1 char.
            return

        if word.char != word.one_behind:
            # Can only be diphthong if the closed vowels are different
            word.next()

        return  # Decendent diphthong

    # Third vowel?
    if word.ended:
        return

    if word.char in "ui":
        word.next()  # Tripthong

    # Special case: 'y' at the end of a word is treated as a consonant
    if word.char == "y" and word.at_end:
        word.next()


@return_section
def coda(word: WordProgress):  # noqa: C901
    if word.ended or is_vowel(word.char, word.one_ahead):
        return  # No coda

    # If we are at the end of the word, advance the pointer to the end position and bail out. The current consonant was
    # the coda.
    if word.at_end:  # End of word
        word.next()
        return

    # If there is only a consonant between vowels, it belongs to the following syllable
    # If the next letter is a vowel, then this consonant is not part of the coda
    if word.has_next() and is_vowel(word.one_ahead, word.look_ahead(2)):
        return

    # Current and next are consonants and are at the word, that looks like coda, except if the second is a y, which
    # acts like a vowel and then we'd have a case like above: one consonant between vowels.
    if word.pos >= word.len - 2:
        if word.one_ahead != "y":
            # The word ends with 2 consonants
            word.next(2)
        return

    # At this point we know that we have more than two letters until the end of the word
    c1 = word.char
    c2 = word.look_ahead(1)
    c3 = word.look_ahead(2)

    if c3 and is_vowel(c3, word.look_ahead(3)):
        digraph = c1 + c2
        # ll, ch, and rr start a new syllable
        if digraph in ("ll", "ch", "rr"):
            return

        # cons + h starts a syllable, except sh and rh
        if c1 not in "sr" and c2 == "h":
            return

        # Handle 'y' based on whether it's acting as vowel or consonant
        if c2 == "y":
            # Use context-aware detection to see if y is vowel or consonant
            if is_vowel("y", word.look_ahead(2)):
                # y is vowel - follows standard consonant+vowel rule (consonant goes to next syllable)
                return
            # y is consonant - move to y to start next syllable
            word.next()  # move the pointer to the y
            return

        # fmt: off
        if digraph in ('gl', 'cl', 'kl', 'bl', 'vl', 'pl', 'fl', 'tl',
                       'gr', 'cr', 'kr', 'br', 'vr', 'pr', 'fr', 'tr', 'dr'):
            return
        # fmt:on

        word.next()
    else:  # 3rd consonant
        if word.pos >= word.len - 3:  # The word ends with 3 consonants
            if c2 == "y":
                # Use context-aware detection
                if is_vowel("y", word.look_ahead(2)):
                    # y is vowel - previous consonant can stay as coda
                    return
                # y is consonant - handle like other consonants

            if c3 == "y":
                word.next()
            else:
                word.next(3)  # The word ends with 3 consonants
            return

        # This is not the end of the word - handle y based on context
        if c2 == "y":
            # Use context-aware detection
            if is_vowel("y", word.look_ahead(2)):
                # y is vowel - previous consonant goes to next syllable (standard rule)
                word.next()
                return
            # y is consonant - fall through to standard consonant cluster logic

        # The groups pt, ct, cn, ps, mn, gn, ft, pn, cz, tz and ts begin a syllable
        # when preceded by other consonant
        if c2 + c3 in (
            "pt",
            "ct",
            "cn",
            "ps",
            "mn",
            "gn",
            "ft",
            "pn",
            "cz",
            "tz",
            "ts",
        ):
            word.next()
            return

        # The consonant groups formed by a consonant following the letter l or r cannot be
        # separated and they always begin a new syllable.
        # y as a vowel starts a new syllable
        # ch starts a new syllable
        if c3 in "lry" or c2 + c3 == "ch":
            word.next()  # The next syllable starts in c2
        else:
            word.next(2)  # The next syllable starts in c3
