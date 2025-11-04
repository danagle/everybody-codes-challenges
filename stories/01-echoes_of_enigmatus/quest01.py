"""
Echoes of Enigmatus [ No. 1 ]
Quest 1: EniCode
https://everybody.codes/story/1/quests/1
"""
from pathlib import Path
import re


def read_input_file(filepath: str):
    return Path(filepath).read_text().strip().splitlines()


def eni_1(n: int, exp: int, mod: int) -> int:
    """
    Computes the modular powers of n up to exp, 
    records each intermediate result, 
    and returns a single large integer made by 
    concatenating the results in reverse order.
    """
    score = 1
    results = []

    for _ in range(exp):
        score = (score * n) % mod
        results.append(str(score))

    return int("".join(reversed(results)))


def eni_2(n: int, exp: int, mod: int) -> int:
    result = []

    for i in range(5):
        score = pow(n, exp - i, mod)
        result.append(str(score))

    return int("".join((result)))


def eni_3(n: int, exp: int, mod: int) -> int:
    """
    Compute S = sum_{k=1..exp} (n^k mod mod) efficiently by detecting cycles
    in the sequence of remainders and skipping full repeated cycles.

    - 'seen' maps a remainder -> (index_of_first_occurrence, cumulative_sum_after_adding_that_occurrence)
    - when a repeated remainder is found at index i, we compute the cycle length and
      the cycle sum and skip as many full cycles as possible, then continue adding the remaining terms.
    """
    seen: dict[int, tuple[int, int]] = {}  # remainder -> (index, cumulative_sum_after_that_index)
    total = 0

    # Iterate indices 0 .. exp-1 corresponding to powers n^(i+1)
    i = 0
    while i < exp:
        score = pow(n, i + 1, mod)

        if score in seen:
            prev_index, prev_cum = seen[score]
            cycle_length = i - prev_index
            # cycle_sum: sum of values from (prev_index+1) .. i inclusive
            cycle_sum = total - prev_cum + score

            # remaining terms including current index 'i'
            remaining = exp - i
            full_cycles = remaining // cycle_length

            # skip those full cycles
            total += full_cycles * cycle_sum
            i += full_cycles * cycle_length
            break

        # record cumulative sum *after* including this score (important)
        total += score
        seen[score] = (i, total)
        i += 1

    # finish any remaining terms (indices i .. exp-1)
    for j in range(i, exp):
        total += pow(n, j + 1, mod)

    return total


def solve(part_num: int) -> None:
    if part_num not in (1, 2, 3):
        return
    
    filepath = f"../../input/everybody_codes_e1_q01_p{part_num}.txt"
    lines = read_input_file(filepath)

    # Select the appropriate `eni` function
    eni = (eni_1, eni_2, eni_3)[part_num - 1]

    highest_result = 0
    for line in lines:
        a, b, c, x, y, z, m = (int(x) for x in re.findall(r"-?[0-9]+", line))
        highest_result = max(highest_result, eni(a, x, m) + eni(b, y, m) + eni(c, z, m))

    print(f"Part {part_num}:", highest_result)
    

if __name__ == "__main__":
    solve(1)
    solve(2)
    solve(3)
