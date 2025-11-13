"""
The Song of Ducks and Dragons [2025]
Quest 8: The Art of Connection
https://everybody.codes/event/2025/quests/8
"""
from collections import defaultdict
from itertools import combinations, pairwise
from pathlib import Path


class BIT:
    """Fenwick Tree for range sum queries"""
    def __init__(self, n):
        self.n = n + 2
        self.tree = [0] * self.n

    def add(self, i, x=1):
        while i < self.n:
            self.tree[i] += x
            i += i & -i

    def query(self, i):
        res = 0
        while i > 0:
            res += self.tree[i]
            i -= i & -i
        return res

    def range_query(self, left, right):
        return self.query(right) - self.query(left - 1)


def load_data(filepath: str) -> complex:
    return [int(s) for s in Path(filepath).read_text().strip().split(",")]


def part1(filepath: str = "../input/everybody_codes_e2025_q08_p1.txt") -> None:
    sequence = load_data(filepath)
    half = max(sequence) // 2
    total = sum(((a - b) % half == 0) for a, b in pairwise(sequence))

    print(f"Part 1: {total}")


def intersects(p, q):
    """Return True if chords intersect inside the circle."""
    if (p[0] in q) or (p[1] in q):
        return False
    # XOR: True if exactly one endpoint of `q` lies strictly between `p` endpoints
    return (p[0] < q[0] < p[1]) ^ (p[0] < q[1] < p[1])


def part2_bruteforce(chords):
    m = len(chords)
    total = sum(
        intersects(chords[i], chords[j])
        for i in range(m)
        for j in range(i + 1, m)
    )

    print("Part 2:", total)


def part2_fenwick(chords):
    # Sort chords by left endpoint
    chords.sort(key=lambda x: x[0])
    max_point = max(max(a, b) for a, b in chords) + 1
    bit = BIT(max_point)

    total = 0
    for a, b in chords:
        # Count how many right endpoints are inside (a,b)
        total += bit.query(b - 1) - bit.query(a)
        # Add this chord's right endpoint to the BIT
        bit.add(b)

    print("Part 2:", total)


def part2(filepath = "../input/everybody_codes_e2025_q08_p2.txt"):
    sequence = load_data(filepath)
    chords = [(min(a, b), max(a, b)) for a, b in pairwise(sequence)]
    #part2_bruteforce(chords)
    part2_fenwick(chords)


def part3_bruteforce(chords):
    num_points = 256
    max_crosses = 0
    
    for a, b in combinations(range(1, num_points + 1), 2):
        count = sum(intersects((a, b), chord) for chord in chords)
        max_crosses = max(max_crosses, count)

    print("Part 3:", max_crosses)


def part3_slidingwindow(sequence):
    num_points = max(sequence)
    upper_bounds = num_points + 1
    best = 0

    # Frequency matrix of chords
    frequency = [[0] * upper_bounds for _ in range(upper_bounds)]
    for a, b in pairwise(sequence):
        frequency[a][b] += 1
        frequency[b][a] += 1

    # Precompute cumulative sums per row
    sums = [[0] * upper_bounds for _ in range(upper_bounds)]
    for a in range(1, upper_bounds):
        for b in range(1, upper_bounds):
            sums[a][b] = sums[a][b-1] + frequency[a][b]

    # Sweep across all possible chords
    for a in range(1, upper_bounds):
        count = 0
        for b in range(a+2, upper_bounds):
            # Add chords that start crossing at the new boundary
            count += sums[b-1][a-1] + sums[b-1][num_points] - sums[b-1][b]
            # Remove chords that stop crossing when window expands
            count -= sums[b][b-2] - sums[b][a]
            # Update the best result
            best = max(best, count + frequency[a][b])

    print("Part 3:", best)


def part3_sweep(chords):
    n = 256
    best = 0

    # Build all chords from consecutive pairs and count duplicates
    chord_count = defaultdict(int)
    for a, b in chords:
        chord_count[(a, b)] += 1

    # Iterate over all possible line starting points
    for a in range(1, n + 1):
        # delta[b] will track how many chords start/end contributing as b moves
        delta = [0] * (n + 3)  # padding to simplify range updates

        # Process each chord occurrence
        for lo, hi in chords:
            # Skip chords that share the start point a; handled separately
            if a == lo or a == hi:
                continue
            # Skip chords entirely before a (they can't intersect)
            if hi <= a:
                continue

            # Case 1: a is outside the chord, chord contributes when b is strictly between endpoints
            if not (lo < a < hi):
                start = max(lo + 1, a + 2)  # b must be at least a+2
                end = hi - 1  # exclude hi itself to avoid endpoint count
                if start <= end:
                    delta[start] += 1
                    delta[end + 1] -= 1

            # Case 2: a is inside the chord, chord contributes for b outside the chord
            else:
                # Range before the chord
                start1, end1 = max(a + 2, 1), lo - 1
                if start1 <= end1:
                    delta[start1] += 1
                    delta[end1 + 1] -= 1
                # Range after the chord
                start2, end2 = hi + 1, n
                if start2 <= end2:
                    delta[start2] += 1
                    delta[end2 + 1] -= 1

        # Sweep b across possible line endpoints and compute total intersections
        running = 0
        for b in range(a + 2, n + 1):
            running += delta[b]
            # Include exact chord (a,b) if it exists
            total = running + chord_count.get((a, b), chord_count.get((b, a), 0))
            if total > best:
                best = total

    print("Part 3:", best)


def part3_improvedsweep(chords):
    chord_count = defaultdict(int)
    for lo, hi in chords:
        chord_count[(lo, hi)] += 1

    n = 256
    best = 0

    for a in range(1, n + 1):
        delta = [0] * (n + 3)
        for lo, hi in chords:
            if a == lo or a == hi or hi <= a:
                continue
            if not (lo < a < hi):
                # Case: a outside chord
                start = max(lo + 1, a + 2)
                end = hi - 1
                if start <= end:
                    delta[start] += 1
                    delta[end + 1] -= 1
            else:
                # Case: a inside chord
                start1, end1 = max(a + 2, 1), lo - 1
                if start1 <= end1:
                    delta[start1] += 1
                    delta[end1 + 1] -= 1
                start2, end2 = hi + 1, n
                if start2 <= end2:
                    delta[start2] += 1
                    delta[end2 + 1] -= 1
        running = 0
        for b in range(a + 2, n + 1):
            running += delta[b]
            total = running + chord_count.get((a,b), chord_count.get((b,a),0))
            best = max(best, total)
    print("Part 3:", best)


def part3(filepath = "../input/everybody_codes_e2025_q08_p3.txt"):
    sequence = load_data(filepath)
    #chords = [(min(a, b), max(a, b)) for a, b in pairwise(sequence)]
    #part3_bruteforce(chords)
    part3_slidingwindow(sequence)
    #part3_sweep(chords)
    #part3_improvedsweep(chords)
    #part3_fenwick(chords)


if __name__ == "__main__":
    part1()
    part2()
    part3()
