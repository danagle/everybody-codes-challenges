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


def part2_bruteforce(filepath="../input/everybody_codes_e2025_q13_p2.txt"):
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


def part2(filepath="../input/everybody_codes_e2025_q13_p2.txt"):
    notes = load_tuples(filepath)
    turns = 20252025
    value = None

    # Build forward (right) and backward (left) segments
    forward = []
    backward = []

    for i, (a, b) in enumerate(notes):
        if i % 2 == 0:
            forward.append((a, b, 1))    # walk a -> b
        else:
            backward.append((a, b, -1))  # walk b -> a

    # Dial order: [1], forward segments, reversed backward segments
    dial = [(1, 1, 1)]
    dial.extend(forward)
    dial.extend(reversed(backward))

    # Compute total size of the dial
    length = sum(abs(a - b) + 1 for a, b, _ in dial)

    # Effective index after wrapping
    offset = turns % length

    # Walk through segments until we land inside one
    for a, b, direction in dial:
        segment_length = (abs(b - a) + 1)

        if offset < segment_length:
            if direction == 1:
                value = a + offset
            else:
                value = b - offset

            break

        offset -= segment_length
        
    print("Part 2:", value)


def part3_bruteforce(filepath="../input/everybody_codes_e2025_q13_p3.txt"):
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


def part3(filepath="../input/everybody_codes_e2025_q13_p3.txt"):
    notes = load_tuples(filepath)
    turns = 202520252025
    result = None

    numbers = [range(1, 1+1)] \
        + [range(a, b+1, +1) for (a, b) in notes[0::2]] \
        + [range(b, a-1, -1) for (a, b) in notes[1::2][::-1]]
    
    position = turns % sum(len(rng) for rng in numbers)

    for rng in numbers:
        if len(rng) <= position:
            position -= len(rng)
        else:
            result = rng[position]
            break

    print(f"Part 3: {result}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
