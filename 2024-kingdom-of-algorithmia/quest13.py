"""
The Kingdom of Algorithmia [2024]
Quest 13: Never Gonna Let You Down
https://everybody.codes/event/2024/quests/13
"""
from math import inf
from pathlib import Path


def load_notes(filepath: str) -> dict[tuple[int, int], str]:
    """
    Load the maze grid from a file.

    Each non-wall character (not '#' or ' ') becomes an entry in the grid,
    mapped from its (row, column) coordinates to its character.
    """
    lines = Path(filepath).read_text().strip().splitlines()
    grid = {}

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char not in "# ":
                grid[(i, j)] = char

    return grid


def adjacent_squares(position: tuple[int, int]) -> list[tuple[int, int]]:
    """Return the 4 orthogonal neighboring squares (up, left, right, down)."""
    i, j = position
    return [(i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j)]


def valid_adjacent_squares(position: tuple[int, int], maze: dict) -> list[tuple[int, int]]:
    """Return neighbors that actually exist in the maze."""
    return [p for p in adjacent_squares(position) if p in maze]


def min_transition(a: int, b: int) -> int:
    """
    Compute the smallest 'rotation' difference between digits a and b,
    considering wrap-around at 10 (like a circular dial 0-9).
    """
    return min(abs(a - b), abs(10 - a + b), abs(10 - b + a))


def complete_maze(filepath: str) -> int:
    """
    Calculate the minimum number of seconds needed to complete the maze.

    The maze consists of numeric tiles (0-9) and start ('S') / end ('E') points.
    Moving between adjacent spaces takes:
        1 + min_transition(current_value, neighbor_value) seconds.
    """
    maze = load_notes(filepath)

    # Identify start and end points
    starts = [pos for pos, char in maze.items() if char == 'S']
    end, = (pos for pos, char in maze.items() if char == 'E')

    # Convert characters to numeric values (non-numeric = 0)
    maze = {pos: int(char) if char.isnumeric() else 0 for pos, char in maze.items()}

    # Initialize cost table
    costs = {pos: inf for pos in maze}
    costs[end] = 0

    # Start propagation from the end point backward
    to_visit = set(valid_adjacent_squares(end, maze))

    while to_visit:
        next_visit = set()

        for position in to_visit:
            neighbors = valid_adjacent_squares(position, maze)
            possible_costs = [
                costs[nbr] + min_transition(maze[position], maze[nbr]) + 1
                for nbr in neighbors
            ]

            if not possible_costs:
                continue

            new_cost = min(possible_costs)
            if new_cost < costs[position]:
                costs[position] = new_cost
                next_visit.update(neighbors)

        to_visit = next_visit

    # Return the best (minimum) cost among all start points
    return min(costs[start] for start in starts)


if __name__ == "__main__":
    for part_num in range(1, 4):
        filepath = f"../input/everybody_codes_e2024_q13_p{part_num}.txt"
        best_cost = complete_maze(filepath)
        print(f"Part {part_num}:", best_cost)
