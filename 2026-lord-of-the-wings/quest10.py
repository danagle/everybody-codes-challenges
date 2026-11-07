from pathlib import Path

DIRS = {"^": 0, ">": 1, "v": 2, "<": 3}
DR = (-1, 0, 1, 0)
DC = (0, 1, 0, -1)


def read_notes(filepath: str):
    grid = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    H, W = len(grid), len(grid[0])
    wall = [[ch == "#" for ch in row] for row in grid]
    ghosts = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch in DIRS:
                ghosts.append((r * W + c, DIRS[ch]))
    return W, H, wall, ghosts


def make_table(W, H, wall):
    # table[cell][dir] = cell landed on, or -1 if that direction is a wall
    table = [[-1] * 4 for _ in range(W * H)]
    for r in range(H):
        for c in range(W):
            if wall[r][c]:
                continue
            for d in range(4):
                rr, cc = r + DR[d], c + DC[d]
                if not wall[rr][cc]:
                    table[r * W + c][d] = rr * W + cc
    return table


def step(table, pos, dir):
    """One round, nobody dies. Mutates pos/dr, returns collisions per ghost."""
    n = len(pos)
    collisions = [0] * n
    for i in range(n):
        t = table[pos[i]][dir[i]]
        if t < 0:
            dir[i] = (dir[i] + 1) & 3  # wall: stay, turn clockwise
            collisions[i] = 1
        else:
            pos[i] = t
    seen = {}
    for i in range(n):
        seen.setdefault(pos[i], []).append(i)
    for lst in seen.values():
        if len(lst) > 1:  # shared cell: everyone turns around once
            for i in lst:
                dir[i] ^= 2
                collisions[i] += 1
    return collisions


def step_real(table, pos, dir, cnt, limit):
    """One round with the death rules."""
    n = len(pos)
    alive = [True] * n
    for i in range(n):
        t = table[pos[i]][dir[i]]
        if t < 0:
            dir[i] = (dir[i] + 1) & 3
            cnt[i] += 1
            if cnt[i] >= limit:
                alive[i] = False
        else:
            pos[i] = t
    seen = {}
    for i in range(n):
        if alive[i]:
            seen.setdefault(pos[i], []).append(i)
    for lst in seen.values():
        if len(lst) > 1:
            for i in lst:
                dir[i] ^= 2
                cnt[i] += 1
                if cnt[i] >= limit:
                    alive[i] = False
    return alive


def total_collisions(filepath, rounds=10):
    W, H, wall, gh = read_notes(filepath)
    table = make_table(W, H, wall)
    positions = [g[0] for g in gh]
    directions = [g[1] for g in gh]
    return sum(sum(step(table, positions, directions)) for _ in range(rounds))


def last_round(filepath, limit):
    W, H, wall, gh = read_notes(filepath)
    table = make_table(W, H, wall)
    pos = [g[0] for g in gh]
    direct = [g[1] for g in gh]
    cnt = [0] * len(pos)
    now = 0
    while pos:
        n = len(pos)
        # Find tail length mu and period lam of the labelled state
        # recording cumulative collisions
        seen = {}
        p2, d2 = pos[:], direct[:]
        cumulative = [
            [0] for _ in range(n)
        ]  # cumulative[i][k] = collisions of ghost i in the first k rounds
        k = 0
        while True:
            key = tuple(p2) + tuple(d2)
            if key in seen:
                mu = seen[key]
                lam = k - mu
                break
            seen[key] = k
            coll = step(table, p2, d2)
            for i in range(n):
                cumulative[i].append(cumulative[i][-1] + coll[i])
            k += 1
        seen = None
        L = mu + lam

        def count_at(i, m):  # collisions of ghost i in the first m rounds (no deaths)
            if m <= L:
                return cumulative[i][m]
            q, r = divmod(m - mu, lam)
            return cumulative[i][mu + r] + q * (cumulative[i][L] - cumulative[i][mu])

        # Earliest round in which some ghost reaches the limit
        best = None
        for i in range(n):
            need = limit - cnt[i]
            per = cumulative[i][L] - cumulative[i][mu]
            if cumulative[i][L] >= need:
                lo, hi = 0, L
            elif per == 0:
                continue  # never collides again in this cycle
            else:
                q = max((need - cumulative[i][mu] - 1) // per, 0)  # whole periods we can skip
                lo, hi = mu + q * lam, mu + (q + 2) * lam
                while count_at(i, hi) < need:
                    hi += lam
            while lo < hi:
                mid = (lo + hi) // 2
                if count_at(i, mid) >= need:
                    hi = mid
                else:
                    lo = mid + 1
            if best is None or lo < best:
                best = lo
        T = best

        # jump to just before round T, then play round T for real
        m = T - 1
        for i in range(n):
            cnt[i] += count_at(i, m)
        m_eff = mu + (m - mu) % lam if m > mu else m
        for _ in range(m_eff):
            step(table, pos, direct)
        now += m
        alive = step_real(table, pos, direct, cnt, limit)
        now += 1
        keep = [i for i in range(n) if alive[i]]
        pos = [pos[i] for i in keep]
        direct = [direct[i] for i in keep]
        cnt = [cnt[i] for i in keep]
    return now


def part1(filepath: str = "../input/everybody_codes_e2026_q10_p1.txt") -> None:
    print("Part 1:", total_collisions(filepath, 10))


def part2(filepath: str = "../input/everybody_codes_e2026_q10_p2.txt") -> None:
    print("Part 2:", last_round(filepath, 10_000))


def part3(filepath: str = "../input/everybody_codes_e2026_q10_p3.txt") -> None:
    print("Part 3:", last_round(filepath, 1_000_000_000_000))


if __name__ == "__main__":
    part1()
    part2()
    #part3()
