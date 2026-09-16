from task2 import limbs as L


class BigNumOverflow(Exception):
    """Число не помещается в N лимбов при выбранном основании M."""


class BigInt:
    """Длинное целое число в системе счисления с основанием M и максимум N лимбами."""

    __slots__ = ("sign", "limbs", "M", "N")

    def __init__(self, sign: int, raw_limbs: list[int], M: int, N: int):
        stripped = L.strip(raw_limbs)
        if len(stripped) > N:
            raise BigNumOverflow(f"number requires {len(stripped)} limbs, but N={N}")
        self.M = M
        self.N = N
        self.limbs = stripped
        self.sign = 0 if L.cmp_mag(self.limbs, [0]) == 0 else sign

    def _check_compatible(self, other: "BigInt") -> None:
        if self.M != other.M or self.N != other.N:
            raise ValueError(
                f"incompatible number systems: "
                f"(M={self.M}, N={self.N}) vs (M={other.M}, N={other.N})"
            )

    @classmethod
    def from_str(cls, s: str, M: int, N: int) -> "BigInt":
        s = s.strip()
        sign = 1
        if s and s[0] in "+-":
            sign = -1 if s[0] == "-" else 1
            s = s[1:]
        if not s or not s.isdigit():
            raise ValueError(f"invalid integer literal: {s!r}")
        raw_limbs = L.from_decimal_magnitude(s, M)
        return cls(sign, raw_limbs, M, N)

    def to_str(self) -> str:
        body = L.to_decimal_magnitude(self.limbs, self.M)
        return ("-" + body) if self.sign < 0 else body

    def __repr__(self) -> str:
        return f"BigInt({self.to_str()!r}, M={self.M}, N={self.N})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BigInt):
            return NotImplemented
        return self.sign == other.sign and self.limbs == other.limbs

    def __add__(self, other: "BigInt") -> "BigInt":
        self._check_compatible(other)
        if self.sign == 0:
            return other
        if other.sign == 0:
            return self
        if self.sign == other.sign:
            return BigInt(self.sign, L.add_mag(self.limbs, other.limbs, self.M), self.M, self.N)
        cmp = L.cmp_mag(self.limbs, other.limbs)
        if cmp == 0:
            return BigInt(0, [0], self.M, self.N)
        if cmp > 0:
            return BigInt(self.sign, L.sub_mag(self.limbs, other.limbs, self.M), self.M, self.N)
        return BigInt(other.sign, L.sub_mag(other.limbs, self.limbs, self.M), self.M, self.N)

    def __neg__(self) -> "BigInt":
        return BigInt(-self.sign, self.limbs[:], self.M, self.N)

    def __sub__(self, other: "BigInt") -> "BigInt":
        self._check_compatible(other)
        return self + (-other)

    def __mul__(self, other: "BigInt") -> "BigInt":
        self._check_compatible(other)
        if self.sign == 0 or other.sign == 0:
            return BigInt(0, [0], self.M, self.N)
        result_limbs = L.mul_mag(self.limbs, other.limbs, self.M)
        return BigInt(self.sign * other.sign, result_limbs, self.M, self.N)

    def divmod(self, other: "BigInt") -> tuple["BigInt", "BigInt"]:
        """Целочисленное деление и остаток (усечение к нулю)."""
        self._check_compatible(other)
        q_limbs, r_limbs = L.divmod_mag(self.limbs, other.limbs, self.M)
        q_sign = self.sign * other.sign if L.cmp_mag(q_limbs, [0]) != 0 else 0
        r_sign = self.sign if L.cmp_mag(r_limbs, [0]) != 0 else 0
        return (
            BigInt(q_sign, q_limbs, self.M, self.N),
            BigInt(r_sign, r_limbs, self.M, self.N),
        )

    def __floordiv__(self, other: "BigInt") -> "BigInt":
        return self.divmod(other)[0]

    def __mod__(self, other: "BigInt") -> "BigInt":
        return self.divmod(other)[1]