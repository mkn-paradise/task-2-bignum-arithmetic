from task2 import limbs as L

M = 1 << 30

def test_from_decimal_example_from_task():
    assert L.from_decimal_magnitude("453833875923", M) == [714826195, 422]

def test_roundtrip():
    for s in ["0", "1", "453833875923", "999999999999999999999"]:
        limbs = L.from_decimal_magnitude(s, M)
        assert L.to_decimal_magnitude(limbs, M) == s

def test_roundtrip_small_base():
    """Регрессионный тест: to_decimal_magnitude должна работать и при base < 10^9,
    не только при большом base (например, 2^30)."""
#    for base in [10, 100]:
    for base in range(10, 100):
        for s in ["0", "1", "24", "28", "453833875923"]:
            limbs = L.from_decimal_magnitude(s, base)
            assert L.to_decimal_magnitude(limbs, base) == s

def test_roundtrip_wide_base_range():
    for base in list(range(2, 100)) + [1 << 30]:
        for s in ["0", "1", "9", "24", "28", "99999999999999999999999999999"]:
            limbs = L.from_decimal_magnitude(s, base)
            assert L.to_decimal_magnitude(limbs, base) == s