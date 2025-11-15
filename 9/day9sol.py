# Solution to day 9: Disk Fragmenter

def parse_disk_map(input_file):
    disk_map = []
    with open(input_file, "r") as file:
        disk_str = file.read()
    for index, digit in enumerate(disk_str):
        length = int(digit)
        if index % 2 == 0: # even index, is a file
            disk_map.extend([index // 2] * length)
        else: # odd index, free space
            disk_map.extend(['.'] * length)
    return disk_map

def sort_disk_map(disk_map):
    j = len(disk_map) - 1
    for i in range(len(disk_map)):
        if i >= j:
            break

        if disk_map[i] == '.':
            while j > i and disk_map[j] == '.':
                j -= 1
            if j > i:
                disk_map[i], disk_map[j] = disk_map[j], disk_map[i]
    return j
        

def sort_disk_map_block(disk_map):
    j = len(disk_map) - 1
    while j >= 0:
        if disk_map[j] != '.':
            file_id = disk_map[j]

            file_size = 1
            while j - file_size >= 0 and disk_map[j - file_size] == file_id:
                file_size += 1

            free_space_start = find_leftmost_free_space(disk_map, file_size, j - file_size + 1)

            if free_space_start is not None:
                move_files(disk_map, free_space_start, j, file_size)
            j -= file_size
        else:
            j -= 1


def move_files(disk_map, free_index, id_index, size):
    for i in range(size):
        disk_map[free_index + i], disk_map[id_index - i] = disk_map[id_index - i], disk_map[free_index + i]
    

def find_leftmost_free_space(disk_map, size, end):
    for i in range(end):
        if disk_map[i] == '.':
            span = 1
            while i + span < end and disk_map[i + span] == '.':
                span += 1
            
            if span >= size:
                return i
    return None
        
def checksum(disk_map, end):
    checksum = 0
    for i in range(end):
        if disk_map[i] != '.':
            checksum += disk_map[i] * i
    return checksum

def solve(input_file):
    """
    Produce the solution to the day 9 problem - Disk Fragmenter
    """
    disk_map = parse_disk_map(input_file)
    end = sort_disk_map(disk_map)
    return checksum(disk_map, end)

def solve_part2(input_file):
    """
    Produce the solution to the day 9 problem - Disk Fragmenter
    """
    disk_map = parse_disk_map(input_file)
    #print(disk_map)
    sort_disk_map_block(disk_map)
    #print(disk_map)
    return checksum(disk_map, len(disk_map))


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))
    print(solve_part2(input))