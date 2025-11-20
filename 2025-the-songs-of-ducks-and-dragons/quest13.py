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


def dial_with_allocation(filepath="../input/everybody_codes_e2025_q13_p2.txt", turns=20252025):
    notes = load_tuples(filepath)
    
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
    
    return dial_numbers[position]


def dial_with_segments(filepath="../input/everybody_codes_e2025_q13_p2.txt", turns=20252025):
    notes = load_tuples(filepath)
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
        
    return value


def dial_with_ranges(filepath="../input/everybody_codes_e2025_q13_p2.txt", turns=20252025):
    notes = load_tuples(filepath)
    value = None

    numbers = [range(1, 1+1)] \
        + [range(a, b+1, +1) for (a, b) in notes[0::2]] \
        + [range(b, a-1, -1) for (a, b) in notes[1::2][::-1]]
    
    position = turns % sum(len(rng) for rng in numbers)

    for rng in numbers:
        if len(rng) <= position:
            position -= len(rng)
        else:
            value = rng[position]
            break

    return value


def part2():
    turns = 20252025
    filepath = "../input/everybody_codes_e2025_q13_p2.txt"
    result = dial_with_segments(filepath, turns)
    print(f"Part 2: {result}")


def part3():
    turns = 202520252025
    filepath = "../input/everybody_codes_e2025_q13_p3.txt"
    result = dial_with_ranges(filepath, turns)
    print(f"Part 3: {result}")


if __name__ == "__main__":
    #import time
    #import tracemalloc

    part1()
    part2()
    #tracemalloc.start()
    #start = time.perf_counter()
    part3()
    #current, peak = tracemalloc.get_traced_memory()
    #end = time.perf_counter()
    #print(f"Elapsed: {end - start} seconds")
    #print(current, peak)

    # dial_with_allocation peak:14370911263 (14.37 GB) (19.17216 seconds)
    # dial_with_segments peak:98463 (99 KB)  (0.00089 seconds)
    # dial_with_ranges peak:120667 (121 KB)  (0.00085 seconds)