"""
The Song of Ducks and Dragons [2025]
Quest 8: The Art of Connection
https://everybody.codes/event/2025/quests/8
"""
from itertools import combinations, pairwise
from pathlib import Path


def load_data(filepath: str) -> complex:
    return [int(s) for s in Path(filepath).read_text().strip().split(",")]


def part1(filepath: str = "../input/everybody_codes_e2025_q08_p1.txt") -> None:
    sequence = load_data(filepath)
    total = sum(((a - b) % 16 == 0) for a, b in pairwise(sequence))

    print(f"Part 1: {total}")


def between(a, b, x):
    """Return True if x is between a and b clockwise on the circle."""
    if a == b:
        return False
    if a < b:
        return a < x < b
    # Wrap-around case
    return x > a or x < b


def intersects(chord1, chord2):
    """Return True if chords intersect inside the circle."""
    a, b = chord1
    c, d = chord2
    # Skip if any endpoints coincide
    if len({a, b, c, d}) < 4:
        return False
    # Chords intersect if endpoints separate each other
    return (between(a, b, c) != between(a, b, d)) and (between(c, d, a) != between(c, d, b))


def part2(filepath: str = "../input/everybody_codes_e2025_q08_p2.txt"):
    sequence = load_data(filepath)
    chords = [(a, b) for a, b in pairwise(sequence)]

    total = sum(
        intersects(chords[i], chords[j])
        for i in range(len(chords))
        for j in range(i + 1, len(chords))
    )

    print("Part 2:", total)


def part3(filepath = "../input/everybody_codes_e2025_q08_p3.txt"):
    sequence = load_data(filepath)
    chords = [(a, b) for a, b in pairwise(sequence)]
    num_points = 256
    max_crosses = 0

    for a, b in combinations(range(1, num_points + 1), 2):
        cross_count = sum(intersects((a, b), chord) for chord in chords)
        if cross_count > max_crosses:
            max_crosses = cross_count

    print("Part 3:", max_crosses)


if __name__ == "__main__":
    part1()
    part2()
    part3()
