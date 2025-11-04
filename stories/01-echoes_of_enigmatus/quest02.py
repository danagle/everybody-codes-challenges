"""
Echoes of Enigmatus [ No. 1 ]
Quest 2: Tangled Trees
https://everybody.codes/story/1/quests/2
"""
from __future__ import annotations
from collections import deque
import dataclasses
from pathlib import Path
import re
from typing import Optional


@dataclasses.dataclass
class Node:
    rank: int
    symbol: str
    left: Optional[Node] = None
    right: Optional[Node] = None


ADD_RE = re.compile(
    r"ADD id=(-?\d+) left=\[(-?\d+),(.)\] right=\[(-?\d+),(.)\]"
)


def place_node(root: Optional[Node], node: Node) -> Node:
    if root is None:
        return node
    if node.rank < root.rank:
        root.left = place_node(root.left, node)
    else:
        root.right = place_node(root.right, node)
    return root


def get_message(root: Node) -> str:
    """Level-order traversal, returning the longest concatenated level string."""
    result = ""
    q = deque([root])
    while q:
        level_symbols = []
        for _ in range(len(q)):
            node = q.popleft()
            level_symbols.append(node.symbol)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        level_message = "".join(level_symbols)
        if len(level_message) > len(result):
            result = level_message
    return result


def parse_add(line: str):
    """Parse an ADD instruction and return id and two Nodes."""
    match = ADD_RE.match(line)
    if not match:
        raise ValueError(f"Invalid line: {line}")
    _id, lr, ls, rr, rs = match.groups()
    return (
        int(_id),
        Node(int(lr), ls),
        Node(int(rr), rs),
    )


def process_tree(filepath: str, swap_children: bool = False):
    """Build the trees and read the message."""
    lines = Path(filepath).read_text().strip().splitlines()

    left_root = right_root = None
    nodes_by_id: dict[int, tuple[Node, Node]] = {}

    for line in lines:
        if line.startswith("SWAP"):
            _id = int(line.split()[1])
            left, right = nodes_by_id[_id]

            # Swap rank/symbol always
            left.rank, right.rank = right.rank, left.rank
            left.symbol, right.symbol = right.symbol, left.symbol

            # Swap subtrees only for part3
            if swap_children:
                left.left, right.left = right.left, left.left
                left.right, right.right = right.right, left.right
            continue

        _id, left_node, right_node = parse_add(line)
        nodes_by_id[_id] = (left_node, right_node)
        left_root = place_node(left_root, left_node)
        right_root = place_node(right_root, right_node)

    return get_message(left_root) + get_message(right_root)


def part1(filepath: str = "../../input/everybody_codes_e1_q02_p1.txt"):
    print("Part 1:", process_tree(filepath))


def part2(filepath: str = "../../input/everybody_codes_e1_q02_p2.txt"):
    print("Part 2:", process_tree(filepath))


def part3(filepath: str = "../../input/everybody_codes_e1_q02_p3.txt"):
    print("Part 3:", process_tree(filepath, swap_children=True))


if __name__ == "__main__":
    part1()
    part2()
    part3()
