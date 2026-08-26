"""
Melody Made of Code [ No. 3 ]
Quest 3: Plug and Play
https://everybody.codes/story/3/quests/3
"""
from __future__ import annotations
from dataclasses import dataclass, fields
from pathlib import Path


@dataclass
class Node:
    id: int
    plug: list[str]
    left_plug: list[str]
    right_plug: list[str]
    left: Node | None = None
    right: Node | None = None
    data: str | None = None

    def swap(self, other):
        for f in fields(self):
            a, b = getattr(self, f.name), getattr(other, f.name)
            setattr(self, f.name, b)
            setattr(other, f.name, a)


def node_elements(filepath):
    for line in Path(filepath).read_text().strip().splitlines():
        id, plug, left, right, data = (p.split("=", 1)[1] for p in line.split(", "))
        yield int(id), plug.split(), left.split(), right.split(), data


def tree_checksum(filename, insert_fn):
    root = None
    for id, plug, left, right, _ in node_elements(filename):
        node = Node(id, plug, left, right)
        if root is None:
            root = node
        else:
            while not insert_fn(root, node):
                pass

    def checksum(node, i):
        if node is None:
            return 0, 0
        l, lc = checksum(node.left, i)
        r, rc = checksum(node.right, i + lc + 1)
        return l + node.id * (i + lc) + r, lc + rc + 1

    return checksum(root, 1)[0]


def insert(current, node):
    return (current.left is None and node.plug == current.left_plug and _set(current, "left", node)
            or (current.left and insert(current.left, node))
            or current.right is None and node.plug == current.right_plug and _set(current, "right", node)
            or (current.right and insert(current.right, node)))

def _set(node, side, child):
    setattr(node, side, child)
    return True


def _bonds_match(plug, socket):
    return plug[0] == socket[0] or plug[1] == socket[1]


def insert_bonds(current, node):
    for side in ("left", "right"):
        child = getattr(current, side)
        if child is None:
            if _bonds_match(node.plug, getattr(current, f"{side}_plug")):
                return _set(current, side, node)
        elif insert_bonds(child, node):
            return True
    return False


def insert_break_bonds(current, node):
    for side in ("left", "right"):
        child = getattr(current, side)
        socket = getattr(current, f"{side}_plug")
        if child is None:
            if _bonds_match(node.plug, socket):
                return _set(current, side, node)
        else:
            if node.plug == socket and child.plug != socket:
                node.swap(child)
            elif insert_break_bonds(child, node):
                return True
    return False


if __name__ == "__main__":
    print("Part 1:", tree_checksum("everybody_codes_e3_q03_p1.txt", insert))
    print("Part 2:", tree_checksum("everybody_codes_e3_q03_p2.txt", insert_bonds))
    print("Part 3:", tree_checksum("everybody_codes_e3_q03_p3.txt", insert_break_bonds))
