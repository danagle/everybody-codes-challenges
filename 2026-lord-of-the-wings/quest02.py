from pathlib import Path


def solve(input_text: str) -> int:
    checksum = 0

    for line in input_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        tokens = line.split()

        # Collect all unique alloy IDs present in this group
        nodes = set()
        for token in tokens:
            if ">" in token:
                u, v = token.split(">")
            else:
                u, v = token.split("<")
            nodes.add(u)
            nodes.add(v)

        nodes_list = list(nodes)

        # Build adjacency matrix:
        # reachable[A][B] = True means alloy A is harder than B
        reachable = {u: {v: False for v in nodes} for u in nodes}
        for token in tokens:
            if ">" in token:
                winner, loser = token.split(">")
            elif "<" in token:
                loser, winner = token.split("<")
            reachable[winner][loser] = True

        # Floyd-Warshall Algorithm
        # Deduces all missing indirect relations (if A > K and K > B, then A > B)
        for k in nodes_list:
            for i in nodes_list:
                for j in nodes_list:
                    if reachable[i][k] and reachable[k][j]:
                        reachable[i][j] = True

        # Count total reachable alloys (win count) for each alloy
        wins_count = {}
        for u in nodes:
            wins_count[u] = sum(1 for v in nodes if reachable[u][v])

        # Sort alloys from hardest (most wins) to softest (least wins)
        ordered_alloys = sorted(nodes_list, key=lambda x: wins_count[x], reverse=True)

        # Form group number and accumulate checksum
        group_number = int("".join(ordered_alloys))
        checksum += group_number

    return checksum


def load_notes(filepath: str):
    text = Path(filepath).read_text(encoding="utf-8").strip()
    return text


def part1(filepath: str = "../input/everybody_codes_e2026_q02_p1.txt") -> None:
    notes = load_notes(filepath)
    result = solve(notes)
    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2026_q02_p2.txt") -> None:
    notes = load_notes(filepath)
    result = solve(notes)
    print("Part 2:", result)


def part3(filepath: str = "../input/everybody_codes_e2026_q02_p3.txt") -> None:
    notes = load_notes(filepath)
    result = solve(notes)
    print("Part 3:", result)


if __name__ == "__main__":
    part1()
    part2()
    part3()
