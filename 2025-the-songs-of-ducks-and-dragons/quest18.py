"""
The Song of Ducks and Dragons [2025]
Quest 18: When Roots Remember
https://everybody.codes/event/2025/quests/18
"""
import re
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Tuple


def load_plants(filepath: str) -> Tuple[Dict[int, Dict], List[str]]:
    """
    Parse plant definitions and test cases from lines.
    Returns (plants, test_cases)
    """
    plants: Dict[int, Dict] = {}
    test_cases: List[str] = []
    current_plant = None

    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        # Plant line
        m = re.fullmatch(
            r"-?\s*Plant\s+(\d+)\s+with\s+thickness\s+(-?\d+):",
            line,
            re.I
        )
        if m:
            pid = int(m.group(1))
            thickness = int(m.group(2))
            plants[pid] = {"thickness": thickness, "inputs": []}
            current_plant = pid
            continue

        if current_plant is None:
            continue

        # Branch to Plant
        m = re.fullmatch(
            r"-?\s*branch\s+to\s+Plant\s+(\d+)\s+with\s+thickness\s+(-?\d+)",
            line,
            re.I
        )
        if m:
            plants[current_plant]["inputs"].append((int(m.group(1)), int(m.group(2))))
            continue

        # Free branch
        m = re.fullmatch(
            r"-?\s*free\s+branch\s+with\s+thickness\s+(-?\d+)",
            line,
            re.I
        )
        if m:
            plants[current_plant]["inputs"].append((None, int(m.group(1))))
            continue

        # Test case line
        if re.fullmatch(r"[01 ]+", line):
            test_cases.append(line)
            continue

    return dict(sorted(plants.items())), test_cases


def get_energy(
    plants: Dict[int, Dict],
    current_free: Dict[int, int],
    plant_id: int,
    cache: Dict[int, int],
    path: List[int] = None
) -> int:
    """Compute how much energy a plant outputs based on its inputs and thickness."""
    if path is None:
        path = []
    if plant_id in path:
        return 0
    if plant_id in cache:
        return cache[plant_id]
    if plant_id not in plants:
        return 0

    total = 0
    path = path + [plant_id]

    for src, w in plants[plant_id]["inputs"]:
        if src is None:  # FREE branch
            active = current_free.get(plant_id, 1)
            total += w * active
        else:
            total += w * get_energy(plants, current_free, src, cache, path)

    final = total if total >= plants[plant_id]["thickness"] else 0
    cache[plant_id] = final

    return final


def get_roots_feeding_plant(plants, pid, cache=None):
    """
    Determine which `root` plants (plants with FREE branches) 
    ultimately feed energy into the plant.
    """
    if cache is None:
        cache = {}
    if pid in cache:
        return cache[pid]
    if pid not in plants:
        return []

    roots = []
    for src, _ in plants[pid]["inputs"]:
        if src is None:
            roots.append(pid)
        else:
            roots += get_roots_feeding_plant(plants, src, cache)

    roots = list(set(roots))
    cache[pid] = roots

    return roots


def identify_clusters(plants, all_roots, last_pid):
    """
    Find groups of roots (clusters) that are interconnected via shared dependencies.
    Roots that feed the same plant become part of the same cluster.
    """
    parent = {r: r for r in all_roots}

    def find(x):
        trail = []
        while parent[x] != x:
            trail.append(x)
            x = parent[x]
        for t in trail:
            parent[t] = x
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for pid in plants:
        if pid == last_pid:
            continue
        roots = get_roots_feeding_plant(plants, pid)
        if len(roots) > 1:
            base = roots[0]
            for r in roots[1:]:
                union(base, r)

    clusters = defaultdict(list)
    for r in all_roots:
        clusters[find(r)].append(r)
    return list(clusters.values())


def hill_climb(plants, roots, last_pid, current_free):
    """Greedily flip FREE branches in a cluster to increase the energy of the last plant."""
    cache = {}
    current_max = get_energy(plants, current_free, last_pid, cache)
    improved = True

    while improved:
        improved = False
        for rid in roots:
            orig = current_free.get(rid, 0)
            toggled = 1 - orig
            current_free[rid] = toggled
            cache = {}
            new_energy = get_energy(plants, current_free, last_pid, cache)
            if new_energy > current_max:
                current_max = new_energy
                improved = True
            else:
                current_free[rid] = orig

    return current_max


def part1(filepath: str = "../input/everybody_codes_e2025_q18_p1.txt"):
    """
    What is the brightness energy of the last plant?
    """
    plants, _ = load_plants(filepath)

    last_pid = max(plants)
    current_free = {}
    cache = {}

    result = get_energy(plants, current_free, last_pid, cache)

    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2025_q18_p2.txt"):
    """
    What is the sum of the brightness energies of the last plant
    for all the test cases?
    """
    plants, test_cases = load_plants(filepath)

    last_pid = max(plants)

    free_plants = [
        pid for pid, data in plants.items()
        if any(src is None for src, _ in data["inputs"])
    ]
    free_plants.sort()

    total = 0
    for case in test_cases:
        bits = list(case.replace(" ", ""))
        current_free = {
            pid: int(bits[i]) if i < len(bits) else 0
            for i, pid in enumerate(free_plants)
        }
        cache = {}

        total += get_energy(plants, current_free, last_pid, cache)

    print("Part 2:", total)


def part3(filepath: str = "../input/everybody_codes_e2025_q18_p3.txt"):
    """
    Find the maximum energy achievable in the final plant of this setup. 
    What is the total difference in energy obtained by the dragonducks in the final
    plant compared to that maximum? 
    Include only those dragonducks who managed to activate the final plant at all.
    """
    plants, test_cases = load_plants(filepath)

    last_pid = max(plants)

    # all roots
    all_roots = [
        pid for pid, data in plants.items()
        if any(src is None for src, _ in data["inputs"])
    ]
    all_roots.sort()

    # pick best starting configuration
    best_cfg = {}
    best_energy = float("-inf")
    for case in test_cases:
        bits = list(case.replace(" ", ""))
        cfg = {
            pid: int(bits[i]) if i < len(bits) else 0
            for i, pid in enumerate(all_roots)
        }
        cache = {}
        e = get_energy(plants, cfg, last_pid, cache)
        if e > best_energy:
            best_energy = e
            best_cfg = cfg.copy()

    current_free = best_cfg

    clusters = identify_clusters(plants, all_roots, last_pid)
    for group in clusters:
        hill_climb(plants, group, last_pid, current_free)

    cache = {}
    global_max = get_energy(plants, current_free, last_pid, cache)
    total_diff = 0
    for case in test_cases:
        bits = list(case.replace(" ", ""))
        cfg = {
            pid: int(bits[i]) if i < len(bits) else 0
            for i, pid in enumerate(all_roots)
        }
        cache = {}
        e = get_energy(plants, cfg, last_pid, cache)
        if e > 0:
            global_max = max(global_max, e)
            total_diff += (global_max - e)

    print("Part 3:", total_diff)


if __name__ == "__main__":
    part1()
    part2()
    part3()
