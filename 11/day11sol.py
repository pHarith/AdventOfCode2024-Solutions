# Solution to day 11 - Plutonian Pebbles 
#### SUMMARY OF TASKS ####
# 1. 

def parse_stones(input_file):
    with open(input_file, "r") as file:
        return file.read().split()
        
def blink(stones, num_times, i=0):
    if i == num_times:
        return stones
    
    new_lst = []
    for stone in stones:
        if stone == '0':
            new_lst.append('1')
        elif len(stone) % 2 == 0:
            mid = len(stone) // 2
            new_lst.extend([str(int(stone[:mid])), str(int(stone[mid:]))])
        else:
            new_lst.append(str(int(stone) * 2024))
    
    return blink(new_lst, num_times, i + 1)

def blink_map(stone_map, num_times, i=0):
    print(stone_map, i)

    if i == num_times:
        return stone_map
    
    new_map = {}
    for stone, stone_count in stone_map.items():
        if len(stone) % 2 == 0:
            mid = len(stone) // 2
            stone_1, stone_2 = str(int(stone[:mid])), str(int(stone[mid:]))
            add_to_map(stone_1, new_map, stone_count)
            add_to_map(stone_2, new_map, stone_count)
        else:
            new_stone = str(int(stone) * 2024) if stone != '0' else '1'
            add_to_map(new_stone, new_map, stone_count)
    
    return blink_map(new_map, num_times, i + 1)

def add_to_map(stone, map, old_count):
    if stone in map:
        map[stone] += old_count
    else:
        map[stone] = old_count
            

def solve(input_file, num_blinks):
    """
    Produce the solution to the day 11 problem - Plutonian Pebbles
    """
    stone_list = parse_stones(input_file)

    stone_map = {stone: 1 for stone in stone_list}
    return len(blink(stone_list, num_blinks))


def solve_part2(input_file, num_blinks):
    """
    Produce the solution to part 2 of the day 11 problem - Plutonian Pebbles
    """
    stone_list = parse_stones(input_file)

    stone_map = {stone: 1 for stone in stone_list}

    return sum_values(blink_map(stone_map, num_blinks))

def sum_values(map):
    sum = 0
    for _, v in map.items():
        sum += v
    return sum


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input, num_blinks=25))

    # Part 2: Blink 75 times
    print(solve_part2(input, num_blinks=75))

# The answer is 