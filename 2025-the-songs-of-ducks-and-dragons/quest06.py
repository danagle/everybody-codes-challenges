"""
The Song of Ducks and Dragons [2025]
Quest 6: Mentorship Matrix
https://everybody.codes/event/2025/quests/6
"""
from pathlib import Path

def load_data(filepath: str) -> str:
    """Load and return stripped text from a file."""
    return Path(filepath).read_text().strip()


def part1(filepath: str = "../input/everybody_codes_e2025_q06_p1.txt"):
    """Count all 'A's before each 'a' and print the total sum."""
    notes = load_data(filepath)
    count_A = 0
    total = 0

    for ch in notes:
        if ch == 'A':
            count_A += 1
        elif ch == 'a':
            total += count_A

    print("Part 1:", total)


def part2(filepath: str = "../input/everybody_codes_e2025_q06_p2.txt"):
    """Count corresponding uppercase letters before each lowercase 'a', 'b', 'c'."""
    s = load_data(filepath)
    counts = {'A': 0, 'B': 0, 'C': 0}
    result = {'a': [], 'b': [], 'c': []}

    for ch in s:
        if ch in counts:  # Uppercase
            counts[ch] += 1
        elif ch in result:  # Lowercase
            result[ch].append(counts[ch.upper()])

    total = sum(sum(lst) for lst in result.values())
    print("Part 2:", total)



def part3(filepath: str = "../input/everybody_codes_e2025_q06_p3.txt", N: int = 1000):
    """Optimized counting of uppercase letters within N chars before/after each lowercase letter."""
    notes = load_data(filepath)
    s = notes * 1000
    length = len(s)

    # Initialize prefix sums for A, B, C
    prefix = {ch: [0] * (length + 1) for ch in 'ABC'}

    for i, ch in enumerate(s):
        for key in 'ABC':
            prefix[key][i + 1] = prefix[key][i] + (1 if ch == key else 0)

    result = {'a': [], 'b': [], 'c': []}

    for i, ch in enumerate(s):
        if ch in result:
            upper = ch.upper()
            start = max(0, i - N)
            end = min(length - 1, i + N)
            count = prefix[upper][end + 1] - prefix[upper][start]
            result[ch].append(count)

    total = sum(sum(lst) for lst in result.values())
    print("Part 3:", total)


if __name__ == "__main__":
    part1()
    part2()
    part3()
