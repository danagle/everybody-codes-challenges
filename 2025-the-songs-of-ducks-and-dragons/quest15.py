"""
The Song of Ducks and Dragons [2025]
Quest 15: Definitely Not a Maze
https://everybody.codes/event/2025/quests/15
"""
from collections import deque
import heapq
from math import inf
from pathlib import Path


def load_file(filepath):
    """Reads list of steps from the input file."""
    return [(s[0], int(s[1:]))
            for s in Path(filepath).read_text(encoding="utf-8").strip().split(',')]


def a_star(grid, cost_fn, start, goal, heuristic):
    """ 
    A* search on a compressed grid.

    grid: 2D list of bytes
    cost_fn: function ((x1,y1), (x2,y2)) -> movement cost
    start: (x, y)
    goal: (x, y)
    heuristic: function (x, y) -> estimated cost to goal
    """
    directions = [(0,1), (1,0), (0,-1), (-1,0)]

    g_score = {start: 0}
    open_heap = []
    heapq.heappush(open_heap, (heuristic(*start), start))

    closed = set()  # nodes whose shortest path is finalized

    while open_heap:
        _, current = heapq.heappop(open_heap)

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

            if tentative_g < g_score.get(neighbor, inf):
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
            if new_dist < dist.get(neighbor, inf):
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return -1  # unreachable


def shortest_distance_with_compression(directions, algorithm="bfs"):
    """
    Simulates movement instructions on a 2D grid, compresses the coordinates
    to a smaller grid, marks walls along the path, and finds the shortest path
    using BFS / Dijkstra / A* on the compressed grid.
    """
    # Initialize position, facing direction, and sequence of positions
    pos = [0, 0]         # starting position
    direction = [0, 1]   # facing north
    seq = [tuple(pos)]   # visit list

    # Track all positions along the path
    for turn, dist in directions:
        # update facing direction
        if turn == 'L':
            direction = [-direction[1], direction[0]]
        else:  # 'R'
            direction = [direction[1], -direction[0]]

        # Move in the current direction by 'dist' steps
        pos[0] += direction[0] * dist
        pos[1] += direction[1] * dist
        seq.append(tuple(pos))

    # Collect compressed coordinate candidates
    # Only real endpoints + 2 inflation coords per turn
    vx = set()
    vy = set()

    for x, y in seq:
        vx.add(x)
        vy.add(y)

    # simulate again to detect turns
    pos = seq[0]
    direction = [0, 1]  # reset to north

    turn_right_pairs = {
        ((0, 1), (1, 0)),    # N -> E
        ((0, -1), (-1, 0)),  # S -> W
        ((-1, 0), (0, -1)),  # W -> S
        ((1, 0), (0, 1)),    # E -> N
    }

    for (turn, dist), next_pos in zip(directions, seq[1:]):
        x, y = pos
        old_dir = tuple(direction)

        # update direction to detect turn type
        if turn == 'L':
            direction = [-direction[1], direction[0]]
        else:
            direction = [direction[1], -direction[0]]

        new_dir = tuple(direction)

        if old_dir != new_dir:
            # RIGHT TURN corner inflation
            if (old_dir, new_dir) in turn_right_pairs:
                vx.update([x - 1, x + 1])
                vy.update([y - 1, y + 1])
            else:
                # LEFT TURN corner inflation
                vx.update([x + 1, x - 1])
                vy.update([y - 1, y + 1])

        pos = next_pos

    # sorted coordinate lists
    xpos = sorted(vx)
    ypos = sorted(vy)

    # maps from real coordinate to compressed index
    xmap = {x: i for i, x in enumerate(xpos)}
    ymap = {y: i for i, y in enumerate(ypos)}

    # Build compressed grid
    grid = [[ord(' ')] * len(xpos) for _ in range(len(ypos))]

    # Trace walls on the compressed grid along the path
    cx, cy = xmap[0], ymap[0]  # starting position in compressed coordinates
    grid[cy][cx] = ord('S')    # mark start

    for target in seq[1:]:
        # next position in compressed space
        nx, ny = xmap[target[0]], ymap[target[1]]

        # Determine step direction for each axis
        dx = nx - cx
        dy = ny - cy
        dx = 0 if dx == 0 else dx // abs(dx)
        dy = 0 if dy == 0 else dy // abs(dy)

        # Fill in all intermediate cells along the straight segment
        while (cx, cy) != (nx, ny):
            cx += dx
            cy += dy
            grid[cy][cx] = ord('#')

    # Clear the destination cell to ensure it is walkable
    grid[cy][cx] = ord(' ')

    # Search on compressed grid
    start = (xmap[0], ymap[0])
    goal = (cx, cy)

    # Use a cost function that converts compressed indices back to real distances
    # Cost function: distance in real coordinates
    cost_fn = lambda src, dst: (
        abs(xpos[dst[0]] - xpos[src[0]]) +
        abs(ypos[dst[1]] - ypos[src[1]])
    )

    # Heuristic for A* (Manhattan in real coordinates)
    heuristic = lambda x, y: (
        abs(xpos[x] - xpos[goal[0]]) +
        abs(ypos[y] - ypos[goal[1]])
    )

    # Map algorithm names to functions
    algorithms = {
        "bfs": bfs,
        "dijkstra": dijkstra,
        "astar": lambda grid, cost, start, goal:
            a_star(grid, cost, start, goal, heuristic)
    }

    if algorithm not in algorithms:
        raise ValueError(f"Unknown algorithm '{algorithm}'.")

    return algorithms[algorithm](grid, cost_fn, start, goal)


def part1(filepath="../input/everybody_codes_e2025_q15_p1.txt"):
    """What is the length of the shortest path to the exit point?"""
    notes = load_file(filepath)
    result = shortest_distance_with_compression(notes)
    print("Part 1:", result)


def part2(filepath="../input/everybody_codes_e2025_q15_p2.txt"):
    """What is the length of the shortest path to the exit point?"""
    notes = load_file(filepath)
    result = shortest_distance_with_compression(notes)
    print("Part 2:", result)


def part3(filepath="../input/everybody_codes_e2025_q15_p3.txt"):
    """What is the length of the shortest path to the exit point?"""
    notes = load_file(filepath)
    result = shortest_distance_with_compression(notes)
    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
