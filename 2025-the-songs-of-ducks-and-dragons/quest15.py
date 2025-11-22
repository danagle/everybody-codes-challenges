"""
The Song of Ducks and Dragons [2025]
Quest 15: Definitely Not a Maze
https://everybody.codes/event/2025/quests/15
"""
from collections import deque
import heapq
import math
from pathlib import Path


def load_file(filepath):
    return [(s[0], int(s[1:])) 
        for s in Path(filepath).read_text().strip().split(',')]


def a_star(grid, cost_fn, start, goal, heuristic):
    """
    A* search on a compressed grid.

    grid: 2D list of bytes (optional: we mutate it only when finalizing a node)
    cost_fn: function ((x1,y1), (x2,y2)) -> movement cost
    start: (x, y)
    goal: (x, y)
    heuristic: function (x, y) -> estimated cost to goal (admissible)
    """
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    INF = math.inf

    g_score = {start: 0}
    open_heap = []
    heapq.heappush(open_heap, (heuristic(*start), start))

    closed = set()  # nodes whose shortest path is finalized

    while open_heap:
        f, current = heapq.heappop(open_heap)

        # skip entries that are stale (we may have pushed duplicates)
        if current in closed:
            continue

        # finalize current
        closed.add(current)
        cx, cy = current

        # optional: mark grid when node is finalized (not when discovered)
        # if you want to keep the side-effect behavior similar to your original
        if 0 <= cy < len(grid) and 0 <= cx < len(grid[0]):
            if grid[cy][cx] == ord(' '):
                grid[cy][cx] = ord('.')  # mark finalized

        if current == goal:
            return g_score[current]

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy

            if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
                continue
            if grid[ny][nx] != ord(' '):
                # treat non-space as non-walkable (walls, start, etc.)
                continue

            neighbor = (nx, ny)
            tentative_g = g_score[current] + cost_fn(current, neighbor)

            if tentative_g < g_score.get(neighbor, INF):
                g_score[neighbor] = tentative_g
                heapq.heappush(open_heap, (tentative_g + heuristic(nx, ny), neighbor))

    return -1


def bfs(grid, cost_fn, start, goal):
    """
    Breath-first search algorithm.
    
    grid: 2D list of bytes representing the map
    cost_fn: function ((x1,y1), (x2,y2)) -> movement cost
    start: tuple (x, y)
    goal: tuple (x, y)
    """
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque()
    queue.append((start, 0))
    
    while queue:
        (x, y), dist = queue.popleft()
        if (x, y) == goal:
            return dist
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] == ord(' '):
                grid[ny][nx] = ord('.')  # mark visited
                cost = cost_fn((x, y), (nx, ny))
                queue.append(((nx, ny), dist + cost))
    
    return -1


def dijkstra(grid, cost_fn, start, goal):
    """
    Dijkstra's algorithm using a min-heap.
    
    grid: 2D list of bytes
    cost_fn: function ((x1,y1), (x2,y2)) -> movement cost
    start: (x, y)
    goal: (x, y)
    """
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    INF = math.inf

    # distances from start
    dist = {start: 0}

    # priority queue of (distance, (x, y))
    heap = []
    heapq.heappush(heap, (0, start))

    # finalized nodes
    closed = set()

    while heap:
        current_dist, (x, y) = heapq.heappop(heap)

        if (x, y) in closed:
            continue
        closed.add((x, y))

        if (x, y) == goal:
            return current_dist

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check bounds and walkability
            if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
                continue
            if grid[ny][nx] != ord(' '):
                continue

            neighbor = (nx, ny)

            cost = cost_fn((x, y), neighbor)
            new_dist = current_dist + cost

            # Relaxation step
            if new_dist < dist.get(neighbor, INF):
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return -1  # unreachable


