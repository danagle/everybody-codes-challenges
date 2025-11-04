"""
Echoes of Enigmatus [ No. 1 ]
Quest 3: The Conical Snail Clock
https://everybody.codes/story/1/quests/3
"""
from itertools import count
import math
from pathlib import Path
import re


def part1(filepath: str = "../../input/everybody_codes_e1_q03_p1.txt"):
    lines = Path(filepath).read_text().strip().splitlines()

    result = 0
    for line in lines:
        x, y = (int(x) for x in re.findall(r"-?[0-9]+", line))

        for _ in range(100):
            x += 1
            y -= 1
            if y == 0:
                y = x - y - 1
                x = 1

        result += x + 100 * y

    print("Part 1:", result)


def chinese_remainder(length, offset):
    #total = 0
    #prod = math.prod(length)
    #for length_i, offset_i in zip(length, offset):
    #    p = prod // length_i
    #    total += offset_i * pow(p, -1, length_i) * p
    #return total % prod
    N = math.prod(length)
    return sum(oi * (N//ni) * pow(N//ni, -1, ni) 
               for ni, oi in zip(length, offset)) % N


def part2(part_num: int = 2, filepath: str = "../../input/everybody_codes_e1_q03_p2.txt"):
    cycle_lengths, offsets = [], []
    lines = Path(filepath).read_text().strip().splitlines()

    for line in lines:
        x, y = (int(x) for x in re.findall(r"-?[0-9]+", line))

        cycle_start = None
        for day in count():
            if y == 1:
                if cycle_start is None:
                    cycle_start = day
                else:
                    break
            x += 1
            y -= 1
            if y == 0:
                y = x - y - 1
                x = 1

        assert cycle_start is not None
        cycle_length = day - cycle_start

        cycle_lengths.append(cycle_length)
        offsets.append(cycle_start)

    result = chinese_remainder(cycle_lengths, offsets)

    print(f"Part {part_num}:", result)


if __name__ == "__main__":
    part1()
    part2()
    part2(3, "../../input/everybody_codes_e1_q03_p3.txt")
