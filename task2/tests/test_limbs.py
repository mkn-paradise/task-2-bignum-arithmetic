from task2 import limbs as L

M = 1 << 30

def test_from_decimal_example_from_task():
    assert L.from_decimal_magnitude("453833875923", M) == [714826195, 422]

def test_roundtrip():
    for s in ["0", "1", "453833875923", "999999999999999999999"]:
        limbs = L.from_decimal_magnitude(s, M)
        assert L.to_decimal_magnitude(limbs, M) == s