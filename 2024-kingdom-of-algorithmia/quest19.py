"""
The Kingdom of Algorithmia [2024]
Quest 19: Encrypted Duck
https://everybody.codes/event/2024/quests/19
"""
from itertools import cycle
from pathlib import Path


def load_input(part_num: int) -> tuple[str, list[str]]:
    """
    Load input for a given part number.
    Returns:
        (pattern, grid_lines)
    """
    filename = f"../input/everybody_codes_e2024_q19_p{part_num}.txt"
    pattern, _, *lines = Path(filename).read_text().strip().splitlines()

    return pattern, lines


def flatten(grid: list[list[str]]) -> str:
    """Convert a 2D character grid into a single newline-joined string."""
    return "\n".join("".join(row) for row in grid)


def adjacent_cells(i: int, j: int) -> list[tuple[int, int]]:
    """Return the 8 coordinates surrounding (i, j) in clockwise order."""
    return [
        (i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1),
        (i + 1, j + 1), (i + 1, j), (i + 1, j - 1), (i, j - 1),
    ]


def rotate(grid: list[list], position: tuple[int, int], direction: str) -> None:
    """
    Rotate the 8 surrounding cells of a given position.
      - direction = 'L' for counterclockwise (left)
      - direction = 'R' for clockwise (right)
    """
    adj = adjacent_cells(*position)
    values = [grid[i][j] for (i, j) in adj]

    if direction == "L":  # rotate left
        adj = adj[-1:] + adj[:-1]
    elif direction == "R":  # rotate right
        adj = adj[1:] + adj[:1]
    else:
        raise ValueError(f"Invalid rotation direction: {direction}")

    for (i, j), val in zip(adj, values):
        grid[i][j] = val


def build_position_mapping(pattern: str, grid_size: tuple[int, int]) -> dict[tuple[int, int], tuple[int, int]]:
    """
    Apply the full rotation pattern to construct a mapping of positions after one full pattern cycle.
    Returns:
        A dict mapping each cell (i, j) → its destination (oi, oj).
    """
    rows, cols = grid_size

    # Prepare a coordinate grid tracking where each cell "moves"
    loc_grid = [[(i, j) for j in range(cols)] for i in range(rows)]
    rotation_points = [(i, j) for i in range(1, rows - 1) for j in range(1, cols - 1)]

    # Apply the pattern cyclically across all rotation points
    for direction, point in zip(cycle(pattern), rotation_points):
        rotate(loc_grid, point, direction)

    # Construct mapping after one complete application
    return {(i, j): loc_grid[i][j] for i in range(rows) for j in range(cols)}


def build_exponent_mappings(base_mapping: dict, target: int) -> list[int]:
    """
    Precompute repeated mappings using exponentiation by squaring.
    Returns:
        A list of mapping sizes needed to reach the target.
    """
    mappings = {1: base_mapping}
    mapping_size = 1

    while mapping_size < target:
        prev = mappings[mapping_size]
        mapping_size *= 2
        # Compose mapping with itself
        mappings[mapping_size] = {k: prev[v] for k, v in prev.items()}

    # Determine which precomputed powers are needed for target
    required = [k for k in mappings if k & target]
    return required, mappings


def solve_part(part: int, target: int) -> str:
    """Compute the solution for a given part."""
    pattern, lines = load_input(part)
    grid = [list(line) for line in lines]

    # Build mapping after one full pattern rotation
    base_mapping = build_position_mapping(pattern, (len(grid), len(grid[0])))

    # Precompute mapping powers and required exponents
    required_sizes, all_mappings = build_exponent_mappings(base_mapping, target)

    # Apply composed mapping to produce the final grid
    new_grid = [row.copy() for row in grid]
    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            oi, oj = i, j
            for size in required_sizes:
                oi, oj = all_mappings[size][(oi, oj)]
            new_grid[i][j] = grid[oi][oj]

    # Format solution output
    result = flatten(new_grid)
    # Trim to the section between '>' and '<' (for compact answer display)
    return result[result.index(">") + 1 : result.index("<")]


if __name__ == "__main__":
    part_rounds = {1: 1, 2: 100, 3: 1_048_576_000}
    for part_num in part_rounds:
        result = solve_part(part_num, part_rounds[part_num])
        print(f"Part {part_num}:", result)
