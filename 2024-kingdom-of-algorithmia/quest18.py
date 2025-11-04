"""
The Kingdom of Algorithmia [2024]
Quest 18: The Ring
https://everybody.codes/event/2024/quests/18
"""
from collections import deque
from math import inf
from pathlib import Path


def load_grid(filepath: str) -> list[str]:
    """
    Load the grid from a text file.

    Each line represents one row of the map.
    Characters:
        '.' = empty space
        '#' = obstacle
        'P' = palm
    """
    lines = Path(filepath).read_text().strip().splitlines()
    return [line.strip() for line in lines if line.strip()]


def find_start(grid: list[str]) -> tuple[int, int]:
    """
    Find the starting position: the first '.' in the leftmost column.
    """
    for r, row in enumerate(grid):
        if row[0] == '.':
            return r, 0
    raise ValueError("No valid starting position found on the left edge.")


def count_palms(grid: list[str]) -> int:
    """
    Count the total number of palm cells ('P') in the grid.
    """
    return sum(row.count('P') for row in grid)


def find_edge_starts(grid: list[str]) -> list[tuple[int, int]]:
    """
    Find all starting positions — cells marked '.' on the leftmost and rightmost edges.
    """
    R, C = len(grid), len(grid[0])
    starts = []
    for r in range(R):
        for c in [0, C - 1]:  # Only check left and right edges
            if grid[r][c] == '.':
                starts.append((r, c))
    return starts


def shortest_path_to_all_palms(grid: list[str]) -> int:
    """
    Perform a multi-source BFS starting from all '.' cells on the left/right edges,
    and return the minimum number of steps needed to reach all palms ('P').

    Returns:
        The number of steps required to reach all palms.
    """
    R, C = len(grid), len(grid[0])
    palms_remaining = count_palms(grid)

    # Initialize BFS queue with all edge start positions
    queue = deque([(0, r, c) for (r, c) in find_edge_starts(grid)])
    visited = set()

    # Directions for 4-way movement
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        dist, r, c = queue.popleft()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        # Found a palm — mark it as collected
        if grid[r][c] == 'P':
            palms_remaining -= 1
            if palms_remaining == 0:
                return dist

        # Explore neighboring cells
        for dr, dc in directions:
            rr, cc = r + dr, c + dc
            if (
                0 <= rr < R
                and 0 <= cc < C
                and grid[rr][cc] != '#'
            ):
                queue.append((dist + 1, rr, cc))

    raise RuntimeError("Unable to reach all palms.")


def bfs_distances(grid: list[str], start_r: int, start_c: int) -> dict[tuple[int, int], int]:
    """
    Perform BFS from a starting point (start_r, start_c) to compute
    the shortest distance to every '.' cell reachable in the grid.

    Returns:
        A dictionary mapping (r, c) positions of '.' cells to their distance.
    """
    R, C = len(grid), len(grid[0])
    distances = {}
    seen = set()
    queue = deque([(0, start_r, start_c)])

    while queue:
        dist, r, c = queue.popleft()
        if (r, c) in seen:
            continue
        seen.add((r, c))

        if grid[r][c] == '.':
            distances[(r, c)] = dist

        # Explore 4-directional neighbors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < R and 0 <= cc < C and grid[rr][cc] != '#':
                queue.append((dist + 1, rr, cc))

    return distances


def find_optimal_dot(grid: list[str]) -> int:
    """
    Find the '.' cell that minimizes the sum of distances
    from all palm ('P') positions.

    Returns:
        The minimal total distance (integer).
    """
    R, C = len(grid), len(grid[0])

    # Collect all '.' and 'P' positions
    open_cells = [(r, c) for r in range(R) for c in range(C) if grid[r][c] == '.']
    palms = [(r, c) for r in range(R) for c in range(C) if grid[r][c] == 'P']

    # Precompute distance maps from every palm to reachable '.' cells
    palm_distances = [bfs_distances(grid, r, c) for (r, c) in palms]

    best_total = inf
    for r, c in open_cells:
        total_distance = sum(dist_map.get((r, c), inf) for dist_map in palm_distances)
        best_total = min(best_total, total_distance)

    return best_total


def part1(filepath: str = "../input/everybody_codes_e2024_q18_p1.txt"):
    grid = load_grid(filepath)
    result = shortest_path_to_all_palms(grid)
    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2024_q18_p2.txt"):
    grid = load_grid(filepath)
    result = shortest_path_to_all_palms(grid)
    print("Part 2:", result)


def part3(filepath: str = "../input/everybody_codes_e2024_q18_p3.txt"):
    grid = load_grid(filepath)
    result = find_optimal_dot(grid)
    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
