[![](https://img.shields.io/github/actions/workflow/status/jdevera/pylabeador/ci.yml?branch=main)](https://github.com/jdevera/pylabeador/actions?query=workflow%3A%22Python+package%22+branch%3Amain)
[![codecov](https://codecov.io/gh/jdevera/pylabeador/branch/master/graph/badge.svg)](https://codecov.io/gh/jdevera/pylabeador)
![](https://img.shields.io/pypi/pyversions/pylabeador)
[![](https://img.shields.io/pypi/v/pylabeador)](https://pypi.org/project/pylabeador/)
![](https://img.shields.io/pypi/l/pylabeador)
![](https://img.shields.io/pypi/dm/pylabeador)

# Pylabeador: Silabación Automática de Palabras en Español

[English](README.md) | [Español](README.es.md)


## Instalación

```
pip install pylabeador
```

## Uso

Lo puedes usar como una librería de Python:

```python
>>> import pylabeador
>>> pylabeador.syllabify("silabear")
['si', 'la', 'be', 'ar']
```

Y lo puedes usar como una herramienta en la línea de comandos:

```sh
$ pylabeador interesante
in-te-re-san-te
```

## Precisión

La silabación automática sin conocimiento léxico o semántico adicional de las palabras solo puede llegar hasta cierto punto. Este silabeador no tiene tal conocimiento. Por esta razón, palabras como *transatlántico*, cuya silabación correcta es *trans-a-tlán-ti-co* o incluso *trans-at-lán-ti-co*, terminan siendo divididas aquí en *tran-sa-tlán-ti-co*. Para separar esto en silabas correctamente, es necesario saber que la palabra sin el prefijo existe en español con semántica similar a la de la palabra original. Esto se explica mejor y más detalladamente en este artículo: [Automatic syllabification for Spanish using lemmatization and derivation to solve the prefix's prominence issue](http://dx.doi.org/10.1016/j.eswa.2013.06.056)

## Inspiración / Fuente original

Este trabajo está inspirado en la excelente herramienta online [Silabeador TIP](https://tulengua.es/syllables/). Esta herramienta considera la semántica de las palabras y separa correctamente las sílabas en presencia de prefijos. También proporcionan una librería en C++ que lleva a cabo la separación de sílabas *ingenua* que `pylabeador` hace. De hecho, *pylabeador* comenzó como una reescritura en Python de esa librería.