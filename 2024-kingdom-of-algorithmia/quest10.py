"""
The Kingdom of Algorithmia [2024]
Quest 10: Shrine Needs to Shine
https://everybody.codes/event/2024/quests/10
"""
from collections import Counter
from pathlib import Path

        
def part1(filepath: str = "../input/everybody_codes_e2024_q10_p1.txt") -> None:
    lines = Path(filepath).read_text().strip().splitlines()

    rows = [set(line)-{"."} for line in lines[2:6]]
    cols = [set(line)-{"."} for line in list(zip(*lines))[2:6]]

    runic_word = "".join(str(x) for row in rows for col in cols for x in row & col)

    print("Part 1:", runic_word)


def part2(filepath: str = "../input/everybody_codes_e2024_q10_p2.txt") -> None:
    lines = Path(filepath).read_text().strip().splitlines()

    big_rows = [lines[i:i+8] for i in range(0, len(lines), 9)]
    big_row = list(map(" ".join, zip(*big_rows)))
    big_row = [l.split() for l in big_row]

    grids = list(zip(*big_row))
    words = []

    for grid in grids:
        rows = [set(line)-{"."} for line in grid[2:6]]
        cols = [set(line)-{"."} for line in list(zip(*grid))[2:6]]
        word = ""
        for row in rows:
            for col in cols:
                word += (row&col).pop()
        words.append(word)

    def score(word):
        if "." in word:
            return 0
        return sum(i*(ord(c)-64) for i,c in enumerate(word,1))

    print("Part 2:", sum(map(score, words)))


def process_block(grid: list[list[str]], start_row: int, start_col: int, R=8, C=8) -> bool:
    """
    Process a single 8x8 block in the grid.
    Returns True if any changes were made.
    """
    changed = False
    block = [[grid[start_row + r][start_col + c] for c in range(C)] for r in range(R)]

    # Pass 1: Fill cells that can be deduced directly
    for r in range(R):
        for c in range(C):
            if block[r][c] == '.':
                row_vals = {block[r][cc] for cc in range(C)}
                col_vals = {block[rr][c] for rr in range(R)}
                candidates = (row_vals & col_vals) - {'.', '?'}

                if len(candidates) == 1:
                    grid[start_row + r][start_col + c] = candidates.pop()
                    changed = True

    # Pass 2: Handle '?' with deduction rules
    for r in range(R):
        for c in range(C):
            if block[r][c] != '?':
                continue

            row_vals = {block[r][cc] for cc in range(C)}
            col_vals = {block[rr][c] for rr in range(R)}

            # Check missing single '.' in row
            if '*' not in row_vals:
                empty_cols = [cc for cc in range(C) if block[r][cc] == '.']
                if len(empty_cols) == 1:
                    col_freq = Counter(block[rr][empty_cols[0]] for rr in range(R))
                    options = [k for k, v in col_freq.items() if v == 1 and k != '.']
                    if len(options) == 1:
                        grid[start_row + r][start_col + c] = options[0]
                        changed = True

            # Check missing single '.' in column
            if '*' not in col_vals:
                empty_rows = [rr for rr in range(R) if block[rr][c] == '.']
                if len(empty_rows) == 1:
                    row_freq = Counter(block[empty_rows[0]][cc] for cc in range(C))
                    options = [k for k, v in row_freq.items() if v == 1 and k != '.']
                    if len(options) == 1:
                        grid[start_row + r][start_col + c] = options[0]
                        changed = True

    return changed


def solve_grid(grid: list[list[str]], block_height=8, block_width=8) -> list[list[str]]:
    """Iteratively solve all 8x8 blocks in the grid until no changes occur."""
    while True:
        changed = False
        for br in range(0, len(grid), 6):
            if br + block_height - 1 >= len(grid):
                continue
            for bc in range(0, len(grid[br]), 6):
                if bc + block_width - 1 >= len(grid[br]):
                    continue
                if process_block(grid, br, bc, block_height, block_width):
                    changed = True
        if not changed:
            break

    return grid


def compute_score(grid: list[list[str]], R=8, C=8) -> int:
    """Compute the final score after solving the grid."""
    total_score = 0
    for br in range(0, len(grid), 6):
        if br + R - 1 >= len(grid):
            continue
        for bc in range(0, len(grid[br]), 6):
            if bc + C - 1 >= len(grid[br]):
                continue

            block = [[grid[br + r][bc + c] for c in range(C)] for r in range(R)]
            block_score = 0
            ok = True
            i = 0
            for r in range(2, 6):
                for c in range(2, 6):
                    ch = block[r][c]
                    if ch in {'.', '?'}:
                        ok = False
                        continue
                    ch_val = ord(ch) - ord('A') + 1
                    assert 1 <= ch_val <= 26
                    i += 1
                    block_score += i * ch_val
            if ok:
                total_score += block_score
    return total_score


def part3(filepath: str = "../input/everybody_codes_e2024_q10_p3.txt") -> None:
    grid = [list(line) 
            for line in Path(filepath).read_text().strip().splitlines()
            if line.strip()]

    solved = solve_grid(grid)
    total_score = compute_score(solved)

    print("Part 3:", total_score)


if __name__ == "__main__":
    part1()
    part2()
    part3()
