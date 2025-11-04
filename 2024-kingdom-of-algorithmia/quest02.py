"""
The Kingdom of Algorithmia [2024]
Quest 2: The Runes of Power
https://everybody.codes/event/2024/quests/2
"""
from pathlib import Path


def part1(filepath: str = "../input/everybody_codes_e2024_q02_p1.txt"):
    """
    Count how many times the listed words appear in the text.
    """
    header, _, text = Path(filepath).read_text().strip().splitlines()

    words = header.split(":")[1].split(",")
    total = sum(text.count(word) for word in words)

    print("Part 1:", total)


def part2(filepath: str = "../input/everybody_codes_e2024_q02_p2.txt"):
    """
    Count all character positions that are part of any listed word
    (or its reverse) found in each line of the text.
    """
    header, _, *lines = Path(filepath).read_text().strip().splitlines()

    words = header.split(":")[1].split(",")
    # Include reversed versions
    words += [word[::-1] for word in words]

    def count_word_coverage(line: str) -> int:
        covered = [False] * len(line)
        for i in range(len(line)):
            for word in words:
                if line[i:i + len(word)] == word:
                    for j in range(len(word)):
                        covered[i + j] = True
        return sum(covered)

    total = sum(count_word_coverage(line) for line in lines)
    print("Part 2:", total)


def part3(filepath: str = "../input/everybody_codes_e2024_q02_p3.txt"):
    """
    Find all occurrences of listed words (and their reverses)
    horizontally (with wraparound) and vertically in a grid.
    Count how many grid positions are part of at least one match.
    """
    header, _, *lines = Path(filepath).read_text().strip().splitlines()

    words = header.split(":")[1].split(",")
    words += [word[::-1] for word in words]

    height, width = len(lines), len(lines[0])
    marked = [[False] * width for _ in range(height)]

    # --- Horizontal (wraparound) search ---
    for row_idx, line in enumerate(lines):
        double_line = line * 2  # for wraparound
        for start in range(width):
            for word in words:
                if double_line[start:start + len(word)] == word:
                    for n in range(len(word)):
                        marked[row_idx][(start + n) % width] = True

    # --- Vertical search ---
    columns = ["".join(col) for col in zip(*lines)]
    for col_idx, column in enumerate(columns):
        for start in range(height):
            for word in words:
                if column[start:start + len(word)] == word:
                    for n in range(len(word)):
                        marked[start + n][col_idx] = True

    total = sum(sum(row) for row in marked)
    print("Part 3:", total)


if __name__ == "__main__":
    part1()
    part2()
    part3()
