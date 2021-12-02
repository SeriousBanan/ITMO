import random
from dataclasses import dataclass
from math import ceil


@dataclass(frozen=True)
class PublicKey:
    n: int
    e: int


@dataclass(frozen=True)
class PrivateKey:
    n: int
    d: int
    p: int
    q: int


def main() -> None:
    public_key, private_key = generate_keys(8 * 4 + 1)

    print("Generated keys:\n" f"\tPublick: {public_key}\n" f"\tPrivate: {private_key}\n")

    text = b"test"
    ciphertext = encrypt(text, public_key)
    decrypted = decrypt(ciphertext, private_key)

    print(f"{text = }\n" f"{ciphertext = }\n" f"{decrypted = }\n" f"{decrypted == text = }")


def encrypt(text: bytes, public_key: PublicKey) -> bytes:
    if len(text) > (len(bin(public_key.n)[2:]) - 1) // 8:
        raise ValueError("text too long")

    x = int.from_bytes(text, "big")

    y = _my_pow(x, public_key.e, public_key.n)

    return y.to_bytes(ceil(len(bin(public_key.n)[2:]) / 8), "big")


def decrypt(ciphertext: bytes, private_key: PrivateKey) -> bytes:
    y = int.from_bytes(ciphertext, "big")

    if y >= private_key.n:
        raise ValueError("Invalid ciphertext")

    r_p = _my_pow((y % private_key.p), (private_key.d % (private_key.p - 1)), private_key.p)
    r_q = _my_pow((y % private_key.q), (private_key.d % (private_key.q - 1)), private_key.q)

    opposite_q_in_mod_p = _get_opposite(private_key.q, private_key.p)
    opposite_p_in_mod_q = _get_opposite(private_key.p, private_key.q)

    x = (
        r_p * private_key.q * opposite_q_in_mod_p + r_q * private_key.p * opposite_p_in_mod_q
    ) % private_key.n

    return x.to_bytes((len(bin(private_key.n)[2:]) - 1) // 8, "big")


def generate_keys(bits: int) -> tuple[PublicKey, PrivateKey]:
    n_min = 1 << (bits - 1)
    n_max = (1 << bits) - 1

    # Generate `p` and `q` with that it has differens of bits maximum 2.
    min_prime = 1 << (bits // 2 - 1)
    max_prime = 1 << (bits // 2 + 1)

    primes = _get_primes(min_prime, max_prime)

    while primes:
        p = random.choice(primes)
        primes.remove(p)

        if q_candidates := [q for q in primes if n_min <= p * q <= n_max]:
            q = random.choice(q_candidates)
            break
    else:
        raise ValueError("Can't generate `p` and `q` for given bits.")

    phi_n = (p - 1) * (q - 1)
    for e in range(3, phi_n, 2):
        if _gcd(phi_n, e) == 1:
            break
    else:
        raise ValueError("Can't generate `e`.")

    d = _get_opposite(e, phi_n)

    return PublicKey(p * q, e), PrivateKey(p * q, d, p, q)


def _my_pow(num: int, power: int, mod: int) -> int:
    result = 1

    while power:
        if power % 2 == 1:
            result = result * num % mod
        power //= 2
        num = num * num % mod

    return result


def _get_primes(start: int, stop: int) -> list[int]:
    primes = [2]

    for number in range(3, stop + 1, 2):
        for prime in primes:
            if number % prime == 0:
                break
        else:
            primes.append(number)

    try:
        while primes[0] < start:
            del primes[0]
    except IndexError:
        pass

    return primes


def _gcd(a: int, b: int) -> int:
    if a < b:
        a, b = b, a

    while a % b != 0:
        a, b = b, a % b

    return b


def _get_opposite(num: int, mod: int) -> int:
    g, x, _ = _gcdext(num, mod)

    if g != 1:
        raise ValueError("Opposite not exists")

    return (x % mod + mod) % mod


def _gcdext(a: int, b: int) -> tuple[int, int, int]:
    if a == 0:
        return b, 0, 1

    g, x1, y1 = _gcdext(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


if __name__ == "__main__":
    main()
