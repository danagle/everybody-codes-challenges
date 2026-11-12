from fractions import Fraction
from itertools import combinations
from math import floor
from pathlib import Path


def gen_notes(filepath: str) -> tuple[list[int], list[int], list[int], list[int]]:
    text = Path(filepath).read_text(encoding="utf-8").strip()
    blocks = text.split("\n\n")
    for block in blocks:
        lines = block.splitlines()
        n = list(map(int, lines[0].split(" ")[1].split(":")))
        sign = [1 if d == "CW" else -1 for d in lines[1].split(" ")[1].split(":")]
        pos = list(map(int, lines[2].split(" ")[1].split(":")))
        moves = list(map(int, lines[3].split(" ")[1].split(":")))
        yield n, sign, pos, moves


def crossings(d0, v):
    """How many times does d(t) = d0 + v*t (0 < t <= 1) hit a whole number."""
    if v == 0:
        return 0
    if d0 == 0:
        return int(abs(v))
    x = d0 + v
    if v > 0:
        return floor(x)
    return floor(-x) + 1 if x <= 0 else 0


def signals(n, sign, pos, moves):
    angle = [Fraction(p, ni) % 1 for p, ni in zip(pos, n)]
    speed = [Fraction(s, ni) for s, ni in zip(sign, n)]     # Turns per second while moving
    total = 0
    t = 0
    for stop in sorted(set(m for m in moves if m > 0)):     # Phases between consecutive stopping times
        length = stop - t
        v = [speed[i] if moves[i] >= stop else Fraction(0) for i in range(3)]  # Who moves during this phase
        for i, j in combinations(range(3), 2):
            d0 = (angle[i] - angle[j]) % 1
            total += crossings(d0, (v[i] - v[j]) * length)
        angle = [(angle[i] + v[i] * length) % 1 for i in range(3)]
        t = stop
    return total


def part1(filepath: str = "../input/everybody_codes_e2026_q13_p1.txt") -> None:
    notes_block = gen_notes(filepath)
    print("Part 1:", signals(*next(notes_block)))


def part2(filepath: str = "../input/everybody_codes_e2026_q13_p2.txt") -> None:
    total = sum(signals(*notes_block) for notes_block in gen_notes(filepath))
    print("Part 2:", total)


def part3(filepath: str = "../input/everybody_codes_e2026_q13_p3.txt") -> None:
    total = sum(signals(*notes_block) for notes_block in gen_notes(filepath))
    print("Part 3:", total)


if __name__ == "__main__":
    part1()
    part2()
    part3()
