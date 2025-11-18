"""
The Song of Ducks and Dragons [2025]
Quest 11: The Scout Duck Protocol
https://everybody.codes/event/2025/quests/11
"""
from pathlib import Path

def load_file(filepath: str):
    return [
        int(line) 
        for line in Path(filepath).read_text().strip().splitlines() 
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


def phase_two(rounds_completed, columns, max_rounds=10):
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
    _, final_columns = phase_two(rounds_completed, columns)
    
    result = sum(i * n for i, n in enumerate(final_columns, 1))

    print("Part 1:", result)


def part2(filepath="../input/everybody_codes_e2025_q11_p2.txt"):
    """Compute how many rounds needed to balance the flock across all columns."""
    columns = load_file(filepath)
    max_rounds = -1
    rounds_completed, columns = phase_one(columns, max_rounds)
    total_rounds, _ = phase_two(rounds_completed, columns, max_rounds)

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
    part2()
    part3()
