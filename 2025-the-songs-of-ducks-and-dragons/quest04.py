"""
The Song of Ducks and Dragons [2025]
Quest 4: Teeth of the Wind
https://everybody.codes/event/2025/quests/4
"""
from math import ceil, floor
from pathlib import Path


def load_data(filepath: str, has_common_shafts: bool = False) -> list[int]:
    if has_common_shafts:
            return [tuple(map(int, line.split("|"))) for line in Path(filepath).read_text().strip().splitlines()]
    return [int(n) for n in Path(filepath).read_text().strip().splitlines()]


def part1(filepath: str = "../input/everybody_codes_e2025_q04_p1.txt") -> None:
    gears = load_data(filepath)
    
    result = floor(2025 * gears[0] / gears[-1])

    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2025_q04_p2.txt") -> None:
    gears = load_data(filepath)

    result = ceil(10000000000000 * gears[-1] / gears[0])

    print("Part 2:", result)


def part3(filepath: str = "../input/everybody_codes_e2025_q04_p3.txt") -> None:
    gears = load_data(filepath, True)
    speed = 1
    
    (start_gear,), *between, (end_gear,) = gears
    for gear in between:
        speed *= gear[1] / gear[0]

    result = floor(100 * speed * start_gear / end_gear)

    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
