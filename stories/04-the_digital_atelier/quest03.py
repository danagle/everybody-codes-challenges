"""
The Digital Atelier [ No. 4 ]
Quest 3: Hitomezashi Sashiko Floorplan
https://everybody.codes/story/4/quests/3
"""
TOP, RIGHT, BOTTOM, LEFT = range(4)

def read_input_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        data = [line.strip() for line in f]

    width = int(data[0].split("=")[1])
    height = int(data[1].split("=")[1])
    horizontal = data[2].split("=")[1]
    vertical = data[3].split("=")[1]

    return width, height, horizontal, vertical


def count_enclosed_cells(width, height, horizontal, vertical):
    grid = [[[False] * 4 for _ in range(width)]
            for _ in range(height)]

    # Mark horizontal edges.
    for line in range(height + 1):
        start = int(horizontal[line % len(horizontal)])

        for col in range(start, width, 2):
            if line < height:
                grid[line][col][TOP] = True

            if line > 0:
                grid[line - 1][col][BOTTOM] = True

    # Mark vertical edges.
    for line in range(width + 1):
        start = int(vertical[line % len(vertical)])

        for row in range(start, height, 2):
            if line < width:
                grid[row][line][LEFT] = True

            if line > 0:
                grid[row][line - 1][RIGHT] = True

    # Count cells with all four sides.
    return sum(
        all(sides)
        for row in grid
        for sides in row
    )


def part1(filepath: str = "everybody_codes_e4_q03_p1.txt"):
    width, height, horizontal, vertical = read_input_file(filepath)
    result = count_enclosed_cells(width, height, horizontal, vertical)
    print("Part 1:", result)


def classify(length, pattern, target=None):
    period = 2 * len(pattern)
    values = [int(pattern[i % len(pattern)]) for i in range(period + 1)]

    buckets = {}

    # Prefix parity for each possible target value.
    prefix = {0: [0] * (period + 1),
              1: [0] * (period + 1)}

    for i in range(1, period + 1):
        for value in (0, 1):
            prefix[value][i] = (
                prefix[value][i - 1] ^
                (values[i] == value)
            )

    limit = min(length, period)

    for start in range(limit):
        # We need equal values at start and start + 1.
        if values[start] != values[start + 1]:
            continue

        value = values[start]
        crossing_target = value if target is None else target

        crossings = prefix[crossing_target][start] & 1

        count = (length - 1 - start) // period + 1

        key = (value, start & 1, crossings)
        buckets[key] = buckets.get(key, 0) + count

    return buckets


def most_isolated_cells(width, height, horizontal, vertical):
    rows = classify(height, horizontal)
    cols = classify(width, vertical, target=0)

    # groups[0] = number of isolated cells in region colour 0
    # groups[1] = number of isolated cells in region colour 1
    groups = [0, 0]

    for (
        (h_value, row_parity, horizontal_colour),
        row_count
    ) in rows.items():
        for (
            (v_value, col_parity, vertical_colour),
            col_count
        ) in cols.items():
            if col_parity != h_value:
                continue
            if row_parity != v_value:
                continue
            colour = (horizontal_colour + vertical_colour) & 1
            groups[colour] += row_count * col_count

    return max(groups)


def part2(filepath: str = "everybody_codes_e4_q03_p2.txt"):
    width, height, horizontal, vertical = read_input_file(filepath)
    print("Part 2:", most_isolated_cells(width, height, horizontal, vertical))


def part3(filepath: str = "everybody_codes_e4_q03_p3.txt"):
    width, height, horizontal, vertical = read_input_file(filepath)
    print("Part 3:", most_isolated_cells(width, height, horizontal, vertical))


if __name__ == "__main__":
    part1()
    part2()
    part3()
