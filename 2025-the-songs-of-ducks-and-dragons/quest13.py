"""
The Song of Ducks and Dragons [2025]
Quest 13: Unlocking the Mountain
https://everybody.codes/event/2025/quests/13
"""
from pathlib import Path


def load_numbers(filepath: str):
    return [
        int(n) 
        for n in Path(filepath).read_text().strip().splitlines()
    ]


def load_tuples(filepath: str):
    return [
        tuple(map(int, line.split('-'))) 
        for line in Path(filepath).read_text().strip().splitlines()
    ]


def part1(filepath="../input/everybody_codes_e2025_q13_p1.txt"):
    notes = load_numbers(filepath)
    turns = 2025
    
    left_side = []
    right_side = [1]

    for index, number in enumerate(notes):
        if index % 2 == 0:
            right_side.append(number)
        else:
            left_side.append(number)

    dial_numbers = right_side + left_side[::-1]
    position = turns % len(dial_numbers)
    
    print(f"Part 1: {dial_numbers[position]}")


def part2(filepath="../input/everybody_codes_e2025_q13_p2.txt"):
    notes = load_tuples(filepath)
    turns = 20252025
    
    left_side = []
    right_side = [1]

    for index, pair in enumerate(notes):
        a, b = pair
        numbers = [n for n in range(a, b+1)]
        if index % 2 == 0:
            right_side.extend(numbers)
        else:
            left_side.extend(numbers)

    dial_numbers = right_side + left_side[::-1]
    position = turns % len(dial_numbers)
    
    print(f"Part 2: {dial_numbers[position]}")


def part3(filepath="../input/everybody_codes_e2025_q13_p3.txt"):
    notes = load_tuples(filepath)
    turns = 202520252025
    
    left_side = []
    right_side = [1]

    for index, pair in enumerate(notes):
        a, b = pair
        numbers = [n for n in range(a, b+1)]
        if index % 2 == 0:
            right_side.extend(numbers)
        else:
            left_side.extend(numbers)

    dial_numbers = right_side + left_side[::-1]
    position = turns % len(dial_numbers)
    
    print(f"Part 3: {dial_numbers[position]}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
