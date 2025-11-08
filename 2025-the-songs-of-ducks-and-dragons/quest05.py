"""
The Song of Ducks and Dragons [2025]
Quest 5: Fishbone Order
https://everybody.codes/event/2025/quests/5
"""
from pathlib import Path
from typing import List, Tuple


class Segment:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def parse_line(line: str) -> Tuple[int, List[int]]:
    """Parse 'id:nums' line into (id, numbers)."""
    line = line.strip()
    if not line:
        return 0, []
    sword_id, rest = line.split(':', 1)
    numbers = [int(x) for x in rest.split(',') if x.strip()]
    return int(sword_id), numbers


def build_fishbone(numbers: List[int]) -> List[Segment]:
    """Constructs the spine of the fishbone."""
    if not numbers:
        return []
    spine = [Segment(numbers[0])]
    for num in numbers[1:]:
        placed = False
        for seg in spine:
            if num < seg.value and seg.left is None:
                seg.left = num
                placed = True
                break
            elif num > seg.value and seg.right is None:
                seg.right = num
                placed = True
                break
        if not placed:
            spine.append(Segment(num))
    return spine


def get_quality(spine: List[Segment]) -> int:
    """Concatenate spine values."""
    return int(''.join(str(seg.value) for seg in spine))


def get_levels(spine: List[Segment]) -> List[int]:
    """Return list of 'level numbers' concatenating left, mid, right for each segment."""
    levels = []
    for seg in spine:
        parts = []
        if seg.left is not None:
            parts.append(str(seg.left))
        parts.append(str(seg.value))
        if seg.right is not None:
            parts.append(str(seg.right))
        levels.append(int(''.join(parts)))
    return levels


def sword_key(sword):
    """Return sorting key tuple for a sword."""
    sword_id, quality, levels = sword
    # Sort: quality desc, levels desc, id desc
    return (quality, levels, sword_id)


def part1(filepath: str = "../input/everybody_codes_e2025_q05_p1.txt") -> None:
    line = Path(filepath).read_text().strip()
    
    _, numbers = parse_line(line)
    spine = build_fishbone(numbers)
    result = get_quality(spine)

    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2025_q05_p2.txt") -> None:
    """Read all swords from file and determine the difference between min_quality and max_quality."""
    qualities = []
    
    for line in Path(filepath).read_text().strip().splitlines():
        _, numbers = parse_line(line)
        spine = build_fishbone(numbers)
        q = get_quality(spine)
        qualities.append(q)

    result = max(qualities) - min(qualities)

    print("Part 2:", result)


def part3(filepath: str = "../input/everybody_codes_e2025_q05_p3.txt") -> None:
    """Reads swords, builds fishbones, sorts, and computes checksum."""
    swords = []

    for line in Path(filepath).read_text().strip().splitlines():
        sword_id, numbers = parse_line(line)
        spine = build_fishbone(numbers)
        quality = get_quality(spine)
        levels = get_levels(spine)
        swords.append((sword_id, quality, levels))

    # Sort by quality, levels, id (all descending)
    swords.sort(key=sword_key, reverse=True)

    # Compute checksum: sum(id * position)
    result = sum(sword_id * (i + 1) for i, (sword_id, _, _) in enumerate(swords))

    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
