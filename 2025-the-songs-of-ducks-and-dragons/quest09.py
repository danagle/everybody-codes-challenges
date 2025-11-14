"""
The Song of Ducks and Dragons [2025]
Quest 9: Encoded in the Scales
https://everybody.codes/event/2025/quests/9
"""
import numpy as np
from collections import Counter
from pathlib import Path

def load_data(filepath: str) -> list[int, int]:
    lines = Path(filepath).read_text().strip().splitlines()
    return [line.split(":", 1)[1] for line in lines]


def part1(filepath: str = "../input/everybody_codes_e2025_q09_p1.txt") -> None:
    p1, p2, child = load_data(filepath)

    result = sum(x==y for x,y in zip(child, p1)) * \
             sum(x==y for x,y in zip(child, p2))

    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2025_q09_p2.txt") -> None:
    scales = load_data(filepath)

    n = len(scales)
    total = 0

    def match_and_score(child, p1, p2):
        d1 = d2 = 0
        for c, a, b in zip(child, p1, p2):
            if c != a and c != b:
                return None
            d1 += (c == a)
            d2 += (c == b)
        return d1 * d2

    for i_child in range(n):
        for i_p1 in range(n):
            if i_p1 == i_child:
                continue
            for i_p2 in range(i_p1 + 1, n):
                if i_p2 == i_child:
                    continue

                score = match_and_score(scales[i_child], scales[i_p1], scales[i_p2])
                if score:
                    total += score

    print("Part 2:", total)
 

def part3(filepath: str = "../input/everybody_codes_e2025_q09_p3.txt"):
    scales = load_data(filepath)
    n = len(scales)
    L = len(scales[0])

    # Convert sequences to integers bitmask arrays
    # diff_mask[i][j] = bitmask of positions where scales[i] != scales[j]
    diff_mask = [[0]*n for _ in range(n)]

    for i in range(n):
        si = scales[i]
        for j in range(i+1, n):
            sj = scales[j]
            mask = 0
            for k in range(L):
                if si[k] != sj[k]:
                    mask |= 1 << k
            diff_mask[i][j] = mask
            diff_mask[j][i] = mask

    parents = list(range(n))

    def find(x):
        while parents[x] != x:
            parents[x] = parents[parents[x]]
            x = parents[x]
        return x

    def union(a, b):
        pa = find(a); pb = find(b)
        if pa != pb:
            parents[pa] = pb

    for child in range(n):
        for p1 in range(n):
            if p1 == child:
                continue

            mask = diff_mask[child][p1]
            if mask == 0:
                # p1 identical to child; any p2 works
                union(child, p1)
                continue

            # Find some p2 where every mismatched bit matches child:
            # diff_mask[child][p2] & mask == 0
            for p2 in range(n):
                if p2 == child or p2 == p1:
                    continue
                if diff_mask[child][p2] & mask == 0:
                    union(child, p1)
                    union(child, p2)
                    break  # p1 proven valid; no need for more p2s

    groups = Counter(find(i) for i in range(n))
    result = max(sum(i + 1 for i in range(n) if find(i) == root) for root in groups)

    print("Part 3:", result)


def part3_numpy(filepath: str = "../input/everybody_codes_e2025_q09_p3.txt"):
    sequences = load_data(filepath)
    scales = np.array([list(seq) for seq in sequences], dtype='U1')
    n, L = scales.shape

    # diff_mask[i,j,k] = True if scales[i,k] != scales[j,k]
    diff_mask = scales[:, np.newaxis, :] != scales[np.newaxis, :, :]

    parents = np.arange(n)

    def find(x):
        while parents[x] != x:
            parents[x] = parents[parents[x]]
            x = parents[x]
        return x

    def union(a, b):
        pa = find(a)
        pb = find(b)
        if pa != pb:
            parents[pa] = pb

    for child in range(n):
        for p1 in range(n):
            if p1 == child:
                continue

            mask = diff_mask[child, p1]  # mismatches between child and p1

            if not mask.any():
                # identical sequences
                union(child, p1)
                continue

            # Candidate p2: all positions where child != p1 must match
            candidate_mask = np.all(~(diff_mask[child] & mask), axis=1)
            candidate_mask[child] = False
            candidate_mask[p1] = False
            candidate_p2 = np.where(candidate_mask)[0]

            if candidate_p2.size > 0:
                p2 = candidate_p2[0]
                union(child, p1)
                union(child, p2)

    # Compute group sums
    roots = np.array([find(i) for i in range(n)])
    groups = Counter()
    for i, r in enumerate(roots):
        groups[r] += i + 1

    print("Part 3:", max(groups.values()))


if __name__ == "__main__":
    part1()
    part2()
    part3_numpy()
