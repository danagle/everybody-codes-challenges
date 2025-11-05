"""
The Song of Ducks and Dragons [2025]
Quest 3: The Deepest Fit
https://everybody.codes/event/2025/quests/3
"""
from collections import Counter
from pathlib import Path


def load_data(filepath: str) -> list[int, int]:
    text = Path(filepath).read_text().strip()
    return [int(n) for n in text.split(',')]


def part1(filepath: str = "../input/everybody_codes_e2025_q03_p1.txt") -> None:
    notes = load_data(filepath)
    result = sum(set(notes))

    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2025_q03_p2.txt") -> None:
    notes = load_data(filepath)
    result = sum(sorted(set(notes))[:20])

    print("Part 2:", result)
    

def part3(filepath: str = "../input/everybody_codes_e2025_q03_p3.txt") -> None:
    notes = load_data(filepath)
    _, result = Counter(notes).most_common(1)[0]

    print("Part 3:", result)      


if __name__ == "__main__":
    part1()
    part2()
    part3()
