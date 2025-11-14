"""
The Song of Ducks and Dragons [2025]
Quest 9: Encoded in the Scales
https://everybody.codes/event/2025/quests/9
"""
from collections import defaultdict
from itertools import combinations
from operator import eq
from pathlib import Path


class DSU:
    """Disjoint Set Union"""
    def __init__(self, n):
        self.p = list(range(n))  # parents: initially each item is its own parent
        self.r = [0] * n         # rank: used to keep trees balanced

    def find(self, x):
        """Find the root representative of x's set, with path compression"""
        while x != self.p[x]:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        """Merge the sets containing a and b"""
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return  # Already in same set
        # Union by rank: attach smaller tree under larger tree
        if self.r[b] > self.r[a]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1

    def sets(self):
        """Return all disjoint sets as a collection of sets"""
        groups = defaultdict(set)
        for i in range(len(self.p)):
            groups[self.find(i)].add(i)
        return groups.values()


def load_data(filepath: str):
    """Load and encode DNA sequences from file"""
    lines = Path(filepath).read_text().strip().splitlines()
    # Translate DNA characters to numbers for efficiency
    # A->0, T->1, C->2, G->3
    dna_translator = bytes.maketrans(b"ATCG", bytes(range(4)))
    # Parse lines like "1:ATCGATCG" into (id, encoded_sequence)
    sequences = [
        (
            int(a), 
            b.encode().translate(dna_translator)
        )
        for a, b in (line.split(":") for line in lines)
    ]
    return sequences


def part1(filepath: str = "../input/everybody_codes_e2025_q09_p1.txt") -> None:
    sequences = load_data(filepath)
    (_, a), (_, b), (_, child) = sequences

    similarity = sum(map(eq, child, a)) * sum(map(eq, child, b))

    print("Part 1:", similarity)


def part2(filepath: str = "../input/everybody_codes_e2025_q09_p2.txt") -> None:
    sequences = load_data(filepath)
    total = 0

    # For each potential child
    for index, child in sequences:
        # Get all other sequences as potential parents
        parents = [seq for i, seq in sequences if i != index]
        
        # Score all pairs of parents
        for a, b in combinations(parents, 2):
            # Check all positions at once: child must match at least one parent
            if not all(c == x or c == y for c, x, y in zip(child, a, b)):
                continue
            total += sum(map(eq, child, a)) * sum(map(eq, child, b))

    print("Part 2:", total)


def part3(filepath: str = "../input/everybody_codes_e2025_q09_p3.txt") -> None:
    sequences = load_data(filepath)
    families = DSU(len(sequences))
    root = {}  # Trie root

    # Build the trie: insert each sequence and store its ID at the leaf
    for id, sequence in sequences:
        node = root
        # Navigate/create path through trie following the sequence
        for x in sequence:
            if x not in node:
                node[x] = {}
            node = node[x]
        # At the leaf, store which sequence ID ends here
        node.setdefault("ids", []).append(id - 1)

    # Compare every pair of sequences to find related sequences
    for (id_a, seq_a), (id_b, seq_b) in combinations(sequences, 2):
        # Stack stores: (current trie node, position in seq_a, position in seq_b)
        stack = [(root, 0, 0)]
        while stack:
            node, pos_a, pos_b = stack.pop()
            # If we've consumed both sequences completely
            if pos_a == len(seq_a):  # must also be == len(seq_b)
                # Check if any OTHER sequences end at this trie node
                for leaf_id in node.get("ids", []):
                    # Don't union a sequence with itself
                    if leaf_id != id_a - 1 and leaf_id != id_b - 1:
                        # This sequence matches the pattern formed by A and B
                        # So unite all three into the same family
                        families.union(leaf_id, id_a - 1)
                        families.union(leaf_id, id_b - 1)
                continue
            # Get current characters from both sequences
            a = seq_a[pos_a]
            b = seq_b[pos_b]

            # Rule 1: Always follow sequence A's character if it exists in trie
            if a in node:
                stack.append((node[a], pos_a + 1, pos_b + 1))

            # Rule 2: If sequences differ, ALSO follow sequence B's character
            # This explores both possibilities and finds sequences that match either
            if a != b and b in node:
                stack.append((node[b], pos_a + 1, pos_b + 1))

    # Find the largest family
    largest = max(families.sets(), key=len)
    print("Part 3:", sum(i+1 for i in largest))


if __name__ == "__main__":
    part1()
    part2()
    part3()
