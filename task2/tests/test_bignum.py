import pytest
from task2.bignum import BigInt, BigNumOverflow

M, N = 1 << 30, 4

def bi(s): return BigInt.from_str(s, M, N)

def test_add_sub_mul():
    a, b = bi("123456789"), bi("987654321")
    assert (a + b).to_str() == "1111111110"
    assert (a - b).to_str() == "-864197532"
    assert (a * b).to_str() == str(123456789 * 987654321)

def test_overflow():
    huge = "9" * 300  # заведомо больше, чем влезет в N=4 лимба по 30 бит
    with pytest.raises(BigNumOverflow):
        bi(huge)

def test_incompatible_systems():
    a = BigInt.from_str("5", M, N)
    b = BigInt.from_str("5", M, N + 1)
    with pytest.raises(ValueError):
        a + b