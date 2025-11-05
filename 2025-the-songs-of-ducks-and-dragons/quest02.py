"""
The Song of Ducks and Dragons [2025]
Quest 2: From Complex to Clarity
https://everybody.codes/event/2025/quests/2
"""
from pathlib import Path
import re


def load_data(filepath: str):
    text = Path(filepath).read_text().strip()
    return tuple(map(int, re.findall(r"-?\d+", text)))


def complex_add(a, b):
    """Add two 'complex' numbers [X1, Y1] and [X2, Y2]."""
    X1, Y1 = a
    X2, Y2 = b
    return [X1 + X2, Y1 + Y2]


def complex_mul(a, b):
    """Multiply two 'complex' numbers [X1, Y1] and [X2, Y2]."""
    X1, Y1 = a
    X2, Y2 = b
    return [X1 * X2 - Y1 * Y2, X1 * Y2 + Y1 * X2]


def complex_div(a, b):
    """Divide two 'complex' numbers [X1, Y1] / [X2, Y2], keeping only integer parts."""
    X1, Y1 = a
    X2, Y2 = b
    return [int(X1 / X2), int(Y1 / Y2)]


def part1(filepath: str = "../input/everybody_codes_e2025_q02_p1.txt"):
    A = load_data(filepath)
    
    result = [0, 0]
    for _ in range(3):
        result = complex_mul(result, result)   # Step 1: multiply by itself
        result = complex_div(result, [10, 10]) # Step 2: divide by [10,10]
        result = complex_add(result, A)        # Step 3: add A

    print("Part 1:", result)


def engrave_point(point):
    res = [0,0]
    for _ in range(100):
        res = complex_mul(res,res)
        res = complex_div(res, [100000, 100000])
        res = complex_add(res,point)
        if -1000000 <= res[0] <= 1000000 >= res[1] >= -1000000:
            continue
        return False
    return True


def part2(filepath: str = "../input/everybody_codes_e2025_q02_p2.txt"):
    top_left = load_data(filepath)
    bottom_right = complex_add(top_left, [1000,1000])

    engraved_total = 0
    left_x, top_y = top_left
    right_x, bottom_y = bottom_right
    for y in range(top_y, bottom_y+1, 10):
        for x in range(left_x, right_x+1, 10):
            if engrave_point([x,y]):
                engraved_total += 1

    print("Part 2:", engraved_total)


def part3(filepath: str = "../input/everybody_codes_e2025_q02_p3.txt"):
    top_left = load_data(filepath)
    bottom_right = complex_add(top_left, [1000,1000])

    engraved_total = 0
    left_x, top_y = top_left
    right_x, bottom_y = bottom_right
    for y in range(top_y, bottom_y+1):
        for x in range(left_x, right_x+1):
            if engrave_point([x,y]):
                engraved_total += 1

    print("Part 3:", engraved_total)


if __name__ == "__main__":
    part1()
    part2()
    part3()
