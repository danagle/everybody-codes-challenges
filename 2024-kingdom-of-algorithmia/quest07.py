"""
The Kingdom of Algorithmia [2024]
Quest 7: Not Fast but Furious
https://everybody.codes/event/2024/quests/7
"""
from itertools import cycle, permutations
from pathlib import Path

DELTAS = {'+': 1, '-': -1, '=': 0}

def load_race_plans(filepath: str) -> dict[str, list[str]]:
    """
    Loads the race plans for a given quest part.
    Each line is formatted as KEY:VALUE1,VALUE2,...
    """
    plans = {}

    for line in Path(filepath).read_text().splitlines():
        k,*v = line.replace(":",",").split(",")
        plans[k] = v

    return plans


def score(sequence: str) -> int:
    """
    Calculates the total score based on the sequence of symbols.
    Starting at 10, each symbol adjusts the score by DELTAS.
    """
    current = 10
    total = 0

    for symbol in sequence:
        current = max(0, current + DELTAS[symbol])
        total += current

    return total


def parse_track(track_2d: str) -> str:
    """
    Converts a 2D ASCII track representation into a linear track string.
    """
    track_grid = {
        complex(i, j): c
        for i, line in enumerate(track_2d.splitlines())
        for j, c in enumerate(line)
        if c != " "
    }

    # 1j ** i gives rotation through [1j, -1, -1j, 1] for 4 directions
    directions = [1j ** i for i in range(4)]
    path = [0j, 1j]

    while path[-1]:
        current, prev = path[-1], path[-2]
        for d in directions:
            next_pos = current + d
            if next_pos == prev:
                continue
            if next_pos in track_grid:
                path.append(next_pos)
                break

    path.pop(0)  # Remove starting point
    track_grid[0] = "="  # Replace 'S' with '='
    return "".join(track_grid[pos] for pos in path)


def apply_plan(plan: str, track: str) -> str:
    """
    Applies a repeating plan (e.g., +-=) to a track.
    '=' in track uses the plan’s character, others remain unchanged.
    """
    return "".join(
        plan_char if track_char == "=" else track_char
        for track_char, plan_char in zip(track, cycle(plan))
    )


def get_best_order(plans: dict[str, list[str]], track: str) -> str:
    """"""
    best_order = sorted(
        plans.keys(),
        reverse=True,
        key=lambda name: score(apply_plan(plans[name], track))
    )
    return "".join(best_order)


def part1(filepath: str = "../input/everybody_codes_e2024_q07_p1.txt") -> None:
    plans = load_race_plans(filepath)
    track = "=" * 10
    print("Part 1:", get_best_order(plans, track))
    
    
def part2(filepath: str = "../input/everybody_codes_e2024_q07_p2.txt") -> None:
    plans = load_race_plans(filepath)
    track_circuit = """S-=++=-==++=++=-=+=-=+=+=--=-=++=-==++=-+=-=+=-=+=+=++=-+==++=++=-=-=--
-                                                                     -
=                                                                     =
+                                                                     +
=                                                                     +
+                                                                     =
=                                                                     =
-                                                                     -
--==++++==+=+++-=+=-=+=-+-=+-=+-=+=-=+=--=+++=++=+++==++==--=+=++==+++-"""
    track = parse_track(track_circuit) * 10
    print("Part 2:", get_best_order(plans, track))


def part3(filepath: str = "../input/everybody_codes_e2024_q07_p3.txt") -> None:
    track_circuit = """S+= +=-== +=++=     =+=+=--=    =-= ++=     +=-  =+=++=-+==+ =++=-=-=--
- + +   + =   =     =      =   == = - -     - =  =         =-=        -
= + + +-- =-= ==-==-= --++ +  == == = +     - =  =    ==++=    =++=-=++
+ + + =     +         =  + + == == ++ =     = =  ==   =   = =++=
= = + + +== +==     =++ == =+=  =  +  +==-=++ =   =++ --= + =
+ ==- = + =   = =+= =   =       ++--          +     =   = = =--= ==++==
=     ==- ==+-- = = = ++= +=--      ==+ ==--= +--+=-= ==- ==   =+=    =
-               = = = =   +  +  ==+ = = +   =        ++    =          -
-               = + + =   +  -  = + = = +   =        +     =          -
--==++++==+=+++-= =-= =-+-=  =+-= =-= =--   +=++=+++==     -=+=++==+++-"""

    track = parse_track(track_circuit) * 11
    (opponent_plan,) = load_race_plans(filepath).values()
    opponent_score = score(apply_plan(opponent_plan, track))

    # Try all unique permutations of opponent plan
    candidates = { "".join(p) for p in permutations(opponent_plan) }

    better_plans = sum(
        1 for plan in candidates
        if score(apply_plan(plan, track)) > opponent_score
    )

    print("Part 3:", better_plans)


if __name__ == "__main__":
    part1()
    part2()
    part3()
