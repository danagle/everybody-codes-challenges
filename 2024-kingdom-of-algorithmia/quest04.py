"""
The Kingdom of Algorithmia [2024]
Quest 4: Royal Smith's Puzzle
https://everybody.codes/event/2024/quests/4
"""
from pathlib import Path

for part_num in range(1, 4):
    filepath = f"../input/everybody_codes_e2024_q04_p{part_num}.txt"
    nails = [int(l.strip()) for l in Path(filepath).read_text().strip().splitlines()]

    if part_num < 3:
        target = min(nails)
    else:
        nails.sort()
        target = nails[len(nails)//2]
    
    total = sum([abs(nail - target) for nail in nails])

    print(f"Part {part_num}:", total)
