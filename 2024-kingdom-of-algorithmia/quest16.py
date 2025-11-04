"""
The Kingdom of Algorithmia [2024]
Quest 16: Cat Grin of Fortune
https://everybody.codes/event/2024/quests/16
"""
from collections import Counter
from pathlib import Path
from typing import Callable


def load_input(filepath: str):
    """
    Load and parse the input file.

    The file has two parts separated by a blank line:
    - First line: comma-separated list of numbers (xs)
    - Second part: ASCII-art 'faces' laid out in rows
    """
    content = Path(filepath).read_text().strip()
    xs_section, faces_section = content.split("\n\n")
    xs = [int(x) for x in xs_section.split(',')]
    faces_lines = faces_section.splitlines()
    return xs, faces_lines


def parse_faces(faces_lines: list[str]) -> list[list[str]]:
    """
    Parse the ASCII-art faces layout into column lists.

    Each face is 3 characters wide with a 1-character gap between them.
    For example:
        ABC DEF GHI
    becomes columns:
        ['ABC'], ['DEF'], ['GHI']
    """
    num_cols = (len(faces_lines[0]) + 1) // 4  # each block is 3 chars + 1 space
    columns = [[] for _ in range(num_cols)]

    for line in faces_lines:
        for i in range(num_cols):
            face = line[i * 4 : i * 4 + 3]
            if face.strip():  # skip empty spaces
                columns[i].append(face)

    return columns


def select_faces(xs: list[int], columns: list[list[str]]) -> list[str]:
    """
    Select one face from each column based on xs[i].

    Each value in xs determines which face to pick by:
        (xs[i] * 100) % len(column)
    """
    selected = []

    for i, x in enumerate(xs):
        faces_in_column = columns[i]
        index = (x * 100) % len(faces_in_column)
        selected.append(faces_in_column[index])

    return selected


def part1(filepath: str = "../input/everybody_codes_e2024_q16_p1.txt") -> None:
    xs, faces_lines = load_input(filepath)
    columns = parse_faces(faces_lines)
    chosen = select_faces(xs, columns)
    print("Part 1:", " ".join(chosen))


def compute_score(columns: list[list[str]], state: list[int]) -> int:
    """
    Given the current state (which face index each column is showing),
    calculate the score based on letter repetition rules.
    """
    counts = Counter()

    # Count first and last characters of each face
    for col_idx, pos in enumerate(state):
        face = columns[col_idx][pos]
        counts[face[0]] += 1
        counts[face[2]] += 1

    # For each character, every occurrence beyond 2 adds 1 to the score
    return sum(max(0, v - 2) for v in counts.values())


def simulate(xs: list[int], columns: list[list[str]], total_steps: int = 202420242024) -> int:
    """
    Simulate the face rotation and scoring process for N steps.

    - Each column cycles through its faces according to xs[i].
    - Each step computes a score based on character repetition.
    - A cycle-detection dictionary (DP) is used to skip ahead efficiently
      once a repeated state is found.
    """
    num_cols = len(columns)
    state = [0] * num_cols  # initial indices for each column
    t = 0
    total_score = 0
    seen_states = {}  # maps state -> (time, score_at_that_time)

    while t < total_steps:
        t += 1

        # Update state (like a modular counter for each column)
        state = [(state[i] + xs[i]) % len(columns[i]) for i in range(num_cols)]
        key = tuple(state)

        # Check if this configuration has been seen before → detect loop
        if key in seen_states:
            prev_time, prev_score = seen_states[key]
            cycle_length = t - prev_time
            cycle_score = total_score - prev_score

            # Jump ahead as many full cycles as possible
            remaining = total_steps - t
            full_cycles = remaining // cycle_length

            if full_cycles > 0:
                t += full_cycles * cycle_length
                total_score += full_cycles * cycle_score

        else:
            seen_states[key] = (t, total_score)

        # Compute score for current state
        step_score = compute_score(columns, state)
        total_score += step_score

    return total_score


def part2(filepath: str = "../input/everybody_codes_e2024_q16_p2.txt") -> None:
    xs, face_lines = load_input(filepath)
    columns = parse_faces(face_lines)
    total = simulate(xs, columns)

    print("Part 2:", total)


