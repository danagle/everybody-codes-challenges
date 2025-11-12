"""
The Song of Ducks and Dragons [2025]
Quest 7: Namegraph
https://everybody.codes/event/2025/quests/7
"""
from collections import Counter
from functools import cache
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


def count_iterative(prefixes, mapping):
    shortest, longest, total = 7, 11, 0
    for prefix in prefixes:
        last_chars = Counter(prefix[-1])
        length = len(prefix)
        while length < longest:
            length += 1
            new_last_chars = Counter()
            for char, count in last_chars.items():
                for next_char in mapping.get(char, ()):
                    new_last_chars[next_char] += count
            last_chars = new_last_chars
            if length >= shortest:
               total += sum(last_chars.values())
    return total


def count_recursive(prefixes, mapping):
    @cache
    def count(last_char, length):
        if length > 11:
            return 0
        total = int(length >= 7)
        for next_char in mapping.get(last_char, ()):
            total += count(next_char, length + 1)
        return total

    return sum(count(prefix[-1], len(prefix)) for prefix in prefixes)


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

    # python -m cProfile -s time quest07.py
    # 8874 function calls (8790 primitive calls) in 0.011 seconds
    # total = count_iterative(filtered_prefixes, mapping)
    # 6324 function calls (6093 primitive calls) in 0.008 seconds
    total = count_recursive(filtered_prefixes, mapping)
    
    print("Part 3:", total)


if __name__ == "__main__":
    part1()
    part2()
    part3()
