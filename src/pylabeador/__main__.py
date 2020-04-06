import argparse
import sys

from . import hyphenate, VERSION


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Syllabify Spanish words")
    parser.add_argument("words", metavar='word', nargs=argparse.ONE_OR_MORE)
    parser.add_argument("--version", action='version', version=f'%(prog)s {VERSION}')

    args = parser.parse_args(argv[1:])
    return args


def main(argv=None):
    """ Run this program """
    if argv is None:
        argv = sys.argv
    args = parse_args(argv)
    try:
        for word in args.words:
            res = hyphenate(word)
            print(res.hyphenate())
    except KeyboardInterrupt:
        sys.exit(-1)


def entrypoint():
    sys.exit(main(sys.argv) or 0)


if __name__ == '__main__':
    entrypoint()

