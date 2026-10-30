from collections import defaultdict
from pathlib import Path


def load_notes(filepath: str):
    return [
        [int(token.split("=")[1]) for token in line.split()]
        for line in Path(filepath).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def part1(filepath: str = "../input/everybody_codes_e2026_q04_p1.txt") -> None:
    total_times = defaultdict(int)

    for participant_id, _, _, time in load_notes(filepath):
        total_times[participant_id] += time

    checksum = sum(rank * total_time for rank, total_time in enumerate(sorted(total_times.values()), 1))
    print(f"Part 1: {checksum}")


def part2(filepath: str = "../input/everybody_codes_e2026_q04_p2.txt") -> None:
    ranking_data = defaultdict(lambda: [0, 0])

    for participant_id, _, _, time in load_notes(filepath):
        ranking_data[participant_id][0] += 1      # Count parts
        ranking_data[participant_id][1] += time   # Total time

    # Sorting: highest count, then lowest time
    sorted_ranking = sorted(ranking_data.values(), key=lambda x: (-x[0], x[1]))

    checksum = sum(rank * total_time for rank, (_, total_time) in enumerate(sorted_ranking, 1))
    print(f"Part 2: {checksum}")


def part3(filepath: str = "../input/everybody_codes_e2026_q04_p3.txt") -> None:
    records = load_notes(filepath)

    # Initialize scores list based on the number of unique participants
    num_participants = len({record[0] for record in records})
    total_scores = [0] * num_participants

    # Group records by (quest, part)
    grouped_by_qp = defaultdict(list)
    for participant_id, quest, part, time_taken in records:
        grouped_by_qp[(quest, part)].append((time_taken, participant_id))

    current_totals = [0] * num_participants

    # Process groups sequentially in sorted order of (quest, part)
    for (quest, part), items in sorted(grouped_by_qp.items()):
        if part == 1:
            current_totals = [0] * num_participants

        for time_taken, participant_id in items:
            current_totals[participant_id - 1] += time_taken

        # Allocate points based on sorted performance within the group
        pool_score = part * 50
        score_step = pool_score
        prev_total = -1

        group_rankings = sorted([(current_totals[participant_id - 1], participant_id) for _, participant_id in items])

        for total_val, participant_id in group_rankings:
            if total_val != prev_total:
                pool_score = score_step
                if pool_score < 0:
                    break
            total_scores[participant_id - 1] += pool_score
            score_step -= 1
            prev_total = total_val

    # Calculate final checksum with tie-breaking rank tracking
    checksum = 0
    rank = 1
    prev_score = -1
    next_rank = rank

    for score in sorted(total_scores, reverse=True):
        if score != prev_score:
            rank = next_rank
        prev_score = score
        checksum += rank * score
        next_rank += 1

    print(f"Part 3: {checksum}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
