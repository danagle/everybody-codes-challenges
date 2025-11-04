"""
The Kingdom of Algorithmia [2024]
Quest 17: Galactic Geometry
https://everybody.codes/event/2024/quests/17
"""
import heapq
from collections import defaultdict
from itertools import combinations
from pathlib import Path


def load_star_map(filepath: str) -> list[tuple[int, int]]:
    """
    Parse the input grid into a list of (y, x) coordinates for stars (*).
    """
    stars = []
    for y, line in enumerate(Path(filepath).read_text().strip().splitlines()):
        for x, char in enumerate(line):
            if char == '*':
                stars.append((y, x))
    return stars


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    """
    Compute the Manhattan distance between two points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def minimum_spanning_tree(stars: list[tuple[int, int]]) -> int:
    """
    Compute the total weight of a Minimum Spanning Tree (MST)
    connecting all stars using Manhattan distance as edge weights.
    
    Returns:
        The total MST length plus the number of connected nodes.
    """
    if not stars:
        return 0

    total_length = 0
    visited = set()
    pq = [(0, stars[0])]  # (distance, star)

    while pq:
        dist, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        total_length += dist

        # Add neighbors (all remaining stars)
        for neighbor in stars:
            if neighbor not in visited:
                heapq.heappush(pq, (manhattan(current, neighbor), neighbor))

    # Add len(visited) for the "node contribution" defined by the problem
    return total_length + len(visited)


def brilliant_constellations(stars: list[tuple[int, int]]) -> int:
    """
    Group stars into 'brilliant constellations' where any two stars
    within Manhattan distance < 6 belong to the same constellation.
    
    For each cluster, compute a local MST (via Prim’s algorithm)
    and record its size (MST total distance + number of nodes).

    Returns:
        The product of the sizes of the 3 largest constellations.
    """
    if not stars:
        return 0

    # Build adjacency list for stars within distance < 6
    adjacency = defaultdict(list)
    for s1, s2 in combinations(stars, 2):
        d = manhattan(s1, s2)
        if d < 6:
            adjacency[s1].append((d, s2))
            adjacency[s2].append((d, s1))

    remaining = set(stars)
    cluster_sizes = []

    # Explore connected components using Prim’s algorithm
    while remaining:
        start = remaining.pop()
        pq = [(0, start)]
        seen = set()
        total_distance = 0

        while pq:
            dist, node = heapq.heappop(pq)
            if node in seen:
                continue
            seen.add(node)
            total_distance += dist

            for ndist, neighbor in adjacency[node]:
                if neighbor not in seen:
                    heapq.heappush(pq, (ndist, neighbor))

        # Store cluster size
        cluster_sizes.append(total_distance + len(seen))

        # Remove visited nodes from remaining
        remaining -= seen

    # Compute the product of the three largest clusters
    cluster_sizes.sort()
    if len(cluster_sizes) < 3:
        return 0  # not enough constellations to multiply

    return cluster_sizes[-1] * cluster_sizes[-2] * cluster_sizes[-3]


def part1(filepath: str = "../input/everybody_codes_e2024_q17_p1.txt") -> None:
    stars = load_star_map(filepath)
    result = minimum_spanning_tree(stars)
    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2024_q17_p2.txt") -> None:
    stars = load_star_map(filepath)
    result = minimum_spanning_tree(stars)
    print("Part 2:", result)


def part3(filepath: str = "../input/everybody_codes_e2024_q17_p3.txt") -> None:
    stars = load_star_map(filepath)
    result = brilliant_constellations(stars)
    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
