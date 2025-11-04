"""
The Kingdom of Algorithmia [2024]
Quest 11: Biological Warfare
https://everybody.codes/event/2024/quests/11
"""
from collections import Counter
from pathlib import Path

def load_conversion_rules(filepath: str) -> dict[str, list[str]]:
    """
    Load termite conversion rules from a text file.

    Each line in the file has the format:
        Parent:Child1,Child2,...

    Example file:
        A:B,C
        B:D
        C:D,E

    Returns:
        A dictionary mapping each parent category (str)
        to a list of its child categories (list[str]).
    """
    lines = Path(filepath).read_text().strip().splitlines()
    rules = {}
    for line in lines:
        category, *children = line.replace(":", ",").split(",")
        rules[category] = children
    return rules


def next_generation_counter(children: list[str], count: int) -> Counter:
    """
    Generate a Counter of the next generation based on offspring rules.

    Args:
        children: List of termite categories produced by a parent.
        count: Number of parent termites of this type.

    Returns:
        A Counter mapping each child category to its resulting termite count.
        (Each child gets 'count' added to its total.)
    """
    next_generation = Counter()
    for termite_category in children:
        next_generation[termite_category] += count
    return next_generation


def track_population(category: str, num_days: int, rules: dict[str, list[str]]) -> int:
    """
    Simulate termite population growth over a given number of days.

    Starting from one termite of the given category, each day:
      - Every termite converts into one or more new categories 
        based on the provided conversion rules.

    Args:
        category: The starting termite category.
        num_days: Number of days (generations) to simulate.
        rules: Conversion mapping from parent to child categories.

    Returns:
        The total population count after 'num_days' generations.
    """
    # Start with one termite of the given category
    counts = Counter([category])

    # Simulate day-by-day population growth
    for _ in range(num_days):
        new_counts = Counter()
        for termite, count in counts.items():
            new_counts += next_generation_counter(rules[termite], count)
        counts = new_counts  # Move to next generation

    # Return the total termite count after all generations
    return sum(counts.values())


def part1(filepath: str = "../input/everybody_codes_e2024_q11_p1.txt") -> None:
    """Starting with a single category 'A' termite compute the population count on the 4th day."""
    rules = load_conversion_rules(filepath)

    result = track_population("A", 4, rules)

    print("Part 1:", result)


def part2(filepath: str = "../input/everybody_codes_e2024_q11_p2.txt") -> None:
    """Starting with a single category 'Z' termite compute the population count on the 10th day."""
    rules = load_conversion_rules(filepath)

    result = track_population("Z", 10, rules)

    print("Part 2:", result)


def part3(filepath: str = "../input/everybody_codes_e2024_q11_p3.txt") -> None:
    """Calculate the population difference on the 20th day."""
    rules = load_conversion_rules(filepath)
    largest, smallest = 0, float("inf")

    for initial_termite in rules:
        count = track_population(initial_termite, 20, rules)
        if count < smallest:
            smallest = count
        if largest < count:
            largest = count

    print("Part 3:", largest-smallest)


if __name__ == "__main__":
    part1()
    part2()
    part3()
