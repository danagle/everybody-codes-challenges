"""
The Song of Ducks and Dragons [2025]
Quest 2: From Complex to Clarity
https://everybody.codes/event/2025/quests/2
"""
from numba import njit, prange
from pathlib import Path
import re


def load_data(filepath: str) -> list[int, int]:
    text = Path(filepath).read_text().strip()
    return list(map(int, re.findall(r"-?\d+", text)))


@njit(inline='always')
def add(a, b):
    return [a[0] + b[0], a[1] + b[1]]


@njit(inline='always')
def multiply(a, b):
    return [a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]]


@njit(inline='always')
def divide(a, b):
    return [int(a[0] / b[0]), int(a[1] / b[1])]


def part1(filepath: str = "../input/everybody_codes_e2025_q02_p1.txt") -> None:
    A = load_data(filepath)
    
    result = [0, 0]
    for _ in range(3):
        result = multiply(result, result)  # Step 1: multiply by itself
        result = divide(result, [10, 10])  # Step 2: divide by [10,10]
        result = add(result, A)            # Step 3: add A

    print(f"Part 1: [{result[0]},{result[1]}]")


@njit(parallel=True, fastmath=True)
def compute_engraved_p2(left_x, top_y, width, height):
    engraved = 0
    for y_index in prange(height):
        y_delta = y_index * 10
        for x_index in range(width):
            x_delta = x_index * 10

            A = [left_x + x_delta, top_y + y_delta]
            result = [0, 0]
            is_engraved = True

            for _ in range(100):
                result = multiply(result, result)
                result = divide(result, [100_000, 100_000])
                result = add(result, A)
                if abs(result[0]) > 1_000_000 or abs(result[1]) > 1_000_000:
                    is_engraved = False
                    break

            if is_engraved:
                engraved += 1

    return engraved


@njit(parallel=True, fastmath=True)
def compute_engraved_p3(left_x, top_y, width, height):
    engraved = 0
    for x_delta in prange(width):
        for y_delta in range(height):
            is_engraved = True
            result = [0, 0]
            A = [left_x + x_delta, top_y + y_delta]
            for _ in range(100):
                result = multiply(result, result)
                result = divide(result, [100_000, 100_000])
                result = add(result, A)
                if abs(result[0]) > 1_000_000 or abs(result[1]) > 1_000_000:
                    is_engraved = False
                    break
            if is_engraved:
                engraved += 1
    return engraved


def part2(filepath: str = "../input/everybody_codes_e2025_q02_p2.txt") -> None:
    top_left = load_data(filepath)
    left_x, top_y = top_left
    width = height = 101

    engraved_total = compute_engraved_p2(left_x, top_y, width, height)

    print("Part 2:", engraved_total)


def part3(filepath: str = "../input/everybody_codes_e2025_q02_p3.txt") -> None:
    top_left = load_data(filepath)
    left_x, top_y = top_left
    width = height = 1001

    engraved_total = compute_engraved_p3(left_x, top_y, width, height)

    print("Part 3:", engraved_total)


if __name__ == "__main__":
    part1()
    part2()
    part3()
