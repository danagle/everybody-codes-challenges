"""
The Song of Ducks and Dragons [2025]
Quest 12: One Spark to Burn Them All
https://everybody.codes/event/2025/quests/12
"""
from collections import deque
from pathlib import Path


def load_file(filepath: str):
    return [
        [int(n) for n in line] 
        for line in Path(filepath).read_text().strip().splitlines() 
        if line.strip()
    ]


def flood_fill(grid, start, previous):
    """Return all cells reachable from start under:
       move only to neighbors with value <= current, excluding previous cells."""
    height, width = len(grid), len(grid[0])
    cardinal_directions = [(-1,0), (1,0), (0,-1), (0,1)]
    queue = deque([start])
    reached = set()
    
    append = queue.append

    while queue:
        row, col = queue.popleft()

        if (row, col) in previous or (row, col) in reached:
            continue

        reached.add((row, col))
        current_value = grid[row][col]

        for dr, dc in cardinal_directions:
            nr = row + dr
            nc = col + dc
            if 0 <= nr < height and 0 <= nc < width:
                if grid[nr][nc] <= current_value:
                    append((nr, nc))

    return reached


def part1(filepath="../input/everybody_codes_e2025_q12_p1.txt"):
    grid = load_file(filepath)
    visited = flood_fill(grid, (0,0), set())
    print("Part 1:", len(visited))


def part2(filepath="../input/everybody_codes_e2025_q12_p2.txt"):
    grid = load_file(filepath)
    visit_one = flood_fill(grid, (0, 0), set())
    bottom_right = len(grid) - 1, len(grid[0]) - 1
    visit_two = flood_fill(grid, bottom_right, visit_one)
    print("Part 2:", len(visit_one) + len(visit_two))


def part3(filepath = "../input/everybody_codes_e2025_q12_p3.txt"):
    grid = load_file(filepath)
    rows, cols = len(grid), len(grid[0])

    seen = set()

    for t in range(3):
        best_reach = None
        best_size = -1

        for r in range(rows):
            for c in range(cols):
                reach = flood_fill(grid, (r, c), seen)
                size = len(reach)
                if size > best_size:
                    best_size = size
                    best_reach = reach

        seen |= best_reach

    print("Part 3:", len(seen))


if __name__ == "__main__":
    part1()
    part2()
    part3()
