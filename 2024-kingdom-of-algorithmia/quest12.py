"""
The Kingdom of Algorithmia [2024]
Quest 12: Desert Shower
https://everybody.codes/event/2024/quests/12
"""
from math import inf
from pathlib import Path

def load_lines(filepath: str) -> list[str]:
    """Read all non-empty lines from file."""
    return Path(filepath).read_text().strip().splitlines()


def get_targets(lines: list[str]) -> list[tuple[int, int, int]]:
    """
    Parse the grid and return target positions.

    Each target is represented as a tuple:
        (x_distance, height, hardness)
    """
    targets = []
    height_offset = len(lines) - 2  # Convert to bottom-based coordinates

    for y, line in enumerate(lines[:-1]):
        for x in range(2, len(line)):
            if line[x] in {'T', 'H'}:
                hardness = 2 if line[x] == 'H' else 1
                targets.append((x - 2, height_offset - y, hardness))
    return targets


def compute_shot_ranking(distance: int, height: int, hardness: int = 1) -> int:
    """
    Checks which trajectory pattern (1, 0, -1) fits the distance and height.
    """
    for offset, multiplier in zip([1, 0, -1], [3, 2, 1]):
        required_distance = distance - (offset - height)
        if required_distance % 3 == 0:
            return multiplier * (required_distance // 3) * hardness
    return 0


def part1(filepath: str = "../input/everybody_codes_e2024_q12_p1.txt") -> None:

    targets = get_targets(load_lines(filepath))
    total = sum(compute_shot_ranking(d, h) for d, h, _ in targets)
    print("Part 1:", total)


def part2(filepath: str = "../input/everybody_codes_e2024_q12_p2.txt") -> None:

    targets = get_targets(load_lines(filepath))
    total = sum(compute_shot_ranking(d, h, hard) for d, h, hard in targets)
    print("Part 2:", total)


def get_projectile_height_power(source: tuple[int, int], target: tuple[int, int]) -> tuple[int, int]:
    """
    Compute the height and power for a projectile from a source to a target.

    Returns (height_reached, total_power) or (-1, inf) if no valid trajectory is found.
    """
    for delay in range(10):
        # Test if changing the target position by the delay
        # makes the projectile’s path valid
        tgt_x, tgt_y = target[0] - delay, target[1] - delay
        dx, dy = tgt_x - source[0], tgt_y - source[1]

        # Check each trajectory type
        # Ascending (dx == dy)
        if dx == dy and dx % 2 == 0:
            p = dx // 2
            return (p + source[1], p * (1 + source[1]))

        # Horizontal flight
        t = dx - dy
        if dx % 2 == 0:
            p = dy - dx // 2
            if 0 < t <= p:
                return (p + source[1], p * (1 + source[1]))

        # Descending
        if dx % 2 == 0 and dy % 3 == 0:
            p = dy // 3
            t = dx // 2 - 2 * dy / 3
            if t > 0:
                return (p + source[1], p * (1 + source[1]))

    # The meteor is unreachable from this catapult
    return (-1, inf)


def part3(filepath: str = "../input/everybody_codes_e2024_q12_p3.txt") -> None:
    """
    Part 3
    Calculate the lowest possible energy for the shots required to
    destroy all meteors at the highest altitudes possible.

    Algorithm:    
    For each meteor, try shooting from each catapult with up to 10 timing adjustments.
    Check if an ascending, flat, or descending trajectory fits.
    Compute the height and energy needed.
    Pick the catapult that gives the highest trajectory using the least energy.
    Sum up the energy totals for the final result.
    """
    lines = load_lines(filepath)
    meteors = [tuple(map(int, line.split())) for line in lines]
    catapults = [(0, 0), (0, 1), (0, 2)]

    total_energy = 0
    # For each meteor, compute the result for all catapults.
    for meteor in meteors:
        results = [get_projectile_height_power(catapult, meteor) for catapult in catapults]
        # Choose highest height, or lowest energy in event of a tie
        best = max(results, key=lambda x: (x[0], -x[1]))
        total_energy += best[1]

    print("Part 3:", total_energy)


if __name__ == "__main__":
    part1()
    part2()
    part3()
