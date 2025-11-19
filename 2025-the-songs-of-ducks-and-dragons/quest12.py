"""
The Song of Ducks and Dragons [2025]
Quest 12: One Spark to Burn Them All
https://everybody.codes/event/2025/quests/12
"""
from collections import defaultdict, deque
from pathlib import Path


class DSU:
    """Disjoint Set (Union-Find)"""
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size   = {x: 1 for x in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


def build_regions(grid):
    """Build DSU regions for equal-value connected components."""
    dsu = DSU(grid)

    for r, c in grid:
        for dr, dc in [(1,0), (0,1)]:         # right and down only
            nr, nc = r + dr, c + dc
            if (nr, nc) in grid:
                if grid[r, c] == grid[nr, nc]:
                    dsu.union((r, c), (nr, nc))

    # group cells by root
    regions = defaultdict(set)
    for cell in grid:
        regions[dsu.find(cell)].add(cell)

    return dsu, regions


def decending_path(grid, regions, dsu):
    """
    Compute descending-path reachability over regions.
    Returns:
       dp[root] = set of region-roots reachable from region 'root'
    """
    # process in increasing cell-value order
    region_order = sorted(regions, key=lambda root: grid[root])

    dp = {}

    for root in region_order:
        reachable = {root}

        for (r, c) in regions[root]:
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in grid and grid[nr, nc] < grid[r, c]:
                    reachable |= dp[dsu.find((nr, nc))]

        dp[root] = reachable

    return dp


def load_file(filepath: str):
    """Parse input file into a 2D-list representation of the grid."""
    return [
        [int(n) for n in line] 
        for line in Path(filepath).read_text().strip().splitlines() 
        if line.strip()
    ]


def load_grid(filepath: str):
    """Parse input file into a dict representation of the grid, {(r, c): barrel}."""
    lines = Path(filepath).read_text().strip().splitlines()
    h, w = len(lines), len(lines[0])
    grid = {(r, c): int(lines[r][c])
            for r in range(h)
            for c in range(w)}
    return grid


def flood_fill(grid, start, previous):
    """Return all cells reachable from start under:
       move only to neighbors with value <= current, excluding previous cells."""
    height, width = len(grid), len(grid[0])
    cardinal_directions = [(-1,0), (1,0), (0,-1), (0,1)]
    queue = deque([start])
    reached = set()
    
    append = queue.append

    while queue:
        row, col = queue.popleft()

        if (row, col) in previous or (row, col) in reached:
            continue

        reached.add((row, col))
        current_value = grid[row][col]

        for dr, dc in cardinal_directions:
            nr = row + dr
            nc = col + dc
            if 0 <= nr < height and 0 <= nc < width:
                if grid[nr][nc] <= current_value:
                    append((nr, nc))

    return reached


def part1(filepath="../input/everybody_codes_e2025_q12_p1.txt"):
    grid = load_file(filepath)
    visited = flood_fill(grid, (0, 0), set())
    print(f"Part 1: {len(visited)}")


def part2(filepath="../input/everybody_codes_e2025_q12_p2.txt"):
    grid = load_file(filepath)
    visit_one = flood_fill(grid, (0, 0), set())
    bottom_right = len(grid) - 1, len(grid[0]) - 1
    visit_two = flood_fill(grid, bottom_right, visit_one)
    print(f"Part 2: {len(visit_one) + len(visit_two)}")


def part3_bruteforce(filepath = "../input/everybody_codes_e2025_q12_p3.txt"):
    grid = load_file(filepath)
    rows = len(grid)
    cols = len(grid[0])
    seen = set()

    for _ in range(3):
        best_reach = None
        best_size = -1

        for r in range(rows):
            for c in range(cols):
                reach = flood_fill(grid, (r, c), seen)
                size = len(reach)
                if size > best_size:
                    best_size = size
                    best_reach = reach

        seen |= best_reach

    print(f"Part 3: {len(seen)}")


def part3(filepath = "../input/everybody_codes_e2025_q12_p3.txt"):
    grid = load_grid(filepath)
    total = 0

    for _ in range(3):
        dsu, regions = build_regions(grid)
        dp = decending_path(grid, regions, dsu)

        # compute score for each region
        scores = {}
        for root in dp:
            scores[root] = sum(dsu.size[r] for r in dp[root])

        # pick region with maximum reach
        best_root = max(scores, key=scores.get)
        removed_region_roots = dp[best_root]

        total += scores[best_root]

        # remove all cells belonging to those region-roots
        grid = {cell: val
                for cell, val in grid.items()
                if dsu.find(cell) not in removed_region_roots}

    print(f"Part 3: {total}")


if __name__ == "__main__":
    part1()
    part2()
    #part3_bruteforce()
    part3()
