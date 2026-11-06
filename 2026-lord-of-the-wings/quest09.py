from collections import defaultdict
from math import comb
from pathlib import Path
import heapq
import re


def read_notes(filepath: str) -> list[tuple[int, int]]:
    text = Path(filepath).read_text(encoding="utf-8")
    return [
        (int(g), int(l)) for g, l in re.findall(r"growth=(\d+),\s*limit=(\d+)", text)
    ]


def simulate_plant(growth: int, limit: int) -> int:
    half_delay = (growth + 1) // 2  # half-branches split again after this long
    fresh_delay = growth - 1  # a new length-1 branch splits after this long

    splits_at = defaultdict(int)  # {second: branches that split then}
    splits_at[growth] = 1

    branches = 1
    total = 1
    t = 1
    while total < limit:
        t += 1
        splits = splits_at.pop(t, 0)
        total += branches + splits
        if splits:
            branches += 2 * splits
            splits_at[t + half_delay] += 2 * splits
            splits_at[t + fresh_delay] += splits
    return t


def part1(filepath: str = "../input/everybody_codes_e2026_q09_p1.txt") -> None:
    print("Part 1:", sum(simulate_plant(g, l) for g, l in read_notes(filepath)))


def simulate_plant_leaves(growth: int, limit: int) -> int:
    half_delay = (growth + 1) // 2
    fresh_delay = growth - 1

    events = [(growth, 1)]  # heap of (second, number of branches splitting)
    leaves = 1

    while leaves < limit:
        t, count = heapq.heappop(events)
        # merge every event scheduled for the same second
        while events and events[0][0] == t:
            count += heapq.heappop(events)[1]

        leaves += count  # each split adds exactly one leaf
        if leaves >= limit:
            return t

        heapq.heappush(events, (t + half_delay, 2 * count))
        heapq.heappush(events, (t + fresh_delay, count))
    return 1  # limit <= 1


def part2(filepath: str = "../input/everybody_codes_e2026_q09_p2.txt") -> None:
    print("Part 2:", sum(simulate_plant_leaves(g, l) for g, l in read_notes(filepath)))


def leaves_at_least(g, t, limit):
    h1 = (g + 1) // 2
    g1 = g - 1
    total = 1
    a = 0
    while g + a * h1 <= t:
        base = g + a * h1
        for b in range((t - base) // g1 + 1):
            total += comb(a + b, a) << a
            if total >= limit:
                return True
        a += 1
    return total >= limit


def get_exact_growth_time(growth, limit):
    hi = growth
    while not leaves_at_least(growth, hi, limit):
        hi *= 2
    lo = 1
    while lo < hi:
        mid = (lo + hi) // 2
        if leaves_at_least(growth, mid, limit):
            hi = mid
        else:
            lo = mid + 1
    return lo


def part3(filepath: str = "../input/everybody_codes_e2026_q09_p3.txt") -> None:
    print("Part 3:", sum(get_exact_growth_time(g, l) for g, l in read_notes(filepath)))


if __name__ == "__main__":
    part1()
    part2()
    part3()
