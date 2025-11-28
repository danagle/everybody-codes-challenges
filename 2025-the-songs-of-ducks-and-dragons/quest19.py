"""
The Song of Ducks and Dragons [2025]
Quest 19: Flappy Quack
https://everybody.codes/event/2025/quests/19
"""
from collections import defaultdict
from math import ceil, inf
from pathlib import Path
from typing import List, Tuple


def load_triplets(filepath: str) -> List[Tuple[int, int, int]]:
    """Reads a list of integer triplets from the input file."""
    return [
        tuple(map(int, line.split(',')))
        for line in Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    ]


def flappy_observation(triplets):
    """
    Computes the minimal flap cost using a geometric shortcut based on the
    movement constraints of the problem.

    Each time step increases x by 1 automatically (air current), while a flap
    changes y by +1 and not flapping changes y by -1. This means every path is
    composed of diagonal unit moves confined between two 45 degree lines (an
    isosceles right triangle constraint).

    For any point (x, y), the minimum number of flaps needed to reach it is the
    perpendicular distance from that point to the optimal 45 degree descent /
    ascent line. Algebraically, this distance is (x + y) / 2.

    The function tracks only the walls with strictly increasing x (the ones that
    actually constrain the optimal path) and returns the maximum of (x + y) / 2
    over those points, rounded up.
    
    This yields the exact minimum flap count for the problem.
    """
    max_xy = 0
    furthest_x = 0

    for triplet in triplets:
        x, y, _ = triplet
        if x > furthest_x:
            furthest_x = x
            max_xy = max(x+y, max_xy)

    return ceil(max_xy / 2)


def flap_through_walls(walls_list):
    """
    Computes the minimum number of flaps required to traverse all wall
    positions from left to right.

    The input list contains (x, y, _) triplets. All points with the same
    x-coordinate form a "wall group", and the solver must choose exactly one
    point from each group. For each step between walls, it calculates the
    flap cost needed to reach the next point.

    Returns the minimal total flap cost across all possible choices.
    """
    # Group wall points by their x-coordinate
    wall_map = defaultdict(list)
    for x, y, _ in walls_list:
        wall_map[x].append((x, y))

    # Sort groups by x, preserving the left to right order of walls
    walls = [group for _, group in sorted(wall_map.items())]

    cache = {}

    def compute_min_flaps(x, y, flaps, index):
        """
        Recursively computes the minimal flap cost from the current state.

        Parameters:
        x, y  : current position.
        flaps : total flaps spent so far.
        index : which wall group is being processed.

        For each candidate point (x1, y1) in the current wall group, it calculates
        the flap cost required to reach it, updates the resulting position, and
        recurses to the next wall group. Results are memoized to avoid recomputing
        identical states.

        Returns the minimum total flaps needed to finish all remaining wall groups
        from this state.
        """
        # Reached the end of all wall groups : return total flaps accumulated
        if index == len(walls):
            return flaps

        # Memoization key: current position + which wall group we're processing
        key = (x, y, index)
        if key in cache:
            return cache[key]

        best = inf  # Track the minimum flaps achievable from this state

        # Try hitting each (x1, y1) wall point in the current group
        for x1, y1 in walls[index]:
            dx = x1 - x  # horizontal distance to next wall
            dy = y1 - y  # vertical offset relative to current height

            # Compute flap cost needed to reach (x1, y1)
            if dy >= 0:
                # Need to rise dy, possibly more if horizontal travel exceeds that
                extra = dy + ceil(max(0, dx - dy) / 2)
            else:
                # Already above the wall; only horizontal shortfall matters
                extra = ceil(max(0, dx - (-dy)) / 2)

            new_flaps = flaps + extra
            new_y = y + 2 * extra - dx  # resulting height after moving/flapping
            new_x = x1

            # Recursively compute best path after this wall
            best = min(best, compute_min_flaps(new_x, new_y, new_flaps, index + 1))

        # Cache result for this state
        cache[key] = best

        return best

    # Start from (0,0) with zero flaps at wall group 0
    return compute_min_flaps(0, 0, 0, 0)


def part1(filepath: str= "../input/everybody_codes_e2025_q19_p1.txt"):
    """
    What is the minimum number of wing flaps required to reach the
    last passage at any height?
    """
    walls = load_triplets(filepath)
    result = flappy_observation(walls)

    print("Part 1:", result)


def part2(filepath: str= "../input/everybody_codes_e2025_q19_p2.txt") -> int:
    """
    What is the minimum number of wing flaps required to reach the
    last passage at any height?
    """
    walls = load_triplets(filepath)
    result = flappy_observation(walls)

    print("Part 2:", result)


def part3(filepath: str= "../input/everybody_codes_e2025_q19_p3.txt") -> int:
    """
    What is the minimum number of wing flaps required to reach the
    last passage at any height?
    """
    walls = load_triplets(filepath)
    result = flappy_observation(walls)

    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
