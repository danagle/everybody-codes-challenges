from pathlib import Path

DIRS = {"^": 0, ">": 1, "v": 2, "<": 3}
DR = (-1, 0, 1, 0)
DC = (0, 1, 0, -1)
NEVER = 1 << 63  # Part 1 ghosts never disappear


def read_notes(filepath: str) -> tuple[list[str], int, int]:
    grid = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    H, W = len(grid), len(grid[0])
    return grid, H, W


def find_ghosts(
    grid: list[str], H: int, W: int
) -> tuple[list[int], list[int], list[int], list[int]]:
    """Parallel lists; index i is the same ghost for its whole life."""
    row, col, direction, collisions = [], [], [], []
    for r in range(H):
        for c in range(W):
            if grid[r][c] in DIRS:
                row.append(r)
                col.append(c)
                direction.append(DIRS[grid[r][c]])
                collisions.append(0)
    return row, col, direction, collisions


def play_round(
    grid: list[str],
    row: list[int],
    col: list[int],
    direction: list[int],
    collisions: list[int],
    limit: int,
) -> tuple[list[bool], int]:
    """Advance every ghost by one round (in place).

    Returns (is_alive, hits_this_round):
    is_alive[i] is False for ghosts that reached the limit,
    hits_this_round is the total number of collisions that happened in this round.
    """
    n = len(row)
    is_alive = [True] * n
    hits_this_round = 0

    # Every ghost moves
    for i in range(n):
        r = row[i] + DR[direction[i]]
        c = col[i] + DC[direction[i]]
        if grid[r][c] == "#":
            # Encountered a wall: stay, turn clockwise, one collision
            direction[i] = (direction[i] + 1) % 4
            collisions[i] += 1
            hits_this_round += 1
            if collisions[i] >= limit:
                is_alive[i] = False  # Disappears before the ghost-ghost check
        else:
            row[i], col[i] = r, c

    # ghost-ghost collisions among the survivors: everyone on a shared cell turns around once
    by_spot: dict[tuple[int, int], list[int]] = {}
    for i in range(n):
        if is_alive[i]:
            by_spot.setdefault((row[i], col[i]), []).append(i)
    for group in by_spot.values():
        if len(group) > 1:
            for i in group:
                direction[i] = (direction[i] + 2) % 4
                collisions[i] += 1
                hits_this_round += 1
                if collisions[i] >= limit:
                    is_alive[i] = False
    return is_alive, hits_this_round


def total_collisions(filepath: str, rounds: int) -> int:
    """Part 1: Returns total collisions over a fixed number of rounds."""
    grid, H, W = read_notes(filepath)
    row, col, direction, collisions = find_ghosts(grid, H, W)
    total = 0
    for _ in range(rounds):
        _, hits = play_round(grid, row, col, direction, collisions, NEVER)
        total += hits
    return total


def last_round(filepath: str, limit: int) -> int:
    """Parts 2 and 3: Returns round in which the last ghost disappears."""
    grid, H, W = read_notes(filepath)
    row, col, direction, collisions = find_ghosts(grid, H, W)
    t = 0
    seen: dict[tuple[tuple[int, int, int], ...], tuple[int, list[int]]] = (
        {}
    )  # State signature -> (round, collisions); reset whenever a ghost disappears
    while row:
        n = len(row)
        signature = tuple(zip(row, col, direction))
        if signature in seen:
            old_t, old_collisions = seen[signature]
            dt = t - old_t  # Period of the cycle
            dh = [collisions[i] - old_collisions[i] for i in range(n)]
            # Whole periods can be skipped while no ghost reaches the limit
            skipped_periods = min(
                (limit - collisions[i] - 1) // dh[i] for i in range(n) if dh[i] > 0
            )
            t += dt * skipped_periods
            for i in range(n):
                collisions[i] += dh[i] * skipped_periods
        seen[signature] = (t, collisions[:])

        t += 1
        alive, _ = play_round(grid, row, col, direction, collisions, limit)

        # Remove the disappeared ghosts, keeping the order of the remaining
        if not all(alive):
            keep = [i for i in range(n) if alive[i]]
            row = [row[i] for i in keep]
            col = [col[i] for i in keep]
            direction = [direction[i] for i in keep]
            collisions = [collisions[i] for i in keep]
            seen = {}  # Old signatures can never match again
    return t


def part1(filepath: str = "../input/everybody_codes_e2026_q10_p1.txt") -> None:
    print("Part 1:", total_collisions(filepath, 10))


def part2(filepath: str = "../input/everybody_codes_e2026_q10_p2.txt") -> None:
    print("Part 2:", last_round(filepath, 10_000))


def part3(filepath: str = "../input/everybody_codes_e2026_q10_p3.txt") -> None:
    print("Part 3:", last_round(filepath, 1_000_000_000_000))


if __name__ == "__main__":
    part1()
    part2()
    part3()
