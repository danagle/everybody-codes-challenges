"""
The Song of Ducks and Dragons [2025]
Quest 8: The Art of Connection
https://everybody.codes/event/2025/quests/8
"""
from collections import defaultdict
from itertools import combinations, pairwise
from pathlib import Path


def load_data(filepath: str) -> complex:
    return [int(s) for s in Path(filepath).read_text().strip().split(",")]


def part1(filepath: str = "../input/everybody_codes_e2025_q08_p1.txt") -> None:
    sequence = load_data(filepath)
    half = max(sequence) // 2
    total = sum(((a - b) % half == 0) for a, b in pairwise(sequence))

    print(f"Part 1: {total}")


def intersects(chord1, chord2):
    """Return True if chords intersect inside the circle."""
    if (chord1[0] in chord2) or (chord1[1] in chord2):
        return False
    # XOR: True if exactly one endpoint of chord2 lies strictly between chord1 endpoints
    return (chord1[0] < chord2[0] < chord1[1]) ^ (chord1[0] < chord2[1] < chord1[1])


def part2(filepath: str = "../input/everybody_codes_e2025_q08_p2.txt"):
    sequence = load_data(filepath)
    # Normalize chord endpoints so (a,b) == (b,a))
    chords = [sorted(pair) for pair in pairwise(sequence)]

    total = sum(
        intersects(chords[i], chords[j])
        for i in range(len(chords))
        for j in range(i + 1, len(chords))
    )

    print("Part 2:", total)


def _part3(filepath = "../input/everybody_codes_e2025_q08_p3.txt"):
    sequence = load_data(filepath)
    chords = [sorted(pair) for pair in pairwise(sequence)]
    num_points = 256
    max_crosses = 0
    
    for a, b in combinations(range(1, num_points + 1), 2):
        count = sum(intersects((a, b), chord) for chord in chords)
        max_crosses = max(max_crosses, count)

    print("Part 3:", max_crosses)


def part3(filepath = "../input/everybody_codes_e2025_q08_p3.txt"):
    sequence = load_data(filepath)
    num_points = 256
    max_crosses = 0

    # Build adjacency list of chords in sequence
    chords = defaultdict(list)
    for a, b in pairwise(sequence):
        chords[a].append(b)
        chords[b].append(a)

    # Iterate over all possible starting points of a chord
    for chord_start in range(1, num_points + 1):
        current = 0

        # Slide the end of the chord forward around the circle
        for chord_end in range(chord_start + 2, num_points + 1):
            # Add new intersections that have entered the window
            current += sum(1 for point in chords[chord_end - 1] 
                           if not chord_start <= point < chord_end + 1)
            # Remove intersections that are no longer inside the window
            current -= sum(1 for point in chords[chord_end] 
                           if chord_start < point < chord_end - 1)

            max_crosses = max(max_crosses, current)

    print("Part 3:", max_crosses)


if __name__ == "__main__":
    part1()
    part2()
    part3()
