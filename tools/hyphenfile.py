#!/usr/bin/env -S uv run -q --script
#
# /// script
# requires-python = ">=3.13"
# dependencies = [
#       "click",
#       "rich",
# ]
# ///

from pathlib import Path
import sys
from typing import IO

import click
from rich.console import Console

THIS_DIR = Path(__file__).parent
TEST_DIR = THIS_DIR.parent / "test"
sys.path.insert(0, str(THIS_DIR.parent / "src"))

import pylabeador  # noqa: E402

HEADER = """\
# ---------------------------------------------------------------------------
# Spanish words test suite
# ---------------------------------------------------------------------------
# Format:
# [word] [hyphenated] [stress] [accent]
#
# - word: The full words
# - hypenated: The word split in syllables, separated by hyphens
# - stress: The index of the stress syllable (0-based)
# - accent: The position of the accent in the word (0-based)
#
# Note that this is not necessarily "correct" hyphenation, but instead it is what
# the library currently does. It is meant to catch any differences in behaviour
# during development.
# ---------------------------------------------------------------------------
"""

DEFAULT_OUTPUT_FILE = TEST_DIR / "spanish-hyphens.txt"
DEFAULT_INPUT_FILE = TEST_DIR / "commonspanish"


@click.command()
@click.option("--input", "-i", "input_file", type=click.File("r"), default=DEFAULT_INPUT_FILE)
@click.option("--output", "-o", "output_file", type=click.File("w"), default=DEFAULT_OUTPUT_FILE)
@click.option(
    "--try-hard",
    "-t",
    is_flag=True,
    default=False,
    help="When source lines have more than one word, take the first of each line",
)
def main(input_file: IO[str], output_file: IO[str], try_hard: bool):
    """
    Generate a test-data file from a list of words.

    Note that this is not necessarily "correct" hyphenation, but instead it is what
    the library currently does. It is meant to catch any differences in behaviour
    during development.
    """
    errors = []
    input_lines = input_file
    input_path = Path(input_file.name).resolve()
    output_path = Path(output_file.name).resolve()
    if input_path == output_path:
        input_lines = list(input_file)
        input_file.close()

    print(HEADER, file=output_file)
    for line_no, line in enumerate(input_lines, start=1):
        text = line.strip()
        parts = text.split()
        if len(parts) > 1:
            if try_hard:
                text = parts[0]
            else:
                errors.append((line_no, f"Multiple words on line: [bold red]{text}[/bold red]"))
                continue
        if not text or text.startswith("#"):
            continue
        try:
            w = pylabeador.syllabify_with_details(text)
            print(
                f"{w.original} {w.hyphenated} {w.stressed} {w.accented if w.accented is not None else '-'}".strip(),
                file=output_file,
            )
        except pylabeador.errors.HyphenatorError as e:
            errors.append((line_no, str(e)))
    console = Console(stderr=True)
    console.print("[bold green]DONE[/bold green]")

    if errors:
        console.print("[bold red]With errors:[/bold red]")
        for line_no, err in errors:
            console.print(f"[bold red]{line_no}[/bold red]: {err}")


if __name__ == "__main__":
    main()
