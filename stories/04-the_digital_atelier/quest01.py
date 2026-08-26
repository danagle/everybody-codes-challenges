"""
The Digital Atelier [ No. 4 ]
Quest 1: The Recamán Drapery
https://everybody.codes/story/4/quests/1
"""
def read_input_file(file: str) -> list[list[int]]:
    with open(file, 'r') as f:
        return [[int(n) for n in line.split(',')] for line in f.read().splitlines() if line]


def part1(filepath: str = "everybody_codes_e4_q01_p1.txt"):
    ornaments = read_input_file(filepath)
    total = 0
    for sequence in ornaments:
        current = 0
        visited = set()
        for length in sequence:
            visited.add(current)
            step_back = current - length
            if step_back > 0 and step_back not in visited:
                current = step_back
            else:
                current = current + length
        total += current
    print("Part 1:", total)


def part2(filepath: str = "everybody_codes_e4_q01_p2.txt"):
    ornaments = read_input_file(filepath)
    total = 0
    for sequence in ornaments:
        current = 0
        destination_map = {}
        # Path Compression to find the next available unseen destination in O(1)
        def get_next_point(pointer):
            path_taken = []
            while pointer in destination_map:
                path_taken.append(pointer)
                pointer = destination_map[pointer]
            for node in path_taken:
                destination_map[node] = pointer
            return pointer

        for length in sequence:
            destination_map[current] = current + 1
            next_point = current - length
            if length <= current and next_point not in destination_map:
                current = next_point
            else:
                current += length
                current = get_next_point(current)

        total += current
    print("Part 2:", total)


def part3(filepath: str = "everybody_codes_e4_q01_p3.txt"):
    ornaments = read_input_file(filepath)
    total = 0
    for sequence in ornaments:
        current = 0
        destination_map = {}
        # 0 for Under, 1 for Over
        arcs = [[], []] 
        side = 0
        
        def get_next_point(pointer):
            path_taken = []
            while pointer in destination_map:
                path_taken.append(pointer)
                pointer = destination_map[pointer]
            for node in path_taken:
                destination_map[node] = pointer
            return pointer

        for length in sequence:
            destination_map[current] = current + 1
            next_point = current - length
            
            can_jump_back = False
            if length <= current and next_point not in destination_map:
                can_jump_back = True
                
                # Check cross condition for jumping back
                for start, end in arcs[side]:
                    # jumps_in
                    if not (start <= current <= end) and (start < next_point < end):
                        can_jump_back = False
                        break
                    # jumps_out
                    if (start < current < end) and not (start <= next_point <= end):
                        can_jump_back = False
                        break
                        
            if can_jump_back:
                next_point = current - length
            else:
                next_point = current + length
                
                # Calculate max_allowed threshold and pre-filter outside arcs
                max_allowed = float('inf')
                outside_arcs = []
                for start, end in arcs[side]:
                    if start < current < end:
                        if end < max_allowed:
                            max_allowed = end
                    else:
                        outside_arcs.append((start, end))
                
                skip_outer = False
                while True:
                    # 1. Bounds check
                    if next_point > max_allowed:
                        skip_outer = True
                        break
                        
                    # 2. Seen fast-forward
                    if next_point in destination_map:
                        next_point = get_next_point(next_point)
                        continue
                        
                    if next_point > max_allowed:
                        skip_outer = True
                        break
                        
                    # 3. Arcs fast-forward
                    jumped = False
                    for start, end in outside_arcs:
                        if start < next_point < end:
                            next_point = end
                            jumped = True
                            break
                            
                    if jumped:
                        continue
                        
                    break # Found valid, non-overlapping next_val
                    
                if skip_outer:
                    continue
            # Add Arc
            a, b = current, next_point
            if a > b:
                a, b = b, a
            arcs[side].append((a, b))
            side ^= 1
            current = next_point

        total += current
    print("Part 3:", total)


if __name__ == "__main__":
    part1()
    part2()
    part3()
