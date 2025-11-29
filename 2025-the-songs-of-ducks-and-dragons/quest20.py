"""
The Song of Ducks and Dragons [2025]
Quest 20: Dream in Triangles
https://everybody.codes/event/2025/quests/20
"""
from pathlib import Path


def read_lines(filepath):
    """Read lines of text from input file."""
    return Path(filepath).read_text(encoding="utf-8").strip().splitlines()


def within(x, y, grid):
    """Check (x,y) is within the grid boundary."""
    return 0 <= x < len(grid) and 0 <= y < len(grid[x])


def at(x, y, grid):
    """Get value at (x,y) on grid."""
    return grid[x][y]


def locate_tile_on_grid(grid, tile):
    """Find the first instance of tile on the grid."""
    return next((r, row.index(tile)) for r, row in enumerate(grid) if tile in row)


def part1(filepath: str = "../input/everybody_codes_e2025_q20_p1.txt") -> None:
    """
    Count pairs of 'T' that share an edge when each cell is an equilateral triangle
    arranged in a checkerboard of up/down orientations.
    """
    lines = read_lines(filepath)
    count = 0

    # horizontal pairs
    for row in lines:
        count += sum(row[i] == row[i-1] == 'T' for i in range(1, len(row)))

    # staggered vertical-ish pairs
    for r in range(1, len(lines) - 1, 2):
        for c, ch in enumerate(lines[r]):
            if ch == 'T':
                dr = 1 if (r + c) % 2 else -1
                if lines[r + dr][c] == 'T':
                    count += 1

    print("Part 1:", count)


def part2(filepath: str = "../input/everybody_codes_e2025_q20_p2.txt") -> None:
    """
    Minimum number of jumps to reach the golden trampoline.
    BFS shortest path on a static map.
    """
    grid = read_lines(filepath)

    start = locate_tile_on_grid(grid, 'S')
    end =  locate_tile_on_grid(grid, 'E')

    current_positions = {start}
    visited = {start}
    jumps = 0

    while True:
        jumps += 1
        next_positions = set()

        for x, y in current_positions:
            for dx, dy in ((0, -1), (0, 1), ((-1 if (x + y) % 2 == 0 else 1), 0)):
                nx, ny = x + dx, y + dy

                if (nx, ny) == end:
                    print("Part 2:", jumps)
                    return

                if within(nx, ny, grid) and at(nx, ny, grid) == 'T' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    next_positions.add((nx, ny))

        current_positions = next_positions


def rotate(grid, start):
    """Rotate the triangle."""
    height = len(grid)
    width = len(grid[0])
    new_grid = [list(row) for row in grid]

    sx, sy = start

    for r in range(height):
        x = sx - r
        y = sy + r
        up = True

        for c in range(width):
            if new_grid[r][c] != '.':
                new_grid[r][c] = at(x, y, grid)
                if up:
                    x -= 1
                else:
                    y -= 1
                up = not up

    return ["".join(row) for row in new_grid]


def part3(filepath: str = "../input/everybody_codes_e2025_q20_p3.txt") -> None:
    """What is the minimum number of jumps required to reach the sphere of mysterious energy?"""
    base_grid = read_lines(filepath)

    start = locate_tile_on_grid(base_grid, 'S')

    # Precompute the three possible triangle layouts
    grids = [base_grid]
    grids.append(rotate(grids[-1], start))
    grids.append(rotate(grids[-1], start))

    current_positions = {start}
    visited = [set([start]), set(), set()]
    jumps = 0

    while True:
        jumps += 1
        idx = jumps % 3
        current_grid = grids[idx]
        next_positions = set()

        for (x, y) in current_positions:
            for dx, dy in ((0, 0), (0, -1), (0, 1), (-1 if (x + y) % 2 == 0 else 1, 0)):
                nx, ny = x + dx, y + dy

                if not within(nx, ny, base_grid):
                    continue

                cell = at(nx, ny, current_grid)

                if cell == 'E':
                    print("Part 3:", jumps)
                    return

                if cell in 'TS' and (nx, ny) not in visited[idx]:
                    visited[idx].add((nx, ny))
                    next_positions.add((nx, ny))

        current_positions = next_positions


if __name__ == "__main__":
    part1()
    part2()
    part3()
