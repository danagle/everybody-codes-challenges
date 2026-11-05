from pathlib import Path

DR, DL, L, UL, UR, R = range(6)
DIRECTIONS = [DR, DL, L, UL, UR, R]


def read_notes(filepath: str) -> dict[tuple[int, int], int]:
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    grid = {}

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char.isdigit():
                grid[(r, c)] = int(char)

    return grid


def get_energized_cells(
    grid: dict[tuple[int, int], int], direction: int
) -> list[tuple[int, int]]:
    """Ray-tracing and shadow propagation for a single direction."""
    rays = {}
    for r, c in grid:
        if direction in (DR, UL):
            key = c - r
        elif direction in (DL, UR):
            key = r + c
        elif direction in (L, R):
            key = r
        rays.setdefault(key, []).append((r, c))

    energized = []
    for key, cells in rays.items():
        # Sort cells in upstream-to-downstream order
        if direction in (DR, DL):
            cells.sort(key=lambda x: x[0])  # r ascending
        elif direction == L:
            cells.sort(key=lambda x: x[1], reverse=True)  # c descending
        elif direction in (UL, UR):
            cells.sort(key=lambda x: x[0], reverse=True)  # r descending
        elif direction == R:
            cells.sort(key=lambda x: x[1])  # c ascending

        current_max_shadow = 0
        prev_rc = None

        for r, c in cells:
            if prev_rc is not None:
                r_prev, c_prev = prev_rc
                steps = abs(c - c_prev) // 2 if direction in (L, R) else abs(r - r_prev)
                current_max_shadow = max(0, current_max_shadow - steps)

            h = grid[(r, c)]
            if h > current_max_shadow:
                energized.append((r, c))
            current_max_shadow = max(current_max_shadow, h)
            prev_rc = (r, c)

    return energized


def part1(filepath: str = "../input/everybody_codes_e2026_q08_p1.txt") -> None:
    grid = read_notes(filepath)
    result = len(get_energized_cells(grid, DR))
    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2026_q08_p2.txt") -> None:
    grid = read_notes(filepath)
    result = sum(len(get_energized_cells(grid, d)) for d in DIRECTIONS)
    print("Part 2:", result)


def part3(filepath: str = "../input/everybody_codes_e2026_q08_p3.txt", target_warriors: int = 100000) -> None:
    grid = read_notes(filepath)

    seeds = {}
    total_energy = 0
    total_warriors = 0
    round_num = 0

    while total_warriors < target_warriors:
        round_num += 1
        direction = DIRECTIONS[(round_num - 1) % 6]

        # Sprout seeds whose underground timer hits 1 at the start of the round
        sprouted = []
        for rc, timer in seeds.items():
            if timer == 1:
                sprouted.append(rc)
            else:
                seeds[rc] = timer - 1

        for rc in sprouted:
            del seeds[rc]
            grid[rc] = 1

        # Get energized cells for this round
        energized_cells = get_energized_cells(grid, direction)
        total_energy += len(energized_cells)

        # Apply growth and warrior graduation
        new_seeds = {}
        for r, c in energized_cells:
            h = grid[(r, c)]
            if h == 9:
                total_warriors += 1
                new_seeds[(r, c)] = 4  # Underground for next 3 rounds
                del grid[(r, c)]
            else:
                grid[(r, c)] = h + 1

        seeds.update(new_seeds)

    print("Part 3:", total_energy)


if __name__ == "__main__":
    part1()
    part2()
    part3()
