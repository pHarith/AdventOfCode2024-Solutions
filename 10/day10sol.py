# Solution to day 10: Hoof It
#### SUMMARY OF TASKS ####
# 1. 


movement = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def parse_topo_map(input_file):
    """
    Given an input file, convert it into a matrix of m x n size.
    """
    with open(input_file, "r") as file:
        map_str = file.read()
        map = [[int(char) if char != '.' else char for char in row] for row in map_str.strip().split('\n')]
    return map
        

def find_trailheads(map):
    """
    Given a map of a hiking trial, return coordinates of 0's.
    """
    trailheads = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 0:
                trailheads.append((i, j))
    return trailheads

def find_unique_9s(trailhead, map):
    i, j = trailhead
    row, col = len(map), len(map[0])
    reachable_9s = set()

    # Implement a dfs here
    def dfs_solve(head, i, j, map, reachable_end_nodes):
        for move in movement:
            new_i, new_j = i + move[0], j + move[1]
            if 0 <= new_i < row and 0 <= new_j < col:
                new_head = map[new_i][new_j]

                if new_head != '.':
                    if new_head - head == 1:
                        if new_head == 9:
                            reachable_end_nodes.add((new_i, new_j))
                        else:
                            dfs_solve(new_head, new_i, new_j, map, reachable_end_nodes)
    
    
    dfs_solve(0, i, j, map, reachable_9s)
    
    return len(reachable_9s)
    
def find_ratings(trailhead, map):
    i, j = trailhead
    row, col = len(map), len(map[0])
    viable_paths = []

    # Implement a dfs here
    def dfs_solve(head, i, j, map, paths):
        for move in movement:
            new_i, new_j = i + move[0], j + move[1]
            if 0 <= new_i < row and 0 <= new_j < col:
                new_head = map[new_i][new_j]

                if new_head != '.':
                    if new_head - head == 1:
                        if new_head == 9:
                            paths.append((new_i, new_j))
                        else:
                            dfs_solve(new_head, new_i, new_j, map, paths)
    
    
    dfs_solve(0, i, j, map, viable_paths)

    return len(viable_paths)


def solve(input_file):
    """
    Produce the solution to the day 10 problem - Hoof It
    """
    total_score = 0
    map = parse_topo_map(input_file)
    trailheads = find_trailheads(map)
    for trailhead in trailheads:
        total_score += find_unique_9s(trailhead, map)
    return total_score

def solve_part2(input_file):
    """
    Produce the solution to the day 10 problem - Hoof It
    """
    total_ratings = 0
    map = parse_topo_map(input_file)
    trailheads = find_trailheads(map)
    for trailhead in trailheads:
        total_ratings += find_ratings(trailhead, map)
    return total_ratings


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))
    print(solve_part2(input))

# The answer is 