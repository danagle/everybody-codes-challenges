"""
The Song of Ducks and Dragons [2025]
Quest 17: Deadline-Driven Development
https://everybody.codes/event/2025/quests/17
"""
import heapq
from pathlib import Path

# 4-way movement
ORTHOGONAL = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def load_volcano(filepath: str):
    """Load grid and find volcano '@' and start 'S' positions."""
    volcano = start = None
    lines = Path(filepath).read_text().strip().splitlines()
    grid = [[int(c) if c.isdigit() else c for c in line.strip()] for line in lines]

    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == '@':
                volcano = (x, y)
            elif val == 'S':
                start = (x, y)
            if volcano and start:
                break
   
    # Replace volcano/start with numeric cost 0
    grid[volcano[1]][volcano[0]] = 0
    
    if start is not None:
        grid[start[1]][start[0]] = 0

    return volcano, grid, start


def part1(filepath="../input/everybody_codes_e2025_q17_p1.txt"):
    (vx, vy), grid, _ = load_volcano(filepath)

    height = len(grid)
    width = len(grid[0])

    # Precompute squared distances
    R = 10
    R2 = R * R
    dx2 = [(c - vx) * (c - vx) for c in range(width)]
    dy2 = [(r - vy) * (r - vy) for r in range(height)]

    total = 0
    for r in range(height):
        row = grid[r]
        dy = dy2[r]
        for c in range(width):
            v = row[c]
            if v > 0 and dx2[c] + dy <= R2:
                total += v

    print("Part 1:", total)


def part2(filepath="../input/everybody_codes_e2025_q17_p2.txt"):
    (vx, vy), grid, _ = load_volcano(filepath)

    height = len(grid)
    width = len(grid[0])

    # Precompute squared coordinate deltas
    dx2 = [(x - vx) * (x - vx) for x in range(width)]
    dy2 = [(y - vy) * (y - vy) for y in range(height)]

    cells = []
    append = cells.append  # local binding = faster

    for y in range(height):
        row = grid[y]
        dy = dy2[y]
        for x in range(width):
            if row[x] > 0:
                append((dx2[x] + dy, row[x]))

    # sort by r^2
    cells.sort(key=lambda t: t[0])

    # sweep outward
    previous = current = 0
    max_val = max_r = 0

    idx = 0
    n = len(cells)
    limit = max(height - vy, width - vx)

    for r in range(1, limit):
        r2 = r * r

        # accumulate all values entering radius r
        while idx < n and cells[idx][0] <= r2:
            current += cells[idx][1]
            idx += 1

        diff = current - previous
        if diff > max_val:
            max_val = diff
            max_r = r

        previous = current

    print("Part 2:", max_val * max_r)


def dijkstra(grid, start, end, passable, limit):
    """Optimized Dijkstra for variable-cost grid with pruning."""
    INF = float('inf')

    heap = [(0, start)]
    seen = {start: 0}
    height = len(grid)
    width = len(grid[0])

    while heap:
        cost, (x, y) = heapq.heappop(heap)

        if cost != seen[(x, y)]:
            continue

        if (x, y) == end:
            return cost

        if cost > limit:
            return INF  # early prune

        for dx, dy in ORTHOGONAL:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if not passable(ny, nx):
                continue

            next_cost = cost + grid[ny][nx]
            if next_cost < seen.get((nx, ny), INF):
                seen[(nx, ny)] = next_cost
                heapq.heappush(heap, (next_cost, (nx, ny)))

    return INF


def part3(filepath="../input/everybody_codes_e2025_q17_p3.txt"):
    INF = float('inf')
    # Offsets used for the start split (left/right of the volcano column)
    LEFT = ORTHOGONAL[-1]   # (-1, 0)
    RIGHT = ORTHOGONAL[-2]  # (1, 0)

    (vx, vy), grid, start = load_volcano(filepath)

    height, width = len(grid), len(grid[0])
    R = 0
    result = 0
    
    while True:
        R2 = R * R
        limit = 30 * (R + 1)

        # Start row is below the lava radius
        start_row = vy + (R + 1)
        if start_row >= height:
            break  # out of bounds

        # Center + left + right positions
        center = (vx, start_row)
        left = (vx + LEFT[0], start_row + LEFT[1])
        right = (vx + RIGHT[0], start_row + RIGHT[1])

        # Skip if neighbors are out of bounds
        if not (0 <= left[0] < width and 0 <= left[1] < height):
            R += 1
            continue
        if not (0 <= right[0] < width and 0 <= right[1] < height):
            R += 1
            continue

        # Precompute passable function for this radius
        def passable(y, x):
            # Blocked by lava
            if (x - vx)**2 + (y - vy)**2 <= R2:
                return False
            # Blocked by vertical line below volcano
            if x == vx and y >= vy:
                return False
            # Is non-negative
            return grid[y][x] >= 0

        # Dijkstra from left and right positions
        left_cost = dijkstra(grid, left, start, passable, limit)
        right_cost = dijkstra(grid, right, start, passable, limit)

        # Skip if either path is impossible
        if left_cost == INF or right_cost == INF:
            R += 1
            continue

        # Total cost = center + left + right + Dijkstra paths
        total = sum([grid[center[1]][center[0]], 
                     grid[left[1]][left[0]], 
                     grid[right[1]][right[0]], 
                     left_cost, 
                     right_cost]
                    )

        if total < limit:
            result = total * R
            break

        R += 1
    
    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
