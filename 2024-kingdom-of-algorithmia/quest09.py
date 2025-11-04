"""
The Kingdom of Algorithmia [2024]
Quest 9: Sparkling Bugs
https://everybody.codes/event/2024/quests/9
"""
from pathlib import Path

def read_sparkballs_data(filepath: str) -> list[int]:
    """Read and parse the list of brightness values from a part's input file."""
    return [int(line) for line in Path(filepath).read_text().strip().splitlines()]


def part1(filepath: str = "../input/everybody_codes_e2024_q09_p1.txt") -> None:
    sparkballs = read_sparkballs_data(filepath)
    # Available dot stamps
    stamps = [10, 5, 3, 1]
    total = 0
    # greedy approach, always choose the biggest first
    for sparkball in sparkballs:
        brightness = 0
        beetles = 0
        while brightness != sparkball:
            for stamp in stamps:
                if brightness + stamp <= sparkball:
                    brightness += stamp
                    beetles += 1
                    break
        total += beetles

    print("Part 1:", total)


def part2(filepath: str = "../input/everybody_codes_e2024_q09_p2.txt") -> None:
    sparkballs = read_sparkballs_data(filepath)
    # Available dot stamps
    stamps = [30, 25, 24, 20, 16, 15, 10, 5, 3, 1]

    # Memoization dictionary
    dp = {}

    def find_min(total: int) -> int:
        if total == 0:
            return 0
        if total < 0:
            return float("inf")
        if total in dp:
            return dp[total]

        min_beetle_count = float("inf")
        for stamp in stamps:
            min_beetle_count = min(min_beetle_count, 1 + find_min(total - stamp))

        dp[total] = min_beetle_count
        return min_beetle_count

    total = sum(find_min(sb) for sb in sparkballs)

    print("Part 2:", total)


def part3(filepath: str = "../input/everybody_codes_e2024_q09_p3.txt") -> None:
    sparkballs = read_sparkballs_data(filepath)
    # Available dot stamps
    stamps = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101]
    
    # iterative dp approach, precompute all possible sparkballs
    total = 0
    max_sparkball = max(sparkballs)
    dp = [float('inf')] * (max_sparkball + 1)
    dp[0] = 0
    for x in range(1, max_sparkball+1):
        for stamp in stamps:
            if x >= stamp:
                dp[x] = min(dp[x], dp[x - stamp] + 1)
    
    for sparkball in sparkballs:
        min_sparkball = float("inf")
        lower = sparkball // 2
        higher = sparkball // 2
        if sparkball % 2 == 1:
            higher += 1
        for split_spark in range(0, 51):
            min_sparkball = min(min_sparkball, dp[lower + split_spark] + dp[higher - split_spark])
        total += min_sparkball

    print("Part 3:", total)


if __name__ == "__main__":
    part1()
    part2()
    part3()
