"""
The Song of Ducks and Dragons [2025]
Quest 1: Whispers in the Shell
https://everybody.codes/event/2025/quests/1
"""
from pathlib import Path


def load_data(filepath: str):
    """Read list of names and instructions from the input file."""
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()
    first_line, _, last_line = lines
    names = first_line.split(',')
    instructions = [int(p[1:]) if p[0] == 'R' else -int(p[1:])
                    for p in last_line.split(',')]
    return names, instructions


def part1(filepath: str = "../input/everybody_codes_e2025_q01_p1.txt"):
    """What is your name?"""
    names, instructions = load_data(filepath)
    position, max_index = 0, len(names) - 1

    for delta in instructions:
        position = max(0, min(position + delta, max_index))

    print("Part 1:", names[position])


def part2(filepath: str = "../input/everybody_codes_e2025_q01_p2.txt"):
    """What is the name of your first parent?"""
    names, instructions = load_data(filepath)

    position = sum(instructions) % len(names)

    print("Part 2:", names[position])


def part3(filepath: str = "../input/everybody_codes_e2025_q01_p3.txt"):
    """What is the name of your second parent?"""
    names, instructions = load_data(filepath)
    num_names = len(names)

    for delta in instructions:
        delta %= num_names
        names[0], names[delta] = names[delta], names[0]

    print("Part 3:", names[0])


if __name__ == "__main__":
    part1()
    part2()
    part3()
