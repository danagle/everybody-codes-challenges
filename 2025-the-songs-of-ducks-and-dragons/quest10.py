"""
The Song of Ducks and Dragons [2025]
Quest 10: Feast on the Board
https://everybody.codes/event/2025/quests/10
"""
from collections import deque, defaultdict
from math import inf
from pathlib import Path

MOVE_DELTAS = [
    (-1, 2), (1, 2), (-1, -2), (1, -2),
    (-2, 1), (2, 1), (-2, -1), (2, -1)
]


def load_file(filepath: str):
    return [
        list(line) 
        for line in Path(filepath).read_text().strip().splitlines() 
        if line.strip()
    ]


def part1(filepath: str = "../input/everybody_codes_e2025_q10_p1.txt") -> None:
    grid = load_file(filepath)
    rows = len(grid)
    cols = len(grid[0])
    max_moves = 4
    dragon = None
    sheep_eaten = 0
    
    dragon = next(
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if grid[r][c] == 'D'
    )

    state = {dragon}
    
    for _ in range(max_moves):
        next_positions = {
            (x + dx, y + dy)
            for x, y in state
            for dx, dy in MOVE_DELTAS
        }
        for r, c in next_positions:
            if (0 <= r < rows) and (0 <= c < cols) and grid[r][c] == 'S':
                grid[r][c] = 'X'
                sheep_eaten += 1
        state = next_positions

    print("Part 1:", sheep_eaten)


def part2(filepath: str = "../input/everybody_codes_e2025_q10_p2.txt") -> None:
    grid = load_file(filepath)
    rows, cols = len(grid), len(grid[0])
    max_moves = 20

    dragon = None
    sheep = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'D':
                dragon = (r, c)
            elif grid[r][c] == 'S':
                sheep.append((r, c))
    
    # Pre-compute all sheep states
    # Map time -> (row, col) -> set of initial sheep coords at that cell.
    sheep_states = defaultdict(lambda: defaultdict(set))
    [
        sheep_states[t][(r + t, c)].add((r, c))
        for r, c in sheep
        for t in range(max_moves + 1)
        if r + t < rows
    ]

    # Breadth-First Search
    eaten = set()
    seen = set()
    queue = deque([(0, dragon[0], dragon[1])])  # (moves, row, col)

    while queue:
        dragon_state = queue.popleft()
        moves_made, r, c = dragon_state

        if moves_made > max_moves or not (0 <= r < rows and 0 <= c < cols):
            continue

        if (dragon_state) in seen:
            continue
        seen.add(dragon_state)

        # Check for sheep after first dragon move
        if moves_made > 0 and grid[r][c] != '#':
            # Dragon moves, THEN sheep move : t = moves_made - 1
            # Sheep move, THEN dragon moves : t = moves_made
            for t in (moves_made - 1, moves_made):
                if t > 0 and (r, c) in sheep_states[t]:
                    eaten.update(sheep_states[t][(r, c)])

        # Enqueue next moves
        for delta_r, delta_c in MOVE_DELTAS:
            queue.append((moves_made + 1, r + delta_r, c + delta_c))

    print("Part 2:", len(eaten))


def part3(filepath: str = "../input/everybody_codes_e2025_q10_p3.txt") -> None:
    grid = load_file(filepath)
    rows = len(grid)
    cols = len(grid[0])
    dragon = None
    sheep = set()
    
    # There are hideouts '#' clustered at the bottom
    safety = [inf for _ in range(cols)]
    
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch != '#':
                safety[c] = r + 1
                if ch == 'D':
                    dragon = (r, c)
                elif ch == 'S':
                    sheep.add((r, c))
    
    # memoization for recursion
    cache = dict()
    
    def count_sequences(dragon, sheep, sheep_turn):
        """Return number of ways the dragon can eat all the sheep."""
        nonlocal grid, rows, cols, cache
        total = 0

        if not sheep:
            return 1

        key = (dragon, frozenset(sheep), sheep_turn)
        if key in cache:
            return cache[key]

        if sheep_turn:
            any_moved = False
            for sheep_r, sheep_c in sheep:
                next_r = sheep_r + 1
                # Sheep reaches safety
                if next_r == safety[sheep_c]:
                    any_moved = True
                # Valid downward move
                elif next_r < rows and (grid[next_r][sheep_c] == '#' or (next_r, sheep_c) != dragon):
                    next_sheep = (sheep - {(sheep_r, sheep_c)}) | {(next_r, sheep_c)}
                    total += count_sequences(dragon, next_sheep, False)
                    any_moved = True

            # Sheep skip if none could move
            if not any_moved:
                total += count_sequences(dragon, sheep, False)
        else:
            for delta_r, delta_c in MOVE_DELTAS:
                next_sheep = sheep
                next_r, next_c = dragon[0] + delta_r, dragon[1] + delta_c
                # Bounds check
                if (0 <= next_r < rows) and (0 <= next_c < cols):
                    next_dragon = (next_r, next_c)
                    # Eat sheep if landing on one
                    if grid[next_r][next_c] != '#':
                        next_sheep = sheep - {next_dragon}
                    total += count_sequences(next_dragon, next_sheep, True)

        cache[key] = total

        return total

    result = count_sequences(dragon, sheep, True)

    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
