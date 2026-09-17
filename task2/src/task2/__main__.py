from task2.bignum import BigInt

# M = 1 << 30   # основание системы счисления
# N = 8         # максимальная разрядность (число лимбов)


def main() -> None:
    M = int(input("Введите систему счисления M для длинной арифметики: "))
    N = int(input("Введите разрядность N для M-ичной системы счисления: "))
    a = BigInt.from_str(input("a = "), M, N)
    b = BigInt.from_str(input("b = "), M, N)
    print(f"a + b = {(a + b).to_str()}")
    print(f"a - b = {(a - b).to_str()}")
    print(f"a * b = {(a * b).to_str()}")
    q, r = a.divmod(b)
    print(f"a // b = {q.to_str()}, a % b = {r.to_str()}")


if __name__ == "__main__":
    main()