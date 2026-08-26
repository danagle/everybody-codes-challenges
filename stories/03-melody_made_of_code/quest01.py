"""
Melody Made of Code [ No. 3 ]
Quest 1: Scales, Bags and a Bit of a Mess
https://everybody.codes/story/3/quests/1
"""
from pathlib import Path


def decode_line(line):
    label, components_str = line.split(':')
    binary_str = ''.join("01"[ch.isupper()] if ch.isalpha() else ch for ch in components_str)
    return label, *[int(x,2) for x in binary_str.split()]


def part1(filepath: str = "everybody_codes_e3_q01_p1.txt"):
    text = Path(filepath).read_text().strip()
    answer = 0

    for line in text.splitlines():
        label, r, g, b = decode_line(line)
        if r < g > b:
            answer += int(label)

    print("Part 1:", answer)


def part2(filepath: str = "everybody_codes_e3_q01_p2.txt"):
    text = Path(filepath).read_text().strip()

    #best = ('', -1, 10**9)  # label, shine, colour_sum
    #for line in text.splitlines():
    #    label, r, g, b, s = decode_line(line)
    #    colour_sum = r + g + b
    #    if s > best[1] or (s == best[1] and colour_sum < best[2]):
    #        best = (label, s, colour_sum)

    best = max(map(decode_line, text.splitlines()),
           key=lambda t: (t[4], -(t[1]+t[2]+t[3])))

    print("Part 2:", best[0])


def part3(filepath: str = "everybody_codes_e3_q01_p3.txt"):
    text = Path(filepath).read_text().strip()

    # 6 groups: red-matte, red-shiny, green-matte, green-shiny, blue-matte, blue-shiny.
    groups = [[] for _ in range(6)]

    for line in text.splitlines():
        label, r, g, b, s = decode_line(line)

        # Shine classification
        if 30 < s < 33:
            continue
        shine_class = s > 32
        
        # Dominant colour detection
        rgb = [r, g, b]
        if rgb.count(max(rgb)) > 1:
            continue
        # index = shine_class + 0 / 2 / 4 depending on colour
        colour = rgb.index(max(rgb))
        groups[shine_class + 2 * colour].append(int(label))

    print("Part 3:", sum(max(groups, key=len)))


if __name__ == "__main__":
    part1()
    part2()
    part3()
