"""
The Song of Ducks and Dragons [2025]
Quest 4: Teeth of the Wind
https://everybody.codes/event/2025/quests/4
"""
from math import ceil
from pathlib import Path


def load_data(filepath: str, has_common_shafts: bool = False) -> list[int]:
    """Read the list of numbers corresponding to the number of gear teeth from input file."""
    # Part 3: There are gears mounted on common shafts
    if has_common_shafts:
        return [tuple(map(int, line.split("|")))
                for line in Path(filepath).read_text(encoding="utf-8").strip().splitlines()]
    # Parts 1 & 2
    return [int(n) for n in Path(filepath).read_text(encoding="utf-8").strip().splitlines()]


def part1(filepath: str = "../input/everybody_codes_e2025_q04_p1.txt") -> None:
    """
    How many full turns will the last gear make if the first one turns exactly 2025 times?
    """
    gears = load_data(filepath)

    result = int(2025 * gears[0] / gears[-1])

    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2025_q04_p2.txt") -> None:
    """
    What is the minimum number of full turns for the first gear, 
    after which the last one turns at least 10,000,000,000,000 times?
    """
    gears = load_data(filepath)

    result = ceil(10_000_000_000_000 * gears[-1] / gears[0])

    print("Part 2:", result)


def part3(filepath: str = "../input/everybody_codes_e2025_q04_p3.txt") -> None:
    """How many full turns will the last gear make if the first one turns exactly 100 times?"""
    gears = load_data(filepath, True)
    ratio = 1

    (start_gear,), *middle, (end_gear,) = gears
    for gear in middle:
        ratio *= gear[1] / gear[0]

    result = int(100 * ratio * start_gear / end_gear)

    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
