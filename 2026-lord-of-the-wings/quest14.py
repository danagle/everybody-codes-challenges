from collections import defaultdict
from itertools import combinations
from pathlib import Path


def read_notes(filepath: str) -> tuple[list[str], int, int]:
    grid = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    H, W = len(grid), len(grid[0])
    return grid, H, W


def bindings(grid: list[str], rows: int, cols: int) -> int:
    """Part 1: Count total boundary and internal edge mismatches."""
    total = 2 * (rows + cols)  # Outer boundary bindings
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols and grid[r][c] != grid[r][c + 1]:
                total += 1
            if r + 1 < rows and grid[r][c] != grid[r + 1][c]:
                total += 1
    return total


def build_graph(
    grid: list[str], rows: int, cols: int
) -> tuple[int, defaultdict[tuple[int, int], int]]:
    """Identifies connected pieces and computes seam costs."""
    piece = [[-1] * cols for _ in range(rows)]
    n = 0

    for r in range(rows):
        for c in range(cols):
            if piece[r][c] != -1:
                continue
            piece[r][c] = n
            stack = [(r, c)]
            while stack:
                y, x = stack.pop()
                for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                    if (
                        0 <= ny < rows
                        and 0 <= nx < cols
                        and piece[ny][nx] == -1
                        and grid[ny][nx] == grid[r][c]
                    ):
                        piece[ny][nx] = n
                        stack.append((ny, nx))
            n += 1

    cost = defaultdict(int)
    for r in range(rows):
        for c in range(cols):
            p = piece[r][c]
            if c + 1 < cols and piece[r][c + 1] != p:
                cost[tuple(sorted((p, piece[r][c + 1])))] += 1
            if r + 1 < rows and piece[r + 1][c] != p:
                cost[tuple(sorted((p, piece[r + 1][c])))] += 1
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                cost[(p, n)] += 1

    return n, cost


def union_find(par: list[int], x: int) -> int:
    """Union-Find with path compression."""
    while par[x] != x:
        par[x] = par[par[x]]
        x = par[x]
    return x


def min_bindings(grid: list[str], rows: int, cols: int) -> int:
    """Part 2: Minimum spanning tree cost of connecting all pieces."""
    n, cost = build_graph(grid, rows, cols)
    parent = list(range(n + 1))

    total = 0
    for (a, b), w in sorted(cost.items(), key=lambda kv: kv[1]):
        ra = union_find(parent, a)
        rb = union_find(parent, b)
        if ra != rb:
            parent[ra] = rb
            total += w
    return total


def min_bindings_with_charges(grid: list[str], rows: int, cols: int, charges: int = 2) -> int:
    """Part 3: MST with pre-merged charged components."""
    n, cost = build_graph(grid, rows, cols)
    nbrs = [[] for _ in range(n + 1)]
    for a, b in cost:
        nbrs[a].append(b)
        nbrs[b].append(a)

    parent = list(range(n + 1))
    tree = []
    for (a, b), w in sorted(cost.items(), key=lambda kv: kv[1]):
        ra = union_find(parent, a)
        rb = union_find(parent, b)
        if ra != rb:
            parent[ra] = rb
            tree.append((w, a, b))
    tree.sort()

    def extra_cost(chosen):
        par = list(range(n + 1))
        for p in chosen:
            for q in nbrs[p]:
                ra = union_find(par, p)
                rb = union_find(par, q)
                if ra != rb:
                    par[ra] = rb
        total = 0
        for w, a, b in tree:
            ra = union_find(par, a)
            rb = union_find(par, b)
            if ra != rb:
                par[ra] = rb
                total += w
        return total

    pieces = range(n)
    return min(extra_cost(c) for c in combinations(pieces, min(charges, n)))


def part1(filepath: str = "../input/everybody_codes_e2026_q14_p1.txt") -> None:
    print("Part 1:", bindings(*read_notes(filepath)))


def part2(filepath: str = "../input/everybody_codes_e2026_q14_p2.txt") -> None:
    print("Part 2:", min_bindings(*read_notes(filepath)))


def part3(filepath: str = "../input/everybody_codes_e2026_q14_p3.txt") -> None:
    print("Part 3:", min_bindings_with_charges(*read_notes(filepath)))


if __name__ == "__main__":
    part1()
    part2()
    part3()
