"""
Melody Made of Code [ No. 3 ]
Quest 2: How Quack Echoes Back
https://everybody.codes/story/3/quests/2
"""
from collections import deque
from pathlib import Path

def part1(filepath: str = "everybody_codes_e3_q02_p1.txt"):
    grid = Path(filepath).read_text().strip().splitlines()

    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == '@':
                at = r * 1j + c
            if ch == '#':
                bone = r * 1j + c

    seen = {at}
    moves = deque([-1j, 1, 1j, -1])
    steps = 0

    while at != bone:
        while at + moves[0] in seen:
            moves.rotate(-1)
        at += moves[0]
        seen.add(at)
        steps += 1
        moves.rotate(-1)

    print("Part 1:", steps)


def part2(filepath: str = "everybody_codes_e3_q02_p2.txt"):
    grid = Path(filepath).read_text().splitlines()

    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == '@':
                at = r * 1j + c
            if ch == '#':
                bone = r * 1j + c

    min_r, max_r = -1, len(grid)
    min_c, max_c = -1, len(grid[0])

    seen = {at}
    moves = deque([-1j, 1, 1j, -1])
    steps = 0

    while not all(bone+d in seen for d in moves):

        while at+moves[0] in seen or at+moves[0] == bone:
            moves.rotate(-1)

        at += moves[0]
        seen.add(at)
        steps += 1
        moves.rotate(-1)

        min_r = min(min_r, at.imag-1)
        max_r = max(max_r, at.imag+1)
        min_c = min(min_c, at.real-1)
        max_c = max(max_c, at.real+1)

        for start in {at+d for d in moves}-seen-{bone}:
            q = deque([start])
            fill = {start}
            outside = False
            while q and not outside:
                p = q.popleft()
                for d in moves:
                    nx = p + d
                    if nx.imag <= min_r or nx.imag >= max_r or nx.real <= min_c or nx.real >= max_c:
                        outside = True
                        break
                    if nx not in seen and nx!=bone and nx not in fill:
                        q.append(nx)
                        fill.add(nx)
            if not outside:
                seen |= fill

    print("Part 2:", steps)


def part3(filepath: str = "everybody_codes_e3_q02_p3.txt"):
    grid = Path(filepath).read_text().strip().splitlines()
    all_coords = {r * 1j + c for r in range(len(grid)) for c in range(len(grid[r]))}
    bones = set()

    min_r = -1
    max_r = len(grid)
    min_c = -1
    max_c = len(grid[0])

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == "@":
                at = r * 1j + c
            elif grid[r][c] == "#":
                bones.add(r * 1j + c)

    offsets = [-1j, 1, 1j, -1]
    boundary = {bone + offset for bone in bones for offset in offsets} - bones

    seen = {at}
    moves = [-1j, -1j, -1j, 1, 1, 1, 1j, 1j, 1j, -1, -1, -1]
    move_count = 0

    def floodfill(start, shortcut_outside):
        queue = deque([start])
        fill = {start}
        while len(queue) > 0:
            curr = queue.popleft()
            for offset in moves:
                nx = curr + offset
                if nx.imag < min_r or nx.imag > max_r or nx.real < min_c or nx.real > max_c:
                    if shortcut_outside: return (True, set())
                    else: continue
                if nx in bones or nx in seen or nx in fill: continue
                queue.append(nx)
                fill.add(nx)
        return (False, fill)

    _, reachable = floodfill(min_r * 1j + min_c, False)
    seen |= all_coords - reachable

    while True:
        if boundary <= seen: break
        
        while at + moves[0] in seen or at + moves[0] in bones:
            moves.append(moves.pop(0))
        
        at += moves[0]
        seen.add(at)
        move_count += 1
        moves.append(moves.pop(0))

        min_r = min(min_r, at.imag - 1)
        max_r = max(max_r, at.imag + 1)
        min_c = min(min_c, at.real - 1)
        max_c = max(max_c, at.real + 1)
        
        adj_empty = {at + offset for offset in moves} - seen - bones
        
        for start in adj_empty:
            outside, fill = floodfill(start, True)
            if not outside:
                seen |= fill

    print("Part 3:", move_count)


if __name__ == "__main__":
    part1()
    part2()
    part3()
