"""
The Song of Ducks and Dragons [2025]
Quest 20: Dream in Triangles
https://everybody.codes/event/2025/quests/20
"""
from collections import defaultdict, deque
from itertools import zip_longest
from math import inf
from pathlib import Path


def load_triangular_grid(filepath: str):
    """Read the 2-D triangular grid from the input text file."""
    grid_dict = {}
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()

    for r, row in enumerate(lines):
        for c, cell in enumerate(row.strip('.')):
            grid_dict[r, c] = cell

    return grid_dict


def neighbours(position, include_self=False):
    """Returns the neighbours for a triangular shaped cell (row, col)."""
    if include_self:
        yield position
    row, col = position
    yield row, col - 1  # left
    yield row, col + 1  # right
    if col % 2:
        yield row + 1, col - 1  # diagonal below left
    else:
        yield row - 1, col + 1  # diagonal above right


def map_rotation(dict_grid):
    """Performs transformation pipeline on the grid to create rotation map."""
    # Group coordinates by row (r)
    rows = defaultdict(list)
    for r, c in dict_grid:
        rows[r].append((r, c))
    grid = list(rows.values())

    # Split each row into even and odd slices
    grid = [row[e::2] for row in grid for e in (0, 1)]

    # Reverse vertically
    grid.reverse()

    # Transpose and drop padding
    grid = [list(filter(None, col)) for col in zip_longest(*grid)]

    # Build mapping from new (r, c) to old coordinate
    return {(r, c): coord for r, row in enumerate(grid) for c, coord in enumerate(row)}


def bfs(grid, with_rotation=False):
    """BFS to find distance to 'end' tile using trampoline mechanics."""
    # Locate start and end
    start = next(p for p, v in grid.items() if v == 'S')
    end   = next(p for p, v in grid.items() if v == 'E')

    # Mark both as traversable
    grid[start] = grid[end] = 'T'

    # Rotation map used for part 3
    mapping = map_rotation(grid)

    def mapped_neighbors(pos):
        """Yields neighbours mapped under rotation."""
        for n in neighbours(pos, True):
            m = mapping.get(n)
            if m is not None:
                yield m

    def local_neighbors(pos):
        """Yields immediate neighbours."""
        for n in neighbours(pos):
            if grid.get(n) == 'T':
                yield n

    if with_rotation:
        neighbors_fn = mapped_neighbors
    else:
        neighbors_fn = local_neighbors

    # Initialize distances for all 'T' cells
    distance = {p: inf for p, v in grid.items() if v == 'T'}
    distance[start] = 0

    queue = deque([start])
    in_queue = set(queue)

    while queue:
        pos = queue.popleft()
        in_queue.remove(pos)
        dist = distance[pos] + 1

        for next_pos in neighbors_fn(pos):
            if next_pos in distance and dist < distance[next_pos]:
                distance[next_pos] = dist
                if next_pos not in in_queue:
                    queue.append(next_pos)
                    in_queue.add(next_pos)

    return distance[end]


def part1(filepath: str = "../input/everybody_codes_e2025_q20_p1.txt") -> None:
    """
    Count pairs of 'T' that share an edge when each cell is an equilateral triangle
    arranged in a checkerboard of up/down orientations.
    """
    grid = load_triangular_grid(filepath)

    count = 0
    for pos, cell in grid.items():
        if cell == 'T':
            for neighbour in neighbours(pos):
                count += grid.get(neighbour) == 'T'

    print("Part 1:", count // 2)


def part2(filepath: str = "../input/everybody_codes_e2025_q20_p2.txt") -> None:
    """Minimum number of jumps to reach the golden trampoline using BFS."""
    grid = load_triangular_grid(filepath)

    print("Part 2:", bfs(grid, with_rotation=False))


def part3(filepath: str = "../input/everybody_codes_e2025_q20_p3.txt") -> None:
    """What is the minimum number of jumps required to reach the sphere of mysterious energy?"""
    grid = load_triangular_grid(filepath)

    # Use rotating map
    print("Part 3:", bfs(grid, with_rotation=True))


if __name__ == "__main__":
    part1()
    part2()
    part3()
