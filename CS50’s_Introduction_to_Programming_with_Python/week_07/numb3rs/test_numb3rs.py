from numb3rs import validate


def test_valid_ips():
    assert validate("127.0.0.1") is True
    assert validate("192.168.1.1") is True
    assert validate("255.255.255.255") is True
    assert validate("0.0.0.0") is True
    assert validate("10.10.10.10") is True


def test_invalid_num_parts():
    assert validate("127.0.0") is False
    assert validate("127.0.0.1.1") is False
    assert validate("") is False


def test_invalid_characters():
    assert validate("cat") is False
    assert validate("1.2.3.a") is False
    assert validate("a.b.c.d") is False


def test_out_of_range_numbers():
    assert validate("256.256.256.256") is False
    assert validate("999.0.0.0") is False
    assert validate("0.0.0.256") is False
    assert validate("-1.0.0.0") is False


def test_leading_zeros():
    assert validate("192.168.01.1") is False
    assert validate("192.168.001.1") is False
    assert validate("01.02.03.04") is False
    assert validate("0.0.0.0") is True
