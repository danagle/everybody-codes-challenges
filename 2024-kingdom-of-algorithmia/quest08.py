"""
The Kingdom of Algorithmia [2024]
Quest 8: A Shrine for Nullpointer
https://everybody.codes/event/2024/quests/8
"""
from itertools import count
from pathlib import Path

def read_input(filepath: str) -> int:
    """Read and parse the single integer value from a part's input file."""
    return int(Path(filepath).read_text().strip())


def part1(filepath: str = "../input/everybody_codes_e2024_q08_p1.txt") -> None:
    """
    Build rows of increasing odd widths (1, 3, 5, 7, ...)
    until the total number of blocks equals or exceeds the target.
    The missing part is multiplied by the current width to form the answer.
    """
    target = read_input(filepath)

    total = 0
    for width in count(1, 2):  # 1, 3, 5, ...
        total += width
        if total >= target:
            break

    missing = total - target
    result = width * missing

    print(f"Part 1: {result}")


def part2(filepath: str = "../input/everybody_codes_e2024_q08_p2.txt") -> None:
    """
    Each row's “thickness” evolves with each step.
    The thickness grows as (thickness * priests) % acolytes.
    Stop once total >= marble blocks.
    """
    priests = read_input(filepath)
    acolytes, marble_blocks = 1111, 20240000  # Given constants
    total = 0
    thickness = 1

    for width in count(1, 2):
        total += thickness * width
        thickness = (thickness * priests) % acolytes
        if total >= marble_blocks:
            break

    missing = total - marble_blocks
    result = missing * width

    print(f"Part 2: {result}")


def part3(filepath: str = "../input/everybody_codes_e2024_q08_p3.txt") -> None:
    """
    More complex architecture with “empty” adjustments.
    - Each new row adds a column.
    - Every column's height increases by the current thickness.
    - The "empty" value for each column is derived from (high priests * width * height) % acolytes.
    - The total area is computed as (sum(remaining)*2 - first_remaining).
    The process repeats until total >= blocks.
    """
    high_priests = read_input(filepath)
    acolytes, blocks = 10, 202400000  # Given constants
    thickness = 1
    total = 0
    column_heights = []

    for width in count(1, 2):
        # Add a new column
        column_heights.append(0)

        # Increase all column heights by current thickness
        column_heights = [height + thickness for height in column_heights]

        # Compute "empty" cells per column
        empty = [(high_priests * width * height) % acolytes for height in column_heights]
        empty[-1] = 0  # Last column has no empty space

        # Remaining filled cells
        remaining = [h - e for h, e in zip(column_heights, empty)]

        # Compute total area
        total = sum(remaining) * 2 - remaining[0]

        # Update thickness
        thickness = (thickness * high_priests) % acolytes + acolytes

        if total >= blocks:
            break

    result = total - blocks

    print(f"Part 3: {result}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
