"""
The Kingdom of Algorithmia [2024]
Quest 14: The House of Palms
https://everybody.codes/event/2024/quests/14
"""
from collections import deque
from math import inf
from pathlib import Path

# Directions in 3D space
MOVES = {
    'B': (0, 0, -1),
    'D': (0, -1, 0),
    'F': (0, 0, 1),
    'L': (-1, 0, 0),
    'R': (1, 0, 0),
    'U': (0, 1, 0),
}


def parse_branches(filepath: str) -> list[list[tuple[str, int]]]:
    """
    Parse input file into a list of branch definitions.
    Each branch is a list of (direction, distance) tuples.
    """
    lines = Path(filepath).read_text().strip().splitlines()
    return [[(segment[0], int(segment[1:])) for segment in line.split(',')]
            for line in lines]


def part1(filepath: str = "../input/everybody_codes_e2024_q14_p1.txt") -> None:
    steps = parse_branches(filepath)
    total = 0
    max_height = 0
    for step in steps[0]:
        if step[0] == 'U':
            total += step[1]
        elif step[0] == 'D':
            total -= step[1]
        max_height = max(max_height, total)

    print("Part 1:", max_height)


def build_tree(branches: list[list[tuple[str, int]]]) -> set[tuple[int, int, int]]:
    """
    Expand all branch paths into a set of occupied 3D coordinates (segments).
    """
    segments = set()

    for branch in branches:
        x = y = z = 0
        segments.add((x, y, z))  # root included
        for direction, distance in branch:
            dx, dy, dz = MOVES[direction]
            for _ in range(distance):
                x += dx
                y += dy
                z += dz
                segments.add((x, y, z))

    return segments


def part2(filepath: str = "../input/everybody_codes_e2024_q14_p2.txt") -> None:
    branches = parse_branches(filepath)
    tree_with_root = build_tree(branches)
    # Exclude root from total number of segments
    print("Part 2:", len(tree_with_root) - 1)
    

def find_leaves(branches: list[list[tuple[str, int]]]) -> set[tuple[int, int, int]]:
    """
    Determine the 3D coordinates of all leaf endpoints (end of each branch).
    """
    leaves = set()
    for branch in branches:
        x = y = z = 0
        for direction, distance in branch:
            dx, dy, dz = MOVES[direction]
            x += dx * distance
            y += dy * distance
            z += dz * distance
        leaves.add((x, y, z))
    return leaves


def find_trunk(segments: set[tuple[int, int, int]]) -> set[tuple[int, int, int]]:
    """
    Identify all main trunk segments (all positions directly above root).
    """
    return {(x, y, z) for (x, y, z) in segments if x == 0 and z == 0 and y >= 0}


def bfs_distance_sum(start: tuple[int, int, int],
                     leaves: set[tuple[int, int, int]],
                     segments: set[tuple[int, int, int]]) -> int:
    """
    Compute total distance from a trunk segment to all leaves via BFS.
    Stop early if all leaves have been reached.
    """
    queue = deque([(start, 0)])
    visited = {start}
    total = 0
    reached = 0

    while queue and reached < len(leaves):
        (x, y, z), dist = queue.popleft()
        if (x, y, z) in leaves:
            total += dist
            reached += 1

        for dx, dy, dz in MOVES.values():
            nxt = (x + dx, y + dy, z + dz)
            if nxt in segments and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, dist + 1))

    return total if reached == len(leaves) else inf


def part3(filepath: str = "../input/everybody_codes_e2024_q14_p3.txt") -> None:
    branches = parse_branches(filepath)
    segments = build_tree(branches)
    leaves = find_leaves(branches)
    trunk = find_trunk(segments)

    print(f"Segments: {len(segments)}, Leaves: {len(leaves)}, Trunk segments: {len(trunk)}")
    murkiness = min(bfs_distance_sum(tap, leaves, segments) for tap in trunk)

    print("Part 3:", murkiness)


if __name__ == "__main__":
    part1()
    part2()
    part3()
