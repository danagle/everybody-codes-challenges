"""
The Kingdom of Algorithmia [2024]
Quest 3: Mining Maestro
https://everybody.codes/event/2024/quests/3
"""
from pathlib import Path

def new_depth(i: int, j: int, depths: list[list[float]], directions: list[tuple[int, int]]) -> float:
    """Calculate the next depth value for cell (i, j) based on its neighbors."""
    min_neighbor_depth = float("inf")

    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < len(depths) and 0 <= nj < len(depths[0]):
            min_neighbor_depth = min(min_neighbor_depth, depths[ni][nj])
        else:
            min_neighbor_depth = 0  # Edge of grid counts as depth 0

    return min_neighbor_depth + 1


def mine_expansion(filepath: str, include_diagonals: bool = False) -> int:
    """
    Simulate the mine digging process for a map file.

    Parameters:
        filepath: Path to input file.
        include_diagonals: If True, diagonal directions are also considered.

    Returns:
        The total sum of all depth values once stable.
    """
    # Direction vectors
    ORTHOGONAL_DIRS = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    DIAGONAL_DIRS = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

    directions = ORTHOGONAL_DIRS + (DIAGONAL_DIRS if include_diagonals else [])

    lines = Path(filepath).read_text().strip().splitlines()

    # Initialize grid and depth map
    depths = [[0] * len(line) for line in lines]
    active_cells = [(i, j) for i, line in enumerate(lines) for j, c in enumerate(line) if c == "#"]

    total_depth, previous_total = 0, -1

    # Continue updating until total depth stabilizes
    while total_depth != previous_total:
        for i, j in active_cells:
            depths[i][j] = new_depth(i, j, depths, directions)

        previous_total, total_depth = total_depth, sum(map(sum, depths))

    return int(total_depth)


if __name__ == "__main__":
    for part_num in range(1, 4):
        filepath = f"../input/everybody_codes_e2024_q03_p{part_num}.txt"
        include_diagonals = (part_num == 3)
        result = mine_expansion(filepath, include_diagonals)
        print(f"Part {part_num}: {result}")
