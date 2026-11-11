from collections import deque
from pathlib import Path


def read_notes(filepath: str) -> tuple[list[str], int, int]:
    grid = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    H, W = len(grid), len(grid[0])
    return grid, H, W


def part1_original(filepath: str = "../input/everybody_codes_e2026_q12_p1.txt") -> None:
    grid, rows, cols = read_notes(filepath)

    seen = [[False] * cols for _ in range(rows)]
    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '#' or seen[r][c]:
                continue
            # Flood fill one stack and take its bounding box
            stack = [(r, c)]
            seen[r][c] = True
            r0 = r1 = r
            c0 = c1 = c
            while stack:
                y, x = stack.pop()
                r0, r1, c0, c1 = min(r0, y), max(r1, y), min(c0, x), max(c1, x)
                for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                    if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == '#' and not seen[ny][nx]:
                        seen[ny][nx] = True
                        stack.append((ny, nx))
            total += min(r1 - r0 + 1, c1 - c0 + 1)  # Full rectangle: one spell per row or per column

    print("Part 1:", total)


def maximum_matching_konig(filepath: str) -> int:
    grid, rows, cols = read_notes(filepath)

    # Label each maximal horizontal run and maximal vertical run of '#'
    hid = [[-1] * cols for _ in range(rows)]
    vid = [[-1] * cols for _ in range(rows)]
    nh = nv = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '#':
                if c > 0 and grid[r][c - 1] == '#':
                    hid[r][c] = hid[r][c - 1]
                else:
                    hid[r][c] = nh
                    nh += 1
                if r > 0 and grid[r - 1][c] == '#':
                    vid[r][c] = vid[r - 1][c]
                else:
                    vid[r][c] = nv
                    nv += 1

    # Bipartite graph where each block joins its horizontal and vertical run
    adj = [[] for _ in range(nh)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '#':
                adj[hid[r][c]].append(vid[r][c])

    # Minimum number of runs touching every block
    # Minimum vertex cover = Maximum matching (Konig)
    return hopcroft_karp(adj, nh, nv)


def hopcroft_karp(adj: list[list[int]], n_left: int, n_right: int) -> int:
    """Hopcroft-Karp algorithm"""
    INF = float('inf')
    match_l = [-1] * n_left
    match_r = [-1] * n_right
    size = 0
    while True:
        dist = [INF] * n_left
        dq = deque()
        for u in range(n_left):
            if match_l[u] == -1:
                dist[u] = 0
                dq.append(u)
        found = False
        while dq:
            u = dq.popleft()
            for v in adj[u]:
                w = match_r[v]
                if w == -1:
                    found = True
                elif dist[w] == INF:
                    dist[w] = dist[u] + 1
                    dq.append(w)
        if not found:
            return size
        it = [0] * n_left
        for root in range(n_left):
            if match_l[root] != -1:
                continue
            path = [root]
            while path:
                u = path[-1]
                if it[u] < len(adj[u]):
                    v = adj[u][it[u]]
                    it[u] += 1
                    w = match_r[v]
                    if w == -1:
                        for k in range(len(path) - 1, -1, -1):
                            uu = path[k]
                            vv = adj[uu][it[uu] - 1]
                            match_l[uu], match_r[vv] = vv, uu
                        size += 1
                        break
                    if dist[w] == dist[u] + 1:
                        path.append(w)
                else:
                    dist[u] = INF
                    path.pop()


def part1(filepath: str = "../input/everybody_codes_e2026_q12_p1.txt") -> None:
    print("Part 1:", maximum_matching_konig(filepath))


def part2(filepath: str = "../input/everybody_codes_e2026_q12_p2.txt") -> None:
    print("Part 2:", maximum_matching_konig(filepath))


def part3(filepath: str = "../input/everybody_codes_e2026_q12_p3.txt") -> None:
    print("Part 3:", maximum_matching_konig(filepath))


if __name__ == "__main__":
    part1()
    part2()
    part3()