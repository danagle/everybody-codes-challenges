"""
The Song of Ducks and Dragons [2025]
Quest 11: The Scout Duck Protocol
https://everybody.codes/event/2025/quests/11
"""
from math import ceil
from pathlib import Path


def load_file(filepath: str):
    """Read list of numbers from input text file."""
    return [
        int(line)
        for line in Path(filepath).read_text(encoding="utf-8").strip().splitlines()
        if line.strip()
    ]


def phase_one(columns, max_rounds=10):
    """Simulates Phase 1: left to right flood of surplus ducks."""
    completed = 0
    moved = True
    while moved:
        if completed == max_rounds:
            break
        moved = False
        for i in range(len(columns) - 1):
            if columns[i] > columns[i + 1]:
                columns[i] -= 1
                columns[i + 1] += 1
                moved = True
        if moved:
            completed += 1
    return completed, columns


def phase_two(rounds_completed, columns, max_rounds=-1):
    """Simulates Phase 2: left to right flood of deficits."""
    moved = True
    while moved:
        if rounds_completed == max_rounds:
            break
        moved = False
        for i in range(len(columns) - 1):
            if columns[i] < columns[i + 1]:
                columns[i] += 1
                columns[i + 1] -= 1
                moved = True
        if moved:
            rounds_completed += 1
    return rounds_completed, columns


def part1(filepath="../input/everybody_codes_e2025_q11_p1.txt"):
    """Calculate flock checksum after 10 rounds."""
    columns = load_file(filepath)
    rounds_completed, columns = phase_one(columns)
    _, final_columns = phase_two(rounds_completed, columns, max_rounds=10)

    result = sum(i * n for i, n in enumerate(final_columns, 1))

    print("Part 1:", result)


def part2_bruteforce(filepath="../input/everybody_codes_e2025_q11_p2.txt"):
    """Compute how many rounds needed to balance the flock across all columns."""
    columns = load_file(filepath)
    max_rounds = -1
    rounds_completed, columns = phase_one(columns, max_rounds)
    total_rounds, _ = phase_two(rounds_completed, columns, max_rounds)

    print("Part 2:", total_rounds)


def part2(filepath="../input/everybody_codes_e2025_q11_p2.txt"):
    """
    Compute how many rounds needed to balance the flock across all columns.
    
    Phase 1: Propagate excess from left to right until the distribution is monotonic.
    Phase 2: Raise everything to the final uniform level.
    """
    columns = load_file(filepath)
    # Create a working copy
    ascending = columns.copy()

    # Iteratively smooth until non-decreasing
    def has_drop(xs):
        """Checks for decreasing sequence."""
        return any(xs[i] > xs[i+1] for i in range(len(xs) - 1))

    while has_drop(ascending):
        for i in range(len(ascending) - 1):
            if ascending[i] > ascending[i + 1]:
                # Shift half of the difference (rounded up) from the left to the right.
                delta = ceil((ascending[i] - ascending[i + 1]) / 2)
                ascending[i] -= delta
                ascending[i + 1] += delta

    sum1 = 0    # Cumulative sum of original list
    sum2 = 0    # Cumulative sum of smoothed list
    phase1 = 0  # Maximum prefix surplus

    # Calculate how much 'lead' the original list has over the smoothed one.
    for first, second in zip(columns, ascending):
        sum1 += first
        sum2 += second
        phase1 = max(phase1, sum1 - sum2)

    # Compute the average value of the smoothed list
    average = sum(ascending) // len(ascending)

    # Compute how much the smoothed list needs to rise to reach the average.
    phase2 = sum(max(0, average - column) for column in ascending)

    total_rounds = phase1 + phase2

    print("Part 2:", total_rounds)


def part3(filepath="../input/everybody_codes_e2025_q11_p3.txt"):
    """
    Computes how many ducks must be added to all below-mean columns to bring
    them up to the mean.
    """
    columns = load_file(filepath)
    mean = sum(columns) // len(columns)

    total = sum(mean - ducks for ducks in columns if ducks < mean)

    print("Part 3:", total)


if __name__ == "__main__":
    part1()
    part2_bruteforce()
    #part2()
    part3()
