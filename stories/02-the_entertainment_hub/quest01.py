"""
The Entertainment Hub [ No. 2 ]
Quest 1: Nail Down Your Luck
https://everybody.codes/story/2/quests/1
"""
from functools import cache
from math import inf
from pathlib import Path
from typing import Callable, List, Tuple


def load_board_instructions(filepath: str) -> Tuple[Tuple[List[str]], List[str]]:

    text = Path(filepath).read_text().strip()
    board_fragment, instructions_fragment = text.split("\n\n")
 
    board = tuple(board_fragment.splitlines())
    instructions_list = instructions_fragment.splitlines()
    
    return board, instructions_list


@cache
def get_coins_won(instructions: str, slot: int, board: tuple[str]) -> int:

    num_rows, num_cols = len(board), len(board[0])
    # Token start position
    row, col = 0, 2 * (slot - 1)

    for move in instructions:
        # Token falls vertically unless it hits a nail
        while row < num_rows and board[row][col] != '*':
            row += 1
        # Has token reached the bottom?
        if row == num_rows:
            break
        # Token hits a nail and bounces Right or Left
        col += (move == 'R') - (move == 'L')
        # Token bounces off of walls
        if col == num_cols:
            col = num_cols - 2
        if col == -1:
            col = 1

    # Convert the column index back into a slot number
    final_slot = col // 2 + 1
    
    # Coins Won = (final slot number * 2) - toss slot number
    coins_won = max(2 * final_slot - slot, 0)

    return coins_won


def part1(filepath: str = "../../input/everybody_codes_e2_q01_p1.txt"):

    board, instructions_list = load_board_instructions(filepath)
        
    total = sum(get_coins_won(instructions, token_slot, board) 
                for token_slot, instructions in enumerate(instructions_list, 1))

    print("Part 1:", total)


def part2(filepath: str = "../../input/everybody_codes_e2_q01_p2.txt"):

    board, instructions_list = load_board_instructions(filepath)

    max_slot = len(board[0]) // 2 + 1
    
    total = sum(
        max(get_coins_won(instructions, token_slot, board)
            for token_slot in range(1, max_slot + 1))
        for instructions in instructions_list
    )

    print("Part 2:", total)


def part3(filepath: str = "../../input/everybody_codes_e2_q01_p3.txt"):

    board, instructions_list = load_board_instructions(filepath)

    max_slot = len(board[0]) // 2 + 1

    @cache
    def get_limit(i: int, used_slot: int, func: Callable[[int, int], int]) -> int:
        # Check if all instructions have been used - termination point reached
        if i == len(instructions_list):
            return 0
        # Initialize the limit baseline
        current_limit = 0 if func == max else inf
        # Iterate over each slot
        for token_slot in range(1, max_slot + 1):
            mask = 1 << token_slot
            # Has slot been used?
            if used_slot & mask == 0:
                # Compute the coins won for this slot and instruction combination
                # Compare against current limit and result for next instructions list
                current_limit = func(
                    current_limit,
                    get_coins_won(instructions_list[i], token_slot, board)
                    + get_limit(i + 1, used_slot | mask, func),
                )

        return current_limit

    best_total = get_limit(0, 0, max)
    worst_total = get_limit(0, 0, min)

    print(f"Part 3: {best_total} {worst_total}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
