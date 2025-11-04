"""
The Kingdom of Algorithmia [2024]
Quest 20: Gliding Finale
https://everybody.codes/event/2024/quests/20
"""
from collections import defaultdict, deque
from math import inf
from pathlib import Path


def part1(filepath: str = "../input/everybody_codes_e2024_q20_p1.txt"):
    """
    Explore all possible paths up to 100 moves.
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    delta = {'+': +1, '-': -2}
    max_steps, start_altitude = 100, 1000

    grid = Path(filepath).read_text().strip().splitlines()
    R, C = len(grid), len(grid[0])

    start = None
    for r, cols in enumerate(grid):
        for c, cell in enumerate(cols):
            if cell == 'S':
                start = (r, c)
                break

    # Each state: (step, row, col, altitude, direction)
    queue = deque()
    for d in range(4):  # Start facing each possible direction
        queue.append((0, start[0], start[1], start_altitude, d))

    seen = set()
    best_altitude = -inf

    while queue:
        steps, r, c, altitude, facing = queue.popleft()

        # Stop when we’ve taken exactly max_steps moves
        if steps == max_steps:
            best_altitude = max(best_altitude, altitude)
            continue

        # Avoid revisiting the same state
        state = (r, c, altitude, facing)
        if state in seen:
            continue
        seen.add(state)

        # Try turning or going straight
        for turn in [3, 0, 1]:  # left, straight, right relative turns
            new_dir = (facing + turn) % 4
            dr, dc = directions[new_dir]
            nr, nc = r + dr, c + dc

            # Stay within bounds and avoid walls
            if not (0 <= nr < R and 0 <= nc < C):
                continue
            cell = grid[nr][nc]
            if cell == "#":
                continue

            # Update altitude based on cell type
            new_altitude = altitude + delta.get(cell, -1)

            # Add next state
            queue.append((steps + 1, nr, nc, new_altitude, new_dir))

    print("Part 1:", best_altitude)


def part2(filepath: str = "../input/everybody_codes_e2024_q20_p2.txt"):
    """
    The grid contains checkpoints A → B → C → S that must be visited in order.
    Movement depends on direction (N, E, S, W), and each cell modifies altitude:
      '.'  → -1 altitude
      '+'  → +1 altitude
      '-'  → -2 altitude

    The goal is to return to 'S' (after visiting A, B, and C) with altitude ≥ 10,000,
    minimizing the number of steps.
    """

    # Parse input
    grid = Path(filepath).read_text().strip().splitlines()
    nrows, ncols = len(grid), len(grid[0])

    # Identify checkpoints
    next_target: dict[str | None, tuple[tuple[int, int], str]] = {}
    for r, columns in enumerate(grid):
        for c, cell in enumerate(columns):
            match cell:
                case 'A':
                    next_target[None] = ((r, c), 'A')
                case 'B':
                    next_target['A'] = ((r, c), 'B')
                case 'C':
                    next_target['B'] = ((r, c), 'C')
                case 'S':
                    start = (r, c)
                    next_target['C'] = ((r, c), 'S')
                case _:  # ignore all other characters
                    pass

    # Configuration constants
    DELTA = {'+': +1, '-': -2}  # Altitude adjustments
    VALID_TURNS = {             # Allowed direction changes
        'N': "NEW",             # from N: turn N, E, or W
        'E': "NES",             # from E: turn N, E, or S
        'S': "ESW",             # from S: turn E, S, or W
        'W': "NSW",             # from W: turn N, S, or W
    }

    START_ALT = 10_000
    ALT_RANGE = 100             # max altitude deviation allowed

    # BFS queue initialization
    # state: (altitude, row, col, last_checkpoint, direction)
    q = deque([(START_ALT, start[0], start[1], None, 'S')])
    seen = defaultdict(int)
    seen[(start[0], start[1], None, 'S')] = START_ALT

    # BFS traversal
    steps = 0
    result = 0

    while q and not result:
        for _ in range(len(q)):  # process one BFS layer
            altitude, r, c, last_cp, direction = q.popleft()

            for new_dir in VALID_TURNS[direction]:
                r2 = r + (new_dir == 'S') - (new_dir == 'N')
                c2 = c + (new_dir == 'E') - (new_dir == 'W')

                # Check bounds and obstacles
                if not (0 <= r2 < nrows and 0 <= c2 < ncols):
                    continue
                if grid[r2][c2] == '#':
                    continue

                # Compute new altitude
                new_altitude = altitude + DELTA.get(grid[r2][c2], -1)
                if not (START_ALT - ALT_RANGE <= new_altitude <= START_ALT + ALT_RANGE):
                    continue

                # Check for checkpoint progression
                next_cp = last_cp
                if (r2, c2) == next_target[last_cp][0]:
                    next_cp = next_target[last_cp][1]

                    # If we returned to 'S' with enough altitude → success
                    if next_cp == 'S' and new_altitude >= START_ALT:
                        result = steps + 1
                        break

                # Skip if we've seen this state with a higher or equal altitude
                state = (r2, c2, next_cp, new_dir)
                if seen[state] >= new_altitude:
                    continue

                seen[state] = new_altitude
                q.append((new_altitude, r2, c2, next_cp, new_dir))

            if result:
                break
        steps += 1

    print("Part 2:", result)


def part3():
    """
    Check the input file to determine the location of the best column.
    """
    distance_south = 0
    altitude = 384_400
    # Best column is 5 segments to the West of start position
    altitude -= 5
    # Pattern in column repeats "+..."
    while altitude > 0:
        distance_south += 1
        if (distance_south + 3) % 4 == 0:
            altitude += 1
        else:
            altitude -= 1

    print("Part 3:", distance_south)

    # Simpler solution:
    altitude_start = 384_400 - 5
    # Each 4-step cycle decreases altitude by 2.
    distance_south = (((altitude_start + 1) // 2) * 4) - 1
    print("Part 3 with equation:", distance_south)


if __name__ == "__main__":
    part1()
    part2()
    part3()
