#!/usr/bin/env -S uv run -q --script
#
# /// script
# requires-python = ">=3.13"
# dependencies = [
#       "rich",
#       "click",
# ]
# ///

from pathlib import Path
import sys
from typing import IO

import click
from rich.console import Console
from rich.table import Table

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR.parent / "src"))

import pylabeador  # noqa: E402


def lines_from(filename, start=1, limit=None):
    count = 0
    for lineno, line in enumerate(filename, start=1):
        if lineno < start:
            continue
        clean_line = line.strip()
        if not clean_line or clean_line.startswith("#"):
            continue
        count += 1
        if limit is not None and count > limit:
            break
        yield lineno, clean_line


def format_result(res: pylabeador.models.SyllabifiedWord):
    if res.accented is not None:
        original = (
            res.original[: res.accented]
            + f"[bold blue]{res.original[res.accented]}[/bold blue]"
            + res.original[res.accented + 1 :]
        )
    else:
        original = res.original
    hyphenated = "-".join(f"[bold green]{s.value}[/bold green]" if s.stressed else s.value for s in res.syllables)
    return original, hyphenated


@click.command()
@click.option("--input", "-i", type=click.File("r"), required=True)
@click.option("--start", "-s", type=int, default=1)
@click.option("--limit", "-l", type=int, default=None)
def main(input: IO[str], start: int, limit: int | None):
    """
    Generate a report of the syllabification and stress detection of a file of words.
    """
    errors = []
    console = Console()
    table = Table(row_styles=["", "on bright_black"])
    table.add_column("Line", justify="right")
    table.add_column("Original", justify="left")
    table.add_column("Hyphenated", justify="left")
    for lineno, line in lines_from(input, start, limit):
        try:
            res = pylabeador.syllabify_with_details(line)
            original, hyphenated = format_result(res)
            table.add_row(str(lineno), original, hyphenated)
        except pylabeador.errors.HyphenatorError as e:
            errors.append((lineno, e))
    console.print(table)
    if errors:
        console.print("[bold red]Errors:[/bold red]")
        for lineno, e in errors:
            console.print(f"[bold red]{lineno}[/bold red]: {e}")


if __name__ == "__main__":
    main()
