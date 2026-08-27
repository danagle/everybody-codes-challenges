"""
The Digital Atelier [ No. 4 ]
Quest 2: Sir Sierpiński's Sparkballs
https://everybody.codes/story/4/quests/2
"""
class LaunchPlan:
    def __init__(self):
        self.start = (0, 0)
        self.a = (0, 0)
        self.b = (0, 0)
        self.c = (0, 0)
        self.moves: List[Tuple[int, int]] = []


def read_input_file(filepath: str) -> LaunchPlan:
    plan = LaunchPlan()

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            key, value = line.split("=", 1)
            if key == "MOVES":
                for m in value:
                    if m == "A": plan.moves.append(plan.a)
                    elif m == "B": plan.moves.append(plan.b)
                    elif m == "C": plan.moves.append(plan.c)
            else:
                x_str, y_str = value[1:-1].split(",")
                coord = (int(x_str), int(y_str))
                if key == "START": plan.start = coord
                elif key == "A": plan.a = coord
                elif key == "B": plan.b = coord
                elif key == "C": plan.c = coord

    return plan


def calculate_fireflies(illuminated: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    fireflies = set()
    for x, y in illuminated:
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if neighbor not in illuminated:
                fireflies.add(neighbor)
    return fireflies


def get_illuminated(plan: LaunchPlan) -> Set[Tuple[int, int]]:
    illuminated = {plan.start}
    pos = plan.start

    for dest in plan.moves:
        nx = (pos[0] + dest[0]) // 2
        ny = (pos[1] + dest[1]) // 2
        pos = (nx, ny)
        illuminated.add(pos)

    return illuminated


def get_illuminated_dfs(plan: LaunchPlan) -> Set[Tuple[int, int]]:
    illuminated = set()
    stack = [plan.start]
    destinations = (plan.a, plan.b, plan.c)
    
    while stack:
        pos = stack.pop()

        if pos in illuminated:
            continue

        illuminated.add(pos)

        for dest in destinations:
            nx = (pos[0] + dest[0]) // 2
            ny = (pos[1] + dest[1]) // 2
            if (nx, ny) not in illuminated:
                stack.append((nx, ny))

    return illuminated


def part1(filepath: str = "everybody_codes_e4_q02_p1.txt"):
    plan = read_input_file(filepath)
    illuminated = get_illuminated(plan)
    print("Part 1:", len(illuminated))


def part2(filepath: str = "everybody_codes_e4_q02_p2.txt"):
    plan = read_input_file(filepath)
    illuminated = get_illuminated(plan)
    fireflies = calculate_fireflies(illuminated)
    print("Part 2:", len(fireflies))


def part3(filepath: str = "everybody_codes_e4_q02_p3.txt"):
    plan = read_input_file(filepath)
    illuminated = get_illuminated_dfs(plan)
    fireflies = calculate_fireflies(illuminated)
    print("Part 3:", len(fireflies))


if __name__ == "__main__":
    part1()
    part2()
    part3()
