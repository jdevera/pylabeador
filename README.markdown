[![](https://img.shields.io/github/actions/workflow/status/jdevera/pylabeador/pythonpackage.yml?branch=main)](https://github.com/jdevera/pylabeador/actions?query=workflow%3A%22Python+package%22+branch%3Amain)
[![codecov](https://codecov.io/gh/jdevera/pylabeador/branch/master/graph/badge.svg)](https://codecov.io/gh/jdevera/pylabeador)
![](https://img.shields.io/pypi/pyversions/pylabeador)
[![](https://img.shields.io/pypi/v/pylabeador)](https://pypi.org/project/pylabeador/)
![](https://img.shields.io/pypi/l/pylabeador)
![](https://img.shields.io/pypi/dm/pylabeador)
# Pylabeador: Automatic Syllabification of Spanish Words

# Install

```
pip install pylabeador
```

# Use

You can use it as a Python library:
```python
>>> import pylabeador
>>> pylabeador.syllabify("silabear")
['si', 'la', 'be', 'ar']
```

And you can use it as a command line tool:

```sh
$ pylabeador interesante
in-te-re-san-te
```
# Accuracy

Automatic syllabification without additional lexical or and semantic *knowledge* of the words can only go so far.  This syllabifier does not have such knowledge. Because of this, words such as *transatlántico*, whose correct hyphenation is *trans-a-tlán-ti-co* or even *trans-at-lán-ti-co*, end up being divided here into *tran-sa-tlán-ti-co*.  To hyphenate this correctly, it is necessary to know that the word without the prefix exists in Spanish with similar semantics to the one of the original word. This is better and further explained in this paper: [Automatic syllabification for Spanish using lemmatization and derivation to solve the prefix’s prominence issue](http://dx.doi.org/10.1016/j.eswa.2013.06.056)

# Inspiration / Original source

This work is inspired by the excellent online tool [Silabeador TIP](https://tulengua.es/syllables/). This tool considers the semantics of the words and correctly separates syllables in the presence of prefixes. They also provide a C++ library that performs the naive syllable separation that *pylabeador* does. In fact, *pyleabeador* started as a Python port of that library.
