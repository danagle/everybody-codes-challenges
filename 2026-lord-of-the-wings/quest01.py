import math
from pathlib import Path


def load_notes(filepath: str):
    text = Path(filepath).read_text(encoding="utf-8").strip()
    return tuple(map(int, text.split(",")))


def part1(filepath: str = "../input/everybody_codes_e2026_q01_p1.txt") -> None:
    numbers = load_notes(filepath)

    def rule(cones: int) -> int:
        side = math.isqrt(cones - 1) + 1
        return side * side - cones

    print("Part 1:", sum(rule(cones) for cones in numbers))


def part2(filepath: str = "../input/everybody_codes_e2026_q01_p2.txt") -> None:
    numbers = load_notes(filepath)

    def rule(cones: int) -> int:
        side = max((cones + 3) // 4, 2)
        return 4 * side - cones

    print("Part 2:", sum(rule(cones) for cones in numbers))


def part3(filepath: str = "../input/everybody_codes_e2026_q01_p3.txt") -> None:
    numbers = load_notes(filepath)

    def rule(cones: int) -> int:
        side = (math.isqrt(cones) + 1) | 1
        return side * side - cones - 1

    print("Part 3:", sum(rule(cones) for cones in numbers))


if __name__ == "__main__":
    part1()
    part2()
    part3()
