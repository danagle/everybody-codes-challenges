"""
The Song of Ducks and Dragons [2025]
Quest 2: From Complex to Clarity
https://everybody.codes/event/2025/quests/2
"""
from pathlib import Path
import re
from numba import njit, prange


def load_data(filepath: str) -> complex:
    """Read the coordinates of the point A from the input file."""
    text = Path(filepath).read_text(encoding="utf-8").strip()
    return tuple(map(int, re.findall(r"-?\d+", text)))


def part1(filepath: str = "../input/everybody_codes_e2025_q02_p1.txt") -> None:
    """
    What number will you get at the end of the process?
    The answer is a "complex" number, written in square brackets as [X,Y] without any spaces.
    """
    point = load_data(filepath)
    px, py = point
    zx, zy = 0, 0
    for _ in range(3):
        # multiply z by itself: (zx + i zy)^2 = (zx^2 - zy^2) + i(2*zx*zy)
        x2 = zx * zx - zy * zy
        y2 = 2 * zx * zy
        # component-wise divide with truncation toward zero
        # NOTE: int(x / 10) in Python truncates toward zero, not floor
        zx = int(x2 / 10) + px
        zy = int(y2 / 10) + py

    print(f"Part 1: [{zx},{zy}]")


@njit
def engrave_point(point: tuple[int, int]) -> bool:
    """Determine if `point` is to be engraved by performing 100 cycles of the steps."""
    px, py = point
    zx, zy = 0, 0
    for _ in range(100):
        x2 = zx * zx - zy * zy
        y2 = 2 * zx * zy
        zx = int(x2 / 100_000) + px
        zy = int(y2 / 100_000) + py
        # check bounds
        if -1_000_000 <= zx <= 1_000_000 and -1_000_000 <= zy <= 1_000_000:
            continue
        return False
    return True


def part2(filepath: str = "../input/everybody_codes_e2025_q02_p2.txt") -> None:
    """How many points will be engraved according to the blacksmith’s plan?"""
    top_left = load_data(filepath)
    left_x, top_y = top_left
    right_x, bottom_y = left_x + 1000, top_y + 1000
    engraved_total = 0

    for y in range(top_y, bottom_y+1, 10):
        for x in range(left_x, right_x+1, 10):
            if engrave_point((x, y)):
                engraved_total += 1

    print("Part 2:", engraved_total)


def part3(filepath: str = "../input/everybody_codes_e2025_q02_p3.txt") -> None:
    """What is the number of points you plan to engrave?"""
    top_left = load_data(filepath)
    left_x, top_y = top_left
    right_x, bottom_y = left_x + 1000, top_y + 1000

    engraved_total = 0
    for y in prange(top_y, bottom_y + 1):
        for x in range(left_x, right_x + 1):
            if engrave_point((x, y)):
                engraved_total += 1

    print("Part 3:", engraved_total)


if __name__ == "__main__":
    part1()
    part2()
    part3()
