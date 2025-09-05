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

import argparse
import sys

from . import __version__, syllabify_with_details


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Syllabify Spanish words")
    parser.add_argument("words", metavar="word", nargs=argparse.ONE_OR_MORE)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    return parser.parse_args(argv[1:])


def main(argv=None):
    """Run this program"""
    if argv is None:
        argv = sys.argv
    args = parse_args(argv)
    try:
        for word in args.words:
            res = syllabify_with_details(word)
            print(res.hyphenated)
    except KeyboardInterrupt:
        sys.exit(-1)


def entrypoint():
    sys.exit(main(sys.argv) or 0)


if __name__ == "__main__":
    entrypoint()
