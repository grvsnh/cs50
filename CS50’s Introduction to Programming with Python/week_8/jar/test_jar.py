import pytest
from jar import Jar

def test_init():
    with pytest.raises(ValueError, match="Capacity must be a non-negative integer."):
        Jar(-1)
    with pytest.raises(ValueError, match="Capacity must be a non-negative integer."):
        Jar("abc")
    jar = Jar(0)
    assert jar.capacity == 0
    assert jar.size == 0
    jar = Jar(12)
    assert jar.capacity == 12
    assert jar.size == 0

def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(1)
    assert str(jar) == "🍪"
    jar.deposit(11)
    assert str(jar) == "🍪" * 12

def test_deposit():
    jar = Jar(10)
    with pytest.raises(ValueError, match="Number of cookies to deposit must be a non-negative integer."):
        jar.deposit(-1)
    with pytest.raises(ValueError, match="Number of cookies to deposit must be a non-negative integer."):
        jar.deposit(3.5)
    with pytest.raises(ValueError, match="Cannot exceed jar's capacity."):
        jar.deposit(11)
    jar.deposit(3)
    assert jar.size == 3
    jar.deposit(7)
    assert jar.size == 10

def test_withdraw():
    jar = Jar(10)
    with pytest.raises(ValueError, match="Number of cookies to withdraw must be a non-negative integer."):
        jar.withdraw(-1)
    with pytest.raises(ValueError, match="Number of cookies to withdraw must be a non-negative integer."):
        jar.withdraw("foo")
    with pytest.raises(ValueError, match="Cannot withdraw more cookies than are in the jar."):
        jar.withdraw(1)
    jar.deposit(5)
    jar.withdraw(2)
    assert jar.size == 3
    with pytest.raises(ValueError, match="Cannot withdraw more cookies than are in the jar."):
        jar.withdraw(4)
    jar.withdraw(3)
    assert jar.size == 0
