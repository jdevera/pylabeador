from pylabeador.pylabeador import WordProgress

def test_end():
    w = WordProgress("radio")
    w.pos = 3
    assert w.char == 'i'
    next = w.next()
    assert next == 'o'
    assert w.char == 'o'
    assert not w.ended
    assert w.one_ahead is None

def test_lookahead():
    w = WordProgress("que")
    assert w.char == 'q'
    assert w.one_ahead == 'u'
    w.next()
    assert w.char == 'u'
    assert w.one_ahead == 'e'