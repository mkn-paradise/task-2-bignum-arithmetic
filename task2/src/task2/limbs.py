"""Арифметика над модулями длинных чисел, представленных как списки лимбов
в системе счисления с основанием `base` (лимб i хранит цифру при base**i)."""


def strip(limbs: list[int]) -> list[int]:
    while len(limbs) > 1 and limbs[-1] == 0:
        limbs.pop()
    return limbs


def cmp_mag(a: list[int], b: list[int]) -> int:
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    for i in range(len(a) - 1, -1, -1):
        if a[i] != b[i]:
            return -1 if a[i] < b[i] else 1
    return 0


def add_mag(a: list[int], b: list[int], base: int) -> list[int]:
    result = []
    carry = 0
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else 0
        y = b[i] if i < len(b) else 0
        s = x + y + carry
        result.append(s % base)
        carry = s // base
    if carry:
        result.append(carry)
    return strip(result)


def sub_mag(a: list[int], b: list[int], base: int) -> list[int]:
    """Требует |a| >= |b|."""
    result = []
    borrow = 0
    for i in range(len(a)):
        y = b[i] if i < len(b) else 0
        d = a[i] - y - borrow
        if d < 0:
            d += base
            borrow = 1
        else:
            borrow = 0
        result.append(d)
    return strip(result)


def mul_mag(a: list[int], b: list[int], base: int) -> list[int]:
    result = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        if x == 0:
            continue
        carry = 0
        for j, y in enumerate(b):
            cur = result[i + j] + x * y + carry
            result[i + j] = cur % base
            carry = cur // base
        k = i + len(b)
        while carry:
            cur = result[k] + carry
            result[k] = cur % base
            carry = cur // base
            k += 1
    return strip(result)


def mul_small(a: list[int], word: int, base: int) -> list[int]:
    """Умножение на «слово» 0 <= word < base — используется при делении."""
    result = []
    carry = 0
    for x in a:
        cur = x * word + carry
        result.append(cur % base)
        carry = cur // base
    if carry:
        result.append(carry)
    return strip(result)


def divmod_mag(a: list[int], b: list[int], base: int) -> tuple[list[int], list[int]]:
    if cmp_mag(b, [0]) == 0:
        raise ZeroDivisionError("division by zero")
    if cmp_mag(a, b) < 0:
        return [0], a[:]

    quotient = [0] * len(a)
    rem = [0]
    for i in range(len(a) - 1, -1, -1):
        rem = strip([a[i]] + rem)
        lo, hi = 0, base - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if cmp_mag(mul_small(b, mid, base), rem) <= 0:
                lo = mid
            else:
                hi = mid - 1
        quotient[i] = lo
        rem = sub_mag(rem, mul_small(b, lo, base), base)
    return strip(quotient), rem


def from_decimal_magnitude(digits: str, base: int) -> list[int]:
    """Строка десятичных цифр -> лимбы, слева направо: limbs = limbs*10 + digit."""
    limbs = [0]
    for ch in digits:
        d = int(ch)
        carry = d
        for i in range(len(limbs)):
            cur = limbs[i] * 10 + carry
            limbs[i] = cur % base
            carry = cur // base
        if carry:
            limbs.append(carry)
    return strip(limbs)


def to_decimal_magnitude(limbs: list[int], base: int) -> str:
    """Лимбы -> строка десятичных цифр, кусками по 9 цифр (10^9 < 2^30)."""
    if cmp_mag(limbs, [0]) == 0:
        return "0"
    chunk = 1_000_000_000
    chunks = []
    cur = limbs[:]
    while cmp_mag(cur, [0]) != 0:
        cur, rem_limbs = divmod_mag(cur, [chunk], base)
        chunks.append(rem_limbs[0] if rem_limbs else 0)
    chunks_str = [str(chunks[0])] + [f"{c:09d}" for c in chunks[1:]]
    return "".join(reversed(chunks_str))