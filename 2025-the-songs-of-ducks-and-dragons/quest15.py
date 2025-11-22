"""
The Song of Ducks and Dragons [2025]
Quest 15: Definitely Not a Maze
https://everybody.codes/event/2025/quests/15
"""
import heapq
from pathlib import Path


def load_file(filepath):
    return Path(filepath).read_text().strip().split(',')


def is_wall(x, y, segments):
    """Return True if (x, y) is on any of the path segments (walls)."""
    for x1, y1, x2, y2 in segments:
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            return True
    return False


def find_shortest_path(instructions):
    """
    Finds the shortest path from (0,0) to the final destination based on a sequence of
    turn-and-step instructions while avoiding walls formed by the path itself.
    Uses a coordinate-compressed grid and Dijkstra-like search.
    """
    # Directions: left, up, right, down
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_index = 0
    start_x = start_y = 0
    current_x = current_y = 0

    wall_segments = []  # List of segments that represent walls
    x_coords = [0]
    y_coords = [0]

    for instr in instructions:
        turn_direction = instr[0]
        steps = int(instr[1:])

        # Update facing direction
        direction_index = (direction_index + (3 if turn_direction == 'L' else 1)) % 4
        dx, dy = directions[direction_index]

        # Compute next position
        next_x = current_x + dx * steps
        next_y = current_y + dy * steps

        # Record segment of the movement as a wall
        wall_segments.append((current_x, current_y, next_x, next_y))

        # Update current position
        current_x, current_y = next_x, next_y

        # Track coordinates for compression (include neighbors for safe movement)
        x_coords.extend([current_x, current_x - 1, current_x + 1])
        y_coords.extend([current_y, current_y - 1, current_y + 1])

    end_x, end_y = current_x, current_y

    # Coordinate compression
    # Remove duplicates and sort coordinates to create a compressed grid
    compressed_x = sorted(set(x_coords))
    compressed_y = sorted(set(y_coords))
    grid_width, grid_height = len(compressed_x), len(compressed_y)

    # Map start and end positions to compressed indices
    start_idx_x = compressed_x.index(start_x)
    start_idx_y = compressed_y.index(start_y)
    end_idx_x = compressed_x.index(end_x)
    end_idx_y = compressed_y.index(end_y)

    # Dijkstra-like search on compressed grid
    priority_queue = [(0, start_idx_x, start_idx_y)]  # (cost, x_index, y_index)
    visited = {}

    while priority_queue:
        current_cost, current_idx_x, current_idx_y = heapq.heappop(priority_queue)

        # Check if we reached the destination
        if current_idx_x == end_idx_x and current_idx_y == end_idx_y:
            return str(current_cost)

        # Skip if already visited with a lower cost
        node_key = (current_idx_x, current_idx_y)
        if node_key in visited and visited[node_key] <= current_cost:
            continue
        visited[node_key] = current_cost

        # Explore neighboring cells (up, down, left, right)
        for move_dx, move_dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_idx_x = current_idx_x + move_dx
            neighbor_idx_y = current_idx_y + move_dy

            # Skip out-of-bounds indices
            if not (0 <= neighbor_idx_x < grid_width and 0 <= neighbor_idx_y < grid_height):
                continue

            # Convert compressed indices back to real coordinates
            neighbor_x = compressed_x[neighbor_idx_x]
            neighbor_y = compressed_y[neighbor_idx_y]

            # Always allow start and end positions, skip walls otherwise
            if not ((neighbor_x == start_x and neighbor_y == start_y) or
                    (neighbor_x == end_x and neighbor_y == end_y)) and \
                    is_wall(neighbor_x, neighbor_y, wall_segments):
                continue

            # Cost to move is Manhattan distance between compressed grid cells
            step_cost = abs(neighbor_x - compressed_x[current_idx_x]) + \
                        abs(neighbor_y - compressed_y[current_idx_y])
            heapq.heappush(priority_queue, (current_cost + step_cost, neighbor_idx_x, neighbor_idx_y))

    return -1


def part1(filepath="../input/everybody_codes_e2025_q15_p1.txt"):
    notes = load_file(filepath)
    result = find_shortest_path(notes)
    print("Part 1:", result)


def part2(filepath="../input/everybody_codes_e2025_q15_p2.txt"):
    notes = load_file(filepath)
    result = find_shortest_path(notes)
    print("Part 2:", result)


def part3(filepath="../input/everybody_codes_e2025_q15_p3.txt"):
    notes = load_file(filepath)
    result = find_shortest_path(notes)
    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
