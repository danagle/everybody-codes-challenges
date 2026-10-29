from pathlib import Path


def load_notes(filepath: str):
    """Reads the file and yields (base, values) tuples for each line."""
    for line in Path(filepath).read_text(encoding="utf-8").strip().splitlines():
        if line.strip():
            base_id, values = line.split()
            base = base_id.split("-")[1]
            yield base, values


def calculate_score(base: str, values: str) -> int:
    return sum(
        int(b) ** i * int(v)
        for i, (b, v) in enumerate(zip(reversed(base), reversed(values)))
    )


def part1(filepath: str = "../input/everybody_codes_e2026_q03_p1.txt") -> None:
    total_score = sum(
        calculate_score(base, values) for base, values in load_notes(filepath)
    )

    print(f"Part 1: {total_score}")


def calculate_score_part2(base: str, values: str) -> int:
    rev_base = base[::-1]
    length = len(rev_base)
    return sum(
        int(rev_base[i % length]) ** i * int(v) for i, v in enumerate(reversed(values))
    )


def part2(filepath: str = "../input/everybody_codes_e2026_q03_p2.txt") -> None:
    total_score = sum(
        calculate_score_part2(base, values) for base, values in load_notes(filepath)
    )

    print(f"Part 2: {total_score}")


def part3(filepath: str = "../input/everybody_codes_e2026_q03_p3.txt") -> None:
    total_score = 0
    for base, values in load_notes(filepath):
        score = calculate_score_part2(base, values)
        max_val = int(values)

        if not any(
            calculate_score_part2(base, str(other_val)) == score
            for other_val in range(max_val - 1, -1, -1)
        ):
            total_score += score

    print(f"Part 3: {total_score}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
