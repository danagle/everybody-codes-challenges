"""
The Song of Ducks and Dragons [2025]
Quest 14: The Game of Light
https://everybody.codes/event/2025/quests/14
"""
from itertools import product
from pathlib import Path

DIAGONALS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def load_grid(filepath: str):
    """Read the 2-D grid from the input text file."""
    text =  Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    return [[c == "#" for c in line] for line in text]


def count_active(grid):
    """Count the active cells in the grid/"""
    return sum(cell for row in grid for cell in row)


def life_round(grid):
    """Simulate a round of the game of light."""
    rows, cols = len(grid), len(grid[0])
    new_grid = [[False] * cols for _ in range(rows)]

    for r, c in product(range(rows), range(cols)):
        live_neighbors = sum(
            grid[nr][nc]
            for dr, dc in DIAGONALS
            if 0 <= (nr := r + dr) < rows and 0 <= (nc := c + dc) < cols
        )

        if grid[r][c]:
            new_grid[r][c] = live_neighbors % 2 == 1
        else:
            new_grid[r][c] = live_neighbors % 2 == 0

    return new_grid


def part1(filepath="../input/everybody_codes_e2025_q14_p1.txt"):
    """What is the total number of active tiles across all 10 rounds?"""
    grid = load_grid(filepath)
    total = 0

    for _ in range(10):
        grid = life_round(grid)
        total += count_active(grid)

    print("Part 1:", total)


def part2(filepath="../input/everybody_codes_e2025_q14_p2.txt"):
    """What is the total number of active tiles across all 2025 rounds?"""
    grid = load_grid(filepath)
    total = 0

    for _ in range(2025):
        grid = life_round(grid)
        total += count_active(grid)

    print("Part 2:", total)


def center_matches(grid, small_grid, top=13, left=13):
    """Check if an 8x8 block matches `small_grid`."""
    return all(
        grid[top + r][left + c] == small_grid[r][c]
        for r in range(8)
        for c in range(8)
    )


def part3(filepath="../input/everybody_codes_e2025_q14_p3.txt"):
    """What is the total number of active tiles across all 1,000,000,000 rounds?"""
    small = load_grid(filepath)
    grid = [[False] * 34 for _ in range(34)]

    total_matched = 0
    last_match = 0
    matches = []

    target_rounds = 1_000_000_000
    cycle_extra_sum = 0

    for round_ in range(target_rounds):
        # 1. Run a life step
        grid = life_round(grid)
        live_count = count_active(grid)

        # 2. Check for center 8×8 match
        if center_matches(grid, small):
            total_matched += live_count

            delta = round_ - last_match
            matches.append((delta, live_count))
            last_match = round_

            # 3. Check if this match closes a cycle
            prev_matches = matches[:-1]
            last = matches[-1]

            if last in prev_matches:
                i = prev_matches.index(last)

                # 4. Identify the cycle section
                cycle = matches[i + 1:]
                cycle_len = sum(d for d, _ in cycle)
                cycle_sum = sum(v for _, v in cycle)

                # 5. Determine how many full cycles remain
                remaining_rounds = target_rounds - round_ - 1
                full_cycles = remaining_rounds // cycle_len
                cycle_extra_sum += full_cycles * cycle_sum

                # 6. Handle leftover rounds
                leftover = remaining_rounds % cycle_len
                for d, val in cycle:
                    if leftover < d:
                        break
                    cycle_extra_sum += val
                    leftover -= d

                break

    print("Part 3:", (total_matched + cycle_extra_sum))


if __name__ == "__main__":
    part1()
    part2()
    part3()
