from bank import value

def test_hello_lower():
    assert value("hello") == 0

def test_hello_upper():
    assert value("Hello there") == 0

def test_h_only():
    assert value("hi") == 20
    assert value("howdy") == 20

def test_not_h():
    assert value("what's up?") == 100

def test_case_insensitivity():
    assert value("HeLLo") == 0
    assert value("Howdy") == 20
    assert value("Bye") == 100
