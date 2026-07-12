# AGENTS.md

This file provides guidance to AI coding agents when working with code in this repository.

## Project Overview

Pylabeador is a Python library for automatic syllabification of Spanish words. The project uses a rule-based approach without lexical knowledge, making it fast but limited in handling complex cases like prefixes (e.g., "transatlántico"). The core functionality is exposed as both a Python API and a command-line tool.

## Development Commands

This project uses `mise` for task management and `uv` for Python package management. Key commands:

### Testing
- `mise run test` - Run the full test suite with pytest
- `mise run test -- test/test_api.py::test_syllabify` - Run a specific test

### Code Quality Checks
- `mise run lint` - Run ruff linting checks on src/ and test/
- `mise run format-check` - Check if code formatting is correct

### Automatic Fixing of Code Issues
- `mise run format` - Format code with ruff
- `mise run lint -- --fix` - Apply Ruff's automatic fixes

### Building and Distribution
- `mise run build` - Build source and wheel distributions (cleans first)
- `mise run clean` - Remove build artifacts and distribution files
- `mise run ci` - Run all CI tasks (build, format-check, lint, test)

### Version Management
- `mise run bump <version>` - Bump version and commit changes
- `mise run tag` - Create git tag with current version
- `mise run publish-test` - Publish to test PyPI (requires TEST_PYPI_TOKEN)
- `mise run publish` - NEVER USE, ABSOLUTELY NEVER

## Project Management

- New versions typically set a new MINOR
- A new version needs a new entry in the changelog before applying the version git tag
- There is a `CHANGELOG.markdown` based on https://keepachangelog.com/en/1.0.0/
- `mise run ci` must run clean before tagging a release
- Never push to github or release, this will only be done manually


## Architecture

### Core Components

**Main API (`src/pylabeador/api.py`)**
- `syllabify(word: str) -> list[str]` - Returns syllables as string list
- `syllabify_with_details(word: str) -> SyllabifiedWord` - Returns detailed syllabification with stress info
- `hyphenate(word: str) -> str` - Returns the word with syllables joined by hyphens

**Models (`src/pylabeador/models.py`)**
- `Syllable` - Represents a syllable with onset, nucleus, coda, and stress information
- `SyllabifiedWord` - Contains original word, syllables list, and stress/accent positions
- `WordProgress` - Tracks syllabification algorithm state during processing

**Core Algorithm (`src/pylabeador/engine.py`)**
- Contains the main hyphenation logic based on Spanish phonological rules
- Uses character classification and vowel/consonant patterns

**Utilities (`src/pylabeador/util.py`)**
- Character validation for Spanish text
- Helper functions for vowel/consonant identification

### Project Structure
```
src/pylabeador/          # Main package
├── __init__.py          # Public API exports
├── api.py               # Main API functions
├── models.py            # Data models
├── engine.py            # Core syllabification algorithm
├── util.py              # Utilities
├── errors.py            # Custom exceptions
├── __main__.py          # CLI entry point
└── __version__.py       # Version string

test/                    # Test suite
├── test_api.py          # Public API tests
├── test_*.py            # Algorithm and internal tests
└── spanish-hyphens.txt  # Test data
```

### Key Design Patterns
- Clean separation between public API (`api.py`) and internal implementation (`engine.py`)
- Dataclasses for structured data (`Syllable`, `SyllabifiedWord`)
- Validation at API boundaries (`check_word_for_spanish_chars`)
- Context-aware 'y' handling: 'y' acts as vowel except when followed by a vowel

## Testing Strategy

Tests are organized by component:
- `test_api.py` - Tests public API functions
- `test_internals.py` - Tests internal algorithm functions
- `test_hyphenation_and_stress.py` - Tests syllabification accuracy
- `test_bits.py` - Tests utility functions
- `test_wordprogress.py` - Tests algorithm state tracking

All tests use pytest. Set `PYTHONPATH=src` when running tests directly.

### Test Data
Most of the tests are driven by a data file `test/spanish-hyphens.txt`. It can have comment lines (start with #), empty lines, and data lines. Data lines look like this:

```
esperen es-pe-ren 1 -
teníamos te-ní-a-mos 1 3
```

And this is the format:
    [word] [hyphenated] [stress] [accent]

- word: The full words
- hypenated: The word split in syllables, separated by hyphens
- stress: The index of the stress syllable (0-based)
- accent: The position of the accent in the word (0-based)

This file is regenerated from itself using `tools/hyphenfile.py` (via `mise run gen-test-data`), therefore, it does not represent necessarily "correct" hyphenation, but instead it is what the library currently does. It is meant to catch any differences in behaviour. Sometimes I will find errors and change them first so that I can do test-drive development on the fix.

## Build System

- **Build tool**: Hatchling (configured in pyproject.toml)
- **Package manager**: uv
- **Python versions**: 3.10-3.13
- **Linting**: ruff with strict rules (E, F, I, B, C, N, UP, S, RET, I001)
- **Line length**: 120 characters
