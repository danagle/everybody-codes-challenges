"""
The Kingdom of Algorithmia [2024]
Quest 6: The Tree of Titans
https://everybody.codes/event/2024/quests/6
"""
from collections import defaultdict, Counter
from pathlib import Path


def load_graph(filepath: str) -> dict[str, list[str]]:
    """Parses the input file into an adjacency list (graph)."""
    graph = defaultdict(list)
    for line in Path(filepath).read_text().splitlines():
        parent, *children = line.replace(":", ",").split(",")
        graph[parent] = children
    return graph


def generate_paths(graph, node="RR", truncate=None, visited=None):
    """
    Recursively generates all possible paths in a directed graph
    starting from the given node until reaching the '@' node.
    
    Parameters:
        graph (dict): adjacency list representing the graph.
        node (str): current node being explored.
        truncate (int | None): if set, truncates each node label to this length.
        visited (set): tracks visited nodes to prevent infinite loops.
    """
    if visited is None:
        visited = set()

    # Stop recursion if a loop is detected
    if node in visited:
        return

    # End condition — reached terminal node
    if node == "@":
        yield "@"
        return

    # Explore child nodes recursively
    for child in graph[node]:
        for path in generate_paths(graph, child, truncate, visited | {node}):
            yield node[:truncate] + path


def solve(part_num: int) -> None:
    """Processes one puzzle part (1-3)."""
    filepath = f"../input/everybody_codes_e2024_q06_p{part_num}.txt"
    graph = load_graph(filepath)

    # Truncate node labels in parts 2 and 3
    truncate = None if part_num == 1 else 1

    paths = list(generate_paths(graph, truncate=truncate))
    path_lengths = Counter(map(len, paths))

    # Identify the unique (powerful) path length
    (unique_length,) = (length for length, count in path_lengths.items() if count == 1)

    # Find all paths with that unique length
    powerful_paths = [path for path in paths if len(path) == unique_length]
    
    # Print the part number and the result
    print(f"Part {part_num}: {''.join(powerful_paths)}")


if __name__ == "__main__":
    for part_num in range(1, 4):
        solve(part_num)