def find_path_with_compression(directions):
    """
    Simulates movement instructions on a 2D plane, compresses the coordinates
    to a smaller grid, marks walls along the path, and finds the shortest path
    from the start to the final destination using BFS with decompression for real distances.
    """
    # Initialize position, facing direction, and sequence of positions
    pos = [0, 0]        # starting at origin
    direction = [0, 1]  # facing north
    seq = [tuple(pos)]  # list of all positions visited

    # Track all positions along the path
    for turn, dist in directions:
        # Update facing direction based on turn
        if turn == 'L':
            direction = [-direction[1], direction[0]]  # rotate left
        elif turn == 'R':
            direction = [direction[1], -direction[0]]  # rotate right

        # Move in the current direction by 'dist' steps
        pos[0] += direction[0] * dist
        pos[1] += direction[1] * dist
        seq.append(tuple(pos))  # record new position

    # Collect all "interesting" coordinates for compression
    # Include neighbors (-1, 0, +1) to ensure movement between adjacent cells
    vx = set()
    vy = set()
    for x, y in seq:
        for d in (-1, 0, 1):
            vx.add(x + d)
            vy.add(y + d)

    # Create sorted lists for compressed coordinates
    xpos = sorted(vx)
    ypos = sorted(vy)

    # Maps from real coordinate -> compressed index
    xmap = {x: i for i, x in enumerate(xpos)}
    ymap = {y: i for i, y in enumerate(ypos)}

    # Initialize compressed grid
    grid = [[ord(' ')] * len(xpos) for _ in range(len(ypos))]

    # Trace walls on the compressed grid along the path
    pos_idx = [xmap[0], ymap[0]]  # starting position in compressed coordinates
    grid[pos_idx[1]][pos_idx[0]] = ord('S')  # mark start

    for target in seq[1:]:
        npos_idx = [xmap[target[0]], ymap[target[1]]]  # next position in compressed space

        # Determine step direction for each axis
        dx = (npos_idx[0] - pos_idx[0])
        dy = (npos_idx[1] - pos_idx[1])
        dx = 0 if dx == 0 else (dx // abs(dx))
        dy = 0 if dy == 0 else (dy // abs(dy))

        # Fill in all intermediate cells along the straight segment
        while pos_idx != npos_idx:
            pos_idx[0] += dx
            pos_idx[1] += dy
            grid[pos_idx[1]][pos_idx[0]] = ord('#')  # mark wall
        pos_idx = npos_idx  # move to next segment start

    # Clear the destination cell to ensure it is walkable
    grid[pos_idx[1]][pos_idx[0]] = ord(' ')

    # Use a cost function that converts compressed indices back to real distances
    dist = bfs(
        grid,
        lambda src_dst, next_dst: abs(xpos[next_dst[0]] - xpos[src_dst[0]]) +
                                  abs(ypos[next_dst[1]] - ypos[src_dst[1]]),
        (xmap[0], ymap[0]),       # start in compressed coordinates
        (pos_idx[0], pos_idx[1])  # goal in compressed coordinates
    )
    # Run Dijkstra's algorithm on compressed grid
    #dist = dijkstra(
    #    grid,
    #    lambda src_dst, next_dst: abs(xpos[next_dst[0]] - xpos[src_dst[0]]) +
    #                              abs(ypos[next_dst[1]] - ypos[src_dst[1]]),
    #    (xmap[0], ymap[0]),       # start in compressed coordinates
    #    (pos_idx[0], pos_idx[1])  # goal in compressed coordinates
    #)
    ## A*
    #goal_x, goal_y = pos_idx
    #heuristic = lambda x, y: abs(xpos[x] - xpos[goal_x]) + abs(ypos[y] - ypos[goal_y])
    #dist = a_star(
    #    grid,
    #    lambda src, dst: abs(xpos[dst[0]] - xpos[src[0]]) + abs(ypos[dst[1]] - ypos[src[1]]),
    #    (xmap[0], ymap[0]),        # start in compressed coordinates
    #    (pos_idx[0], pos_idx[1]),  # goal in compressed coordinates
    #    heuristic
    #)

    return dist


def part1(filepath="../input/everybody_codes_e2025_q15_p1.txt"):
    notes = load_file(filepath)
    result = find_path_with_compression(notes)
    print("Part 1:", result)


def part2(filepath="../input/everybody_codes_e2025_q15_p2.txt"):
    notes = load_file(filepath)
    result = find_path_with_compression(notes)
    print("Part 2:", result)


def part3(filepath="../input/everybody_codes_e2025_q15_p3.txt"):
    notes = load_file(filepath)
    result = find_path_with_compression(notes)
    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
 