"""
The Kingdom of Algorithmia [2024]
Quest 1: The Battle for the Farmlands
https://everybody.codes/event/2024/quests/1
"""
from pathlib import Path

x_potions = {
    3:6,
    2:2,
    1:0,
    0:0
}

monster_potions = {
    'A':0,
    'B':1,
    'C':3,
    'D':5,
    'x':0
}

for part_num in range(1, 4):
    filepath = f"../input/everybody_codes_e2024_q01_p{part_num}.txt"
    text = Path(filepath).read_text().strip()
    # Split the text into groups of length equal to the part number
    attacks = [text[i:i+part_num] for i in range(0, len(text), part_num)]
    total = 0

    for attack in attacks:
        # 1. Sum the potion values of the monsters in the attack
        attack_value = sum(map(monster_potions.get, attack))
        # 2. Add bonus potions based on how many non-'x' attacks are in this group
        bonus = x_potions[part_num - attack.count('x')]
        # Add to the running total
        total += attack_value + bonus

    print(f"Part {part_num}:", total)
