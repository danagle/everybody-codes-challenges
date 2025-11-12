"""
The Song of Ducks and Dragons [2025]
Quest 7: Namegraph
https://everybody.codes/event/2025/quests/7
"""
from collections import Counter
from functools import cache
from itertools import pairwise, product
from pathlib import Path


class TrieNode:
    __slots__ = ("children", "is_end")
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def has_prefix(self, word: str) -> bool:
        """
        Returns True if any stored word is a prefix of the given word.
        """
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
            if node.is_end:
                return True
        return False

    def insert(self, word: str) -> None:
        """
        Inserts the word into the trie.
        """
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True


def load_file(filepath: str) -> tuple[list[str], list[str]]:
    names, _, *rules = Path(filepath).read_text().strip().splitlines()
    return names.split(","), rules


def get_pairs_mapping(rules):
    mapping, pairs = dict(), set()
    for rule in rules:
        a, b = rule.split(" > ", 1)
        mapping[a] = b.split(",")
        pairs.update(product(a, mapping[a]))
    return pairs, mapping


def get_filtered(prefixes, pairs):
    filtered = []
    for prefix in sorted(prefixes, key=len):
        if not any(prefix.startswith(existing) for existing in filtered):
            if all(pair in pairs for pair in pairwise(prefix)):
                filtered.append(prefix)
    return filtered


def get_filtered_trie(prefixes, pairs):
    trie = Trie()
    filtered = []
    for prefix in sorted(prefixes, key=len):
        if not trie.has_prefix(prefix):
            if all(pair in pairs for pair in pairwise(prefix)):
                trie.insert(prefix)
                filtered.append(prefix)
    return filtered


def part1(filepath: str = "../input/everybody_codes_e2025_q07_p1.txt") -> None:
    names, rules = load_file(filepath)

    pairs, _ = get_pairs_mapping(rules)

    for name in names:
        if all(pair in pairs for pair in pairwise(name)):
            print("Part 1:", name)
            break


def part2(filepath: str = "../input/everybody_codes_e2025_q07_p2.txt") -> None:
    names, rules = load_file(filepath)

    pairs, _ = get_pairs_mapping(rules)

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

    pairs, mapping = get_pairs_mapping(rules)

    # 7359 function calls (7128 primitive calls) in 0.009 seconds
    # filtered = get_filtered(prefixes, pairs)
    # 7064 function calls (6833 primitive calls) in 0.009 seconds
    filtered = get_filtered_trie(prefixes, pairs)

    # python -m cProfile -s time quest07.py
    # 8874 function calls (8790 primitive calls) in 0.011 seconds
    # total = count_iterative(filtered_prefixes, mapping)
    # 6324 function calls (6093 primitive calls) in 0.008 seconds
    total = count_recursive(filtered, mapping)
    
    print("Part 3:", total)


if __name__ == "__main__":
    part1()
    part2()
    part3()
