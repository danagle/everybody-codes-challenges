from pathlib import Path

# State Constants
WATER = 0
POTENTIAL = 1
LAND = 2
SAND = 3
TREE = 4


def read_notes(filepath: str):
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    grid = [[POTENTIAL if char == "1" else WATER for char in line] for line in lines]

    rows, cols = len(grid), len(grid[0])
    if rows > 0 and cols > 0:
        grid[rows // 2][cols // 2] = LAND

    return grid


def land_expansion(grid):
    rows = len(grid)
    cols = len(grid[0])

    changed = True
    while changed:
        changed = False
        for r in range(rows):
            row_r = grid[r]
            for c in range(cols):
                if row_r[c] == LAND:
                    continue

                good = 0
                land = 0
                for dr in (-1, 0, 1):
                    nr = r + dr
                    if 0 <= nr < rows:
                        row_nr = grid[nr]
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            nc = c + dc
                            if 0 <= nc < cols:
                                val = row_nr[nc]
                                if val == LAND:
                                    land += 1
                                    good += 1
                                elif val == POTENTIAL:
                                    good += 1

                if land >= 1 and good >= 5:
                    row_r[c] = LAND
                    changed = True

    return grid


def part1(filepath: str = "../input/everybody_codes_e2026_q05_p1.txt"):
    grid = read_notes(filepath)
    grid = land_expansion(grid)
    result = sum(row.count(LAND) for row in grid)
    print("Part 1:", result)


def place_sand(grid):
    """Coast marking and sand expansion."""
    rows = len(grid)
    cols = len(grid[0])

    # Mark water-touching land as coast (SAND)
    for r in range(rows):
        row_r = grid[r]
        for c in range(cols):
            if row_r[c] != LAND:
                continue

            touches_water = False
            for dr in (-1, 0, 1):
                nr = r + dr
                if not (0 <= nr < rows):
                    touches_water = True
                    break
                row_nr = grid[nr]
                for dc in (-1, 0, 1):
                    nc = c + dc
                    if not (0 <= nc < cols):
                        touches_water = True
                        break
                    if row_nr[nc] <= POTENTIAL:
                        touches_water = True
                        break
                if touches_water:
                    break

            if touches_water:
                row_r[c] = SAND

    # Sand expansion
    changed = True
    while changed:
        changed = False
        for r in range(rows):
            row_r = grid[r]
            for c in range(cols):
                if row_r[c] != LAND:
                    continue

                sand_count = 0
                for dr in (-1, 0, 1):
                    nr = r + dr
                    if 0 <= nr < rows:
                        row_nr = grid[nr]
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            nc = c + dc
                            if 0 <= nc < cols and row_nr[nc] == SAND:
                                sand_count += 1

                if sand_count >= 5:
                    row_r[c] = SAND
                    changed = True

    return grid


def part2(filepath: str = "../input/everybody_codes_e2026_q05_p2.txt"):
    grid = read_notes(filepath)
    grid = land_expansion(grid)
    grid = place_sand(grid)
    result = sum(row.count(SAND) for row in grid)
    print("Part 2:", result)


def tree_placement(grid):
    """Initial tree placement and dual growth iterations."""
    rows = len(grid)
    cols = len(grid[0])

    # Initial tree placement
    for r in range(rows):
        row_r = grid[r]
        for c in range(cols):
            if row_r[c] != LAND:
                continue

            tree = 0
            for dr in range(-2, 3):
                nr = r + dr
                if nr < 0 or nr >= rows:
                    continue
                row_nr = grid[nr]
                for dc in range(-2, 3):
                    nc = c + dc
                    if nc < 0 or nc >= cols or (dr == 0 and dc == 0):
                        continue
                    if (dr in (-2, 2)) and (dc in (-2, 2)):
                        continue
                    val = row_nr[nc]
                    if val == LAND or val == TREE:
                        tree += 1

            if tree == 20:
                row_r[c] = TREE

    # Tree growth iterations (twice)
    for _ in range(2):
        positions = []
        for r in range(rows):
            row_r = grid[r]
            for c in range(cols):
                if row_r[c] != LAND:
                    continue

                tree_count = 0
                blocked = False
                for dr in (-1, 0, 1):
                    nr = r + dr
                    if nr < 0 or nr >= rows:
                        continue
                    row_nr = grid[nr]
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nc = c + dc
                        if 0 <= nc < cols:
                            val = row_nr[nc]
                            if val == SAND:
                                blocked = True
                                break
                            if val == TREE:
                                tree_count += 1
                    if blocked:
                        break

                if not blocked and tree_count >= 4:
                    positions.append((r, c))

        for r, c in positions:
            grid[r][c] = TREE

    return sum(row.count(TREE) for row in grid)


def part3(filepath: str = "../input/everybody_codes_e2026_q05_p3.txt"):
    grid = read_notes(filepath)
    grid = land_expansion(grid)
    grid = place_sand(grid)
    result = tree_placement(grid)
    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