def load_machine_input(filepath: str = "../input/everybody_codes_e2024_q16_p3.txt"):
    """
    Load and parse the lever machine input file.

    Format:
    - Line 1: comma-separated rotation values
    - Blank line
    - Multiple lines of 3-character-wide faces separated by spaces
    """
    content = Path(filepath).read_text().strip()
    lines = content.splitlines()
    rotations = [int(x) for x in lines[0].split(",")]

    # Parse the face grid (each face is 3 characters wide, separated by 1 space)
    faces_lines = lines[2:]
    cat_faces: list[list[str]] = []
    face_counts = []

    for line in faces_lines:
        faces = [line[i:i + 3] for i in range(0, len(line) - 2, 4)]
        for i, face in enumerate(faces):
            if len(cat_faces) <= i:
                cat_faces.append([])
                face_counts.append(0)
            if face.strip():
                cat_faces[i].append(face)
                face_counts[i] += 1

    return rotations, cat_faces, face_counts


def right_lever(indexes: list[int], rotations: list[int], max_values: list[int]) -> list[int]:
    """Advance each wheel by its rotation speed (the 'right lever')."""
    return [(indexes[i] + rotations[i]) % max_values[i] for i in range(len(indexes))]


def pull(indexes: list[int], max_values: list[int]) -> list[int]:
    """Increment each wheel by 1 (the 'pull lever')."""
    return [(indexes[i] + 1) % max_values[i] for i in range(len(indexes))]


def push(indexes: list[int], max_values: list[int]) -> list[int]:
    """Decrement each wheel by 1 (the 'push lever')."""
    return [(indexes[i] - 1) % max_values[i] for i in range(len(indexes))]


def get_cat_faces(cat_faces: list[list[str]], indexes: list[int]) -> list[str]:
    """Return the visible face from each column for the given indexes."""
    return [cat_faces[i][indexes[i]] for i in range(len(cat_faces))]


def get_coins(faces: list[str]) -> int:
    """
    Calculate coins from the current visible faces.
    Each face contributes its first and last character.
    If a character appears 3 or more times, you earn (count - 2) coins.
    """
    chars = "".join(face[0] + face[2] for face in faces)
    freq = {}
    for ch in chars:
        freq[ch] = freq.get(ch, 0) + 1
    return sum(max(0, count - 2) for count in freq.values())


def find_rotations(
    rotations: list[int],
    max_values: list[int],
    cat_faces: list[list[str]],
    steps: int,
    choose_fn: Callable[[int, int, int], int],
) -> int:
    """
    Dynamic programming over all possible lever actions for a fixed number of steps.

    States:
        (indexes, remaining_steps) -> best achievable score

    Transitions:
        - no action: just rotate via right lever
        - pull lever: increment all indexes by 1, then rotate
        - push lever: decrement all indexes by 1, then rotate

    The DP is implemented iteratively using a manual stack
    to avoid Python recursion limits.
    """
    dp = {}
    stack = [([0] * len(cat_faces), steps)]

    while stack:
        indexes, remaining = stack.pop()
        key = (tuple(indexes), remaining)

        if key in dp:
            continue
        if remaining == 0:
            dp[key] = 0
            continue

        # Compute possible next states
        no_action = right_lever(indexes, rotations, max_values)
        pull_action = right_lever(pull(indexes, max_values), rotations, max_values)
        push_action = right_lever(push(indexes, max_values), rotations, max_values)

        next_keys = [
            (tuple(no_action), remaining - 1),
            (tuple(pull_action), remaining - 1),
            (tuple(push_action), remaining - 1),
        ]

        # Ensure dependencies are processed before this one
        if any(k not in dp for k in next_keys):
            stack.append((indexes, remaining))
            for k in next_keys:
                if k not in dp:
                    stack.append(k)
            continue

        # Compute coin outcomes for each lever choice
        coins_no = get_coins(get_cat_faces(cat_faces, no_action))
        coins_pull = get_coins(get_cat_faces(cat_faces, pull_action))
        coins_push = get_coins(get_cat_faces(cat_faces, push_action))

        total_no = coins_no + dp[(tuple(no_action), remaining - 1)]
        total_pull = coins_pull + dp[(tuple(pull_action), remaining - 1)]
        total_push = coins_push + dp[(tuple(push_action), remaining - 1)]

        # Choose max or min depending on decider function
        dp[key] = choose_fn(total_no, total_pull, total_push)

    return dp[(tuple([0] * len(cat_faces)), steps)]


def part3(filepath: str = "../input/everybody_codes_e2024_q16_p3.txt") -> None:
    rotations, cat_faces, face_counts = load_machine_input(filepath)

    steps = 256

    max_score = find_rotations(rotations, face_counts, cat_faces, steps, max)
    min_score = find_rotations(rotations, face_counts, cat_faces, steps, min)

    print(f"Part 3: {max_score} {min_score}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
