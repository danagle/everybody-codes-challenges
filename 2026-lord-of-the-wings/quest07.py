from collections import Counter
from pathlib import Path
from re import findall

INF = 1 << 63


def read_notes(filepath: str) -> tuple[dict[int, int], dict[int, list[int]]]:
    energy = {}
    connections = {}
    for line in Path(filepath).read_text(encoding="utf-8").strip().splitlines():
        # Extract all numbers: [cuid, initial_energy, *outgoing_connections]
        nums = list(map(int, findall(r"\d+", line)))
        energy[nums[0]] = nums[1]
        connections[nums[0]] = nums[2:]
    return energy, connections


def propagate(
    clouds: dict[int, list[int]],
    energy: dict[int, int],
    start_cloud: int,
    impulse: int = 5,
    explosion: int = INF,
) -> int:
    current_energy = energy.copy()
    current_stage = Counter({(start_cloud, impulse): 1})
    exploded: set[int] = set()

    while current_stage:
        next_stage = Counter()

        for (cuid, strength), count in current_stage.items():
            if cuid in exploded or strength <= 0:
                continue
            current_energy[cuid] += count * strength
            for cid in clouds[cuid]:
                if cid not in exploded:
                    next_stage[(cid, strength - 1)] += count

        newly_exploded = [
            cuid
            for cuid, e in current_energy.items()
            if cuid not in exploded and e >= explosion
        ]

        for cuid in newly_exploded:
            exploded.add(cuid)
            current_energy[cuid] = 0
            for cid in clouds[cuid]:
                if cid not in exploded:
                    next_stage[(cid, 10)] += 1

        current_stage = next_stage

    return sum(current_energy.values())


def part1(filepath: str = "../input/everybody_codes_e2026_q07_p1.txt") -> None:
    energy, clouds = read_notes(filepath)
    start_cloud = max(clouds.keys(), key=lambda cuid: len(clouds[cuid]))
    print("Part 1:", propagate(clouds, energy, start_cloud))


def part2(filepath: str = "../input/everybody_codes_e2026_q07_p2.txt") -> None:
    energy, clouds = read_notes(filepath)
    start_cloud = max(clouds.keys(), key=lambda cuid: len(clouds[cuid]))
    print("Part 2:", propagate(clouds, energy, start_cloud, impulse=10))


def part3(filepath: str = "../input/everybody_codes_e2026_q07_p3.txt") -> None:
    energy, clouds = read_notes(filepath)
    print(
        "Part 3:",
        max(
            propagate(clouds, energy, start_cloud, impulse=10, explosion=1_000_000)
            for start_cloud in clouds.keys()
        ),
    )


if __name__ == "__main__":
    part1()
    part2()
    part3()
