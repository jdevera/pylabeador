# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.5.0] - 2020-08-02
### Fixed
- Fix incorrect syllable division when the coda is empty and the next syllable starts with cr or cl.

## [0.4.0] - 2020-07-25
### Fixed
- Fix incorrect syllable division when there is a consonant in the coda and the next syllable starts with "ch".

## [0.3.0] - 2020-04-23
### Fixed
- Fix inconsistency between stressed syllable position and graphical accent position, now all using 0-based positions. (by @kikocorreoso)

## [0.2.0] - 2020-04-10
### Changed
- Stop exposing internals in the result of `syllabify_with_details`, use a separate class for results. (08834c2)

### Fixed
- Fix crash when syllabifing words ending in "gu". (f848a4c)

## [0.1.5] - 2020-04-09

Initial public release.
