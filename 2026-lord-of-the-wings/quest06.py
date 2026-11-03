from collections import defaultdict
from pathlib import Path


def read_notes(filename: str) -> list[tuple(str, list[str])]:
    lines = Path(filename).read_text(encoding="utf-8").splitlines()
    records = []
    for line in lines:
        product, ingredients = line.split(":")
        records.append((product, ingredients.split(",")))
    return records


def bfs(graph, null):
    q = [null]
    seen = set()
    for item in q:
        for neighbor in graph.get(item, set()):
            if neighbor in seen:
                continue
            seen |= {neighbor}
            q += (neighbor,)

    return seen - {null}


def part1(filepath: str = "../input/everybody_codes_e2026_q06_p1.txt") -> None:
    records = read_notes(filepath)

    graph = defaultdict(set)
    for product, ingredients in records:
        graph[product] = set(ingredients)

    print("Part 1:", len(bfs(graph, "NULL")))


def part2(filepath: str = "../input/everybody_codes_e2026_q06_p2.txt") -> None:
    records = read_notes(filepath)

    graph = defaultdict(set)
    for product, ingredients in records:
        for ingredient in ingredients:
            graph[ingredient].add(product)

    print("Part 2:", len(bfs(graph, "NULL")))


def part3(filepath: str = "../input/everybody_codes_e2026_q06_p3.txt") -> None:
    records = read_notes(filepath)

    graph = defaultdict(set)
    for product, ingredients in records:
        for ingredient in ingredients:
            graph[ingredient].add(product)

    v1 = bfs(graph, "NULLv1")
    v2 = bfs(graph, "NULLv2")
    v3 = bfs(graph, "NULLv3")
    common = (v1 & v2) | (v2 & v3) | (v1 & v3)

    print("Part 3:", len(common))


if __name__ == "__main__":
    part1()
    part2()
    part3()
