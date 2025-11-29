"""
The Song of Ducks and Dragons [2025]
Quest 16: Harmonics of Stone
https://everybody.codes/event/2025/quests/16
"""
from pathlib import Path
from math import prod


def load_numbers(filepath: str):
    """Reads list of numbers from the input file."""
    return [
        int(n)
        for n in Path(filepath).read_text(encoding="utf-8").strip().split(',')
    ]


def part1(filepath="../input/everybody_codes_e2025_q16_p1.txt"):
    """
    How many blocks are needed to build a wall with a length of
    90 columns according to the spell?
    """
    numbers = load_numbers(filepath)

    length = 90  # Number of wall positions

    total = sum(length // n for n in numbers)

    print("Part 1:", total)


def get_spell_numbers(numbers):
    """
    Extracts the spell numbers used to construct the wall.
    """
    # Number of wall positions
    length = len(numbers)

    # Simulated wall heights
    simulated = [0] * length

    spell_numbers = []

    # Walk through each wall position
    for i in range(length):
        real = numbers[i]    # actual wall height at position i
        simh = simulated[i]  # current simulated height at position i

        # A new spell is needed if the real height exceeds the current simulated height
        if real > simh:
            diff = real - simh
            pos = i + 1  # spell number is 1-based index

            spell_numbers.append(pos)

            # Apply the spell: raise every multiple of 'pos' starting at i
            j = i
            while j < length:
                simulated[j] += diff
                j += pos

    # Return all discovered spell numbers
    return spell_numbers


def part2(filepath="../input/everybody_codes_e2025_q16_p2.txt"):
    """
    Find the spell that generated the wall fragment and calculate
    the product of all numbers from the spell.
    """
    numbers = load_numbers(filepath)

    spells = get_spell_numbers(numbers)

    print("Part 2:", prod(spells))


def part3(filepath="../input/everybody_codes_e2025_q16_p3.txt"):
    """
    How long is the wall (in columns) if the spell had 202,520,252,025,000 
    blocks to use?
    """
    numbers = load_numbers(filepath)

    # The limit we must not exceed when summing contributions of spells
    target = 202520252025000

    # Compute spell numbers
    spells = get_spell_numbers(numbers)
    spells_local = spells

    # Binary search boundaries for the answer
    low, high = 1, target
    result = 0

    # Standard binary search: find the largest mid such that cost(mid) <= target
    while low <= high:
        mid = (low + high) // 2

        # Compute cost = sum(mid // s for s in spells)
        cost = 0
        for s in spells_local:
            div = mid // s

            # If mid < s then mid // s == 0, and every larger s contributes 0.
            # So we can stop immediately.
            if div == 0:
                break

            cost += div

            # If the cost already exceeds the target, no need to continue.
            if cost > target:
                break

        # If cost is valid, this mid is feasible -> try larger values
        if cost <= target:
            result = mid
            low = mid + 1
        else:
            # Cost too high -> mid is too big
            high = mid - 1

    # Print the maximum feasible mid
    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
