"""
The Song of Ducks and Dragons [2025]
Quest 7: Namegraph
https://everybody.codes/event/2025/quests/7
"""
from collections import Counter
from itertools import pairwise, product
from pathlib import Path


def load_file(filepath: str) -> tuple[list[str], list[str]]:
    names, _, *rules = Path(filepath).read_text().strip().splitlines()
    return names.split(","), rules


def part1(filepath: str = "../input/everybody_codes_e2025_q07_p1.txt") -> None:
    names, rules = load_file(filepath)

    pairs = set()
    for rule in rules:
        a, b = rule.split(" > ", 1)
        pairs.update(product(a, b.split(",")))

    for name in names:
        if all(pair in pairs for pair in pairwise(name)):
            print("Part 1:", name)
            break


def part2(filepath: str = "../input/everybody_codes_e2025_q07_p2.txt") -> None:
    names, rules = load_file(filepath)

    pairs = set()
    for rule in rules:
        a, b = rule.split(" > ", 1)
        pairs.update(product(a, b.split(",")))

    total = sum(i for i, name in enumerate(names, 1) 
                if all(pair in pairs for pair in pairwise(name)))
    print("Part 2:", total)


def part3(filepath: str = "../input/everybody_codes_e2025_q07_p3.txt") -> None:
    prefixes, rules = load_file(filepath)

    mapping, pairs = dict(), set()
    for rule in rules:
        a, b = rule.split(" > ", 1)
        mapping[a] = b.split(",")
        pairs.update(product(a, mapping[a]))

    filtered_prefixes = []
    for prefix in sorted(prefixes, key=len):
        if not any(prefix.startswith(existing) for existing in filtered_prefixes):
            if all(pair in pairs for pair in pairwise(prefix)):
                filtered_prefixes.append(prefix)

    shortest, longest, num_unique = 7, 11, 0

    for prefix in filtered_prefixes:
        last_chars = Counter(prefix[-1])
        length = len(prefix)
        while length <= longest - 1:
            length += 1
            new_last_chars = Counter()
            for char, count in last_chars.items():
                for next_char in mapping.get(char, ()):
                    new_last_chars[next_char] += count
            last_chars = new_last_chars
            if length >= shortest:
                num_unique += sum(last_chars.values())

    print("Part 3:", num_unique)


if __name__ == "__main__":
    part1()
    part2()
    part3()
