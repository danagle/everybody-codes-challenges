"""
The Entertainment Hub [ No. 2 ]
Quest 2: The Pocket-Money Popper
https://everybody.codes/story/2/quests/2
"""
from collections import deque
from itertools import cycle
from pathlib import Path


def part1(filepath: str = "../../input/everybody_codes_e2_q02_p1.txt") -> None:
    balloons = list(Path(filepath).read_text().strip())
    fluffbolts = "RGB"

    shots_taken = 0
    fluffbolt_iterator = cycle(fluffbolts)
    current_bolt = next(fluffbolt_iterator)

    for balloon in balloons:
        if current_bolt != balloon:
            shots_taken += 1
            current_bolt = next(fluffbolt_iterator)

    print("Part 1:", shots_taken)


def count_shots(balloons: list[str]) -> int:
    left = deque(balloons[:len(balloons) // 2])
    right = deque(balloons[len(balloons) // 2 :])

    fluffbolt_iterator = cycle("RGB")
    shots = 0
    while right or left:
        color = next(fluffbolt_iterator)

        if len(left) > len(right):
            left.popleft()
        elif len(right) > len(left):
            left.append(right.popleft())
            left.popleft()
        else:
            if left[0] == color:
                right.popleft()
            left.popleft()

        shots += 1

    return shots


def part2(filepath: str = "../../input/everybody_codes_e2_q02_p2.txt"):
    balloons = list(Path(filepath).read_text().strip())

    repeat = 100
    shots = count_shots(balloons * repeat)

    print("Part 2:", shots)


def part3(filepath: str = "../../input/everybody_codes_e2_q02_p3.txt"):
    balloons = list(Path(filepath).read_text().strip())

    repeat = 100_000
    shots = count_shots(balloons * repeat)

    print("Part 3:", shots)
    

if __name__ == "__main__":
    part1()
    part2()
    part3()
