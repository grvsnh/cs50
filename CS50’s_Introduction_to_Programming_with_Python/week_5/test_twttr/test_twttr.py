from twttr import shorten

def test_empty():
    assert shorten("") == ""

def test_all_vowels_lowercase():
    assert shorten("aeiou") == ""

def test_all_vowels_uppercase():
    assert shorten("AEIOU") == ""

def test_mixed_case():
    assert shorten("ApPlE") == "pPl"

def test_no_vowels():
    assert shorten("rhythm") == "rhythm"

def test_mixed_characters():
    assert shorten("CS50!") == "CS50!"

def test_sentence():
    assert shorten("Hello, World!") == "Hll, Wrld!"
