"""
The Kingdom of Algorithmia [2024]
Quest 5: Pseudo-Random Clap Dance
https://everybody.codes/event/2024/quests/5
"""
from collections import Counter
from pathlib import Path


def load_columns(filepath: str) -> list[list[int]]:
    """
    Load the puzzle input file for a given part and return the columns as lists of integers.
    """
    rows = [list(map(int, line.split())) for line in Path(filepath).read_text().splitlines()]
    # Transpose rows into columns
    return [list(col) for col in zip(*rows)]


def step(round_num: int, cols: list[list[int]]) -> None:
    """
    Perform one step of the clapper simulation.
    - Selects the current column based on round number.
    - Removes the top number (the "clapper").
    - Calculates its new position in the next column and inserts it there.
    """
    clapper_col_index = round_num % len(cols)
    clapper = cols[clapper_col_index].pop(0)
    target_col = cols[(clapper_col_index + 1) % len(cols)]

    # Compute the new position in a mirrored circular manner
    pos = (clapper - 1) % (2 * len(target_col))
    if pos >= len(target_col):
        pos = 2 * len(target_col) - pos

    target_col.insert(pos, clapper)


def part1(filepath: str = "../input/everybody_codes_e2024_q05_p1.txt") -> None:
    """
    Simulate 10 steps and print the top element of each column concatenated together.
    """
    cols = load_columns(filepath)
    for r in range(10):
        step(r, cols)
    print("".join(str(col[0]) for col in cols))


def part2(filepath: str = "../input/everybody_codes_e2024_q05_p2.txt") -> None:
    """
    Continue stepping until a number has been seen 2024 times.
    Print the final result multiplied by the number of rounds executed.
    """
    cols = load_columns(filepath)
    seen = Counter()
    result = None
    round_num = 0

    while seen[result] < 2024:
        step(round_num, cols)
        result = int("".join(str(col[0]) for col in cols))
        seen[result] += 1
        round_num += 1

    print(result * round_num)


def get_state(round_num: int, cols: list[list[int]]) -> tuple[int, tuple[tuple[int, ...], ...]]:
    """
    Represent the current state uniquely as (current_column_index, columns_as_tuples).
    Used to detect repeating patterns.
    """
    current_col = round_num % len(cols)
    return (current_col, tuple(tuple(col) for col in cols))


def part3(filepath: str = "../input/everybody_codes_e2024_q05_p3.txt") -> None:
    """
    Run steps until the state repeats.
    """
    cols = load_columns(filepath)
    seen_states = set()
    round_num = 0
    max_result = 0

    while (state := get_state(round_num, cols)) not in seen_states:
        seen_states.add(state)
        step(round_num, cols)
        result = int("".join(str(col[0]) for col in cols))
        max_result = max(max_result, result)
        round_num += 1

    print(max_result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
