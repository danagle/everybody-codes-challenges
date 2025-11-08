"""
The Song of Ducks and Dragons [2025]
Quest 5: Fishbone Order
https://everybody.codes/event/2025/quests/5
"""
from pathlib import Path
from typing import Iterator, List, Tuple


def read_line(filepath: str) -> Iterator[Tuple[int, List[int]]]:
    """Yield (id, numbers) pairs from file."""
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            sword_id, rest = line.split(":", 1)
            numbers = [int(x) for x in rest.split(",") if x.strip()]
            yield (int(sword_id), numbers)


def build_fishbone(numbers: List[int]) -> List[dict]:
    """Build a fishbone structure represented as a list of dict segments."""
    spine = [{"value": numbers[0], "left": None, "right": None}]
    for number in numbers[1:]:
        for segment in spine:
            if ((number < segment["value"] and segment["left"] is None) or 
                (number > segment["value"] and segment["right"] is None)):
                segment["left" if number < segment["value"] else "right"] = number
                break
        else:
            spine.append({"value": number, "left": None, "right": None})
    return spine


def get_quality(spine: List[dict]) -> int:
    """Return integer made by concatenating segment values."""
    return int("".join(str(segment["value"]) for segment in spine))


def get_levels(spine: List[dict]) -> List[int]:
    """Return a list of concatenated left/mid/right numbers per segment."""
    return [
        int("".join(
            str(x) for x in (filter(None, [segment["left"], segment["value"], segment["right"]]))
        ))
        for segment in spine
    ]


def sword_sort_key(sword: Tuple[int, int, List[int]]) -> Tuple[int, Tuple[int, ...], int]:
    """Sort by quality, levels, and id (all descending)."""
    sword_id, quality, levels = sword
    return (quality, tuple(levels), sword_id)


def part1(filepath: str):
    _, numbers = next(read_line(filepath))
    print("Part 1:", get_quality(build_fishbone(numbers)))


def part2(filepath: str):
    qualities = [get_quality(build_fishbone(numbers)) for _, numbers in read_line(filepath)]
    print("Part 2:", max(qualities) - min(qualities))


def part3(filepath: str):
    swords = [
        (sword_id, get_quality(spine := build_fishbone(numbers)), get_levels(spine))
        for sword_id, numbers in read_line(filepath)
    ]
    swords.sort(key=sword_sort_key, reverse=True)
    checksum = sum(sword_id * (index + 1) for index, (sword_id, _, _) in enumerate(swords))
    print("Part 3:", checksum)


if __name__ == "__main__":
    base = Path("../input")
    part1(base / "everybody_codes_e2025_q05_p1.txt")
    part2(base / "everybody_codes_e2025_q05_p2.txt")
    part3(base / "everybody_codes_e2025_q05_p3.txt")
