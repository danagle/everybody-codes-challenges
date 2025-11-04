"""
The Entertainment Hub [ No. 2 ]
Quest 3: The Dice that Never Lie (Unless I Tell Them To)
https://everybody.codes/story/2/quests/3
"""
from collections import defaultdict
from itertools import count
from pathlib import Path
import re
from typing import Generator, List


def die(faces: List[int], seed: int) -> Generator[int, None, None]:
    """
    Deterministic pseudo-random die generator.

    Given a list of face values and a numeric seed,
    this yields an infinite sequence of die rolls based
    on a non-trivial but deterministic update rule.

    The sequence is governed by:
      - a 'pulse' value derived from the seed and roll number,
      - a cyclic index into the faces list.
    """

    pulse = seed          # initial state
    face_index = 0        # current face position
    n_faces = len(faces)

    for roll_number in count(1):
        # Each roll generates a 'spin' based on the current pulse and roll number
        spin = roll_number * pulse

        # Update the pulse using a modular recurrence
        pulse = (pulse + spin) % seed
        pulse += 1 + roll_number + seed

        # Advance the die face cyclically
        face_index = (face_index + spin) % n_faces

        # Yield the current face value
        yield faces[face_index]
        

def parse_dice(text: str) -> List[Generator[int, None, None]]:
    """
    Parse dice lines from `text` and return a list of die generators.

    Expected-ish line examples (flexible):
        "0: faces=[1, 2, 3,4,5,6] seed=1234"
        "12: faces=[1,2,3] seed=0"
    Blank lines are ignored.

    Raises ValueError for any non-blank line that cannot be parsed.
    """
    pattern = re.compile(r"faces=\[([^\]]+)\].*?seed=(\d+)")
    dice = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue  # allow blank lines

        m = pattern.search(line)
        if not m:
            fallback = re.search(r"faces=\[(.+?)\].*?seed=(\d+)", line)
            if fallback:
                faces_str, seed_str = fallback.groups()
            else:
                raise ValueError(f"Could not parse dice line: {line!r}")
        else:
            faces_str, seed_str = m.groups()

        # allow optional spaces after commas
        faces = [int(num.strip()) for num in faces_str.split(",") if num.strip()]
        seed = int(seed_str)
        dice.append(die(faces, seed))

    return dice


def part1(filepath: str = "../../input/everybody_codes_e2_q03_p1.txt"):
    text = Path(filepath).read_text().strip()
    
    dice = parse_dice(text)

    total = rolls = 0
    for group_roll in zip(*dice):
        total += sum(group_roll)
        rolls += 1
        if total >= 10_000:
            break

    print("Part 1:", rolls)


def part2(filepath: str = "../../input/everybody_codes_e2_q03_p2.txt"):
    # Read and parse input file
    text = Path(filepath).read_text().strip()
    dice_str, track_str = text.split("\n\n")

    track = [int(x) for x in track_str]
    dice = parse_dice(dice_str)

    # Track finish times
    finishes = []  # (finish_time, dice_index)
    for dice_index, die in enumerate(dice, start=1):
        finish_time = 0

        # Each track value must appear in sequence from the die
        for target_value in track:
            # Advance the die until it shows the required value
            while next(die) != target_value:
                finish_time += 1
            finish_time += 1  # count the successful roll

        finishes.append((finish_time, dice_index))

    # Sort dice by how quickly they finished
    finishes.sort(key=lambda x: x[0])

    # Build and print the finishing order
    finishing_order = ",".join(str(dice_index) for _, dice_index in finishes)

    print("Part 2:", finishing_order)


def part3(filepath: str = "../../input/everybody_codes_e2_q03_p3.txt"):
    """Simulate dice rolls across a grid, tracking all reachable cells."""

    # Load and parse input
    text = Path(filepath).read_text().strip()
    dice_str, grid_str = text.split("\n\n")

    # Convert grid into a 2D list of integers
    grid = [[int(num) for num in line] for line in grid_str.splitlines()]
    dice = parse_dice(dice_str)

    nrows, ncols = len(grid), len(grid[0])

    # Initialize starting positions
    # For each die, find all grid cells that match its first rolled value.
    active_positions = defaultdict(set)
    for i, die in enumerate(dice):
        first_value = next(die)
        for r in range(nrows):
            for c in range(ncols):
                if grid[r][c] == first_value:
                    active_positions[i].add((r, c))

    # Simulate rolling
    visited = set()  # all cells ever visited by any die
    while active_positions:
        new_positions = defaultdict(set)

        for i, positions in active_positions.items():
            next_value = next(dice[i])

            for r, c in positions:
                visited.add((r, c))

                # Check all 4 directions + stay put
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]:
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < nrows and 0 <= cc < ncols:
                        if grid[rr][cc] == next_value:
                            new_positions[i].add((rr, cc))

        active_positions = new_positions  # advance one round

    print("Part 3:", len(visited))


if __name__ == "__main__":
    part1()
    part2()
    part3()
    
