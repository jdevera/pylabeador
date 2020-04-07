# Pylabeador: Automatic Syllabification of Spanish Words

```python
>>> import pylabeador
>>> pylabeador.syllabify("silabear")
['si', 'la', 'be', 'ar']
```

# Accuracy

Automatic syllabification without additional lexical or and semantic *knowledge* of the words can only go so far.  This syllabifier does not have such knowledge. Because of this, words such as *transatlántico*, whose correct hyphenation is *trans-a-tlán-ti-co* or even *trans-at-lán-ti-co*, end up being divided here into *tran-sa-tlán-ti-co*.  To hyphenate this correctly, it is necessary to know that the word without the prefix exists in Spanish with similar semantics to the one of the original word. This is better and further explained in this paper: [Automatic syllabification for Spanish using lemmatization and derivation to solve the prefix’s prominence issue](http://dx.doi.org/10.1016/j.eswa.2013.06.056)

# Inspiration / Original source

This works is inspired by the excellent online tool [Silabeador TIP](https://tulengua.es/syllables/). This tool considers the semantics of the words and correctly separates syllables in the presence of prefixes. As a side, they also provide a C++ library that performs the naive syllable separation that pylabeador does. In fact, pyleabeador started as a python port of that library.
