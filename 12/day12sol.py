# Solution to day 12: Garden Groups
#### SUMMARY OF TASKS ####
# 1. Build a flowfill bfs algorithm


def parse_grid(input_file):
    """
    Return a matrix m x n representing a grid from a textfile
    """
    with open(input_file, "r") as file:
        grid = file.read()
        return [[r for r in row] for row in grid.strip().split('\n')]
    
direction_vector = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def sum_tuple(a, b):
    return (a[0] + b[0], a[1] + b[1])

def compute_perimeter(grid):
    perimeter = 0
    for coord in grid:
        for dir in direction_vector:
            new_coord = sum_tuple(coord, dir)
            if not new_coord in grid:
                perimeter += 1
    return perimeter

def compute_area(grid):
    return len(grid)

def flood_fill_search(grid):
    visited = set()
    all_regions = []
    rows, cols = len(grid), len(grid[0])

    def flood_fill_dfs(row, col, letter, region):
        # Check out of bounds:
        if not (0 <= row < rows and 0 <= col < cols):
            return
        
        # Check if the same letter
        if grid[row][col] != letter:
            return
        
        # Check if it has been visited
        if (row, col) in visited:
            return
        
        # It passes all the checks; not visited and connected
        # Mark coordinates as visited and add to region
        coord = (row, col)
        visited.add(coord)
        region.append(coord)

        # Recurse through each direction
        flood_fill_dfs(row + 1, col, letter, region) # right
        flood_fill_dfs(row - 1, col, letter, region) # left
        flood_fill_dfs(row, col + 1, letter, region) # down
        flood_fill_dfs(row, col - 1, letter, region) # up

        return region

    for i in range(rows):
        for j in range(cols):
            if (i, j) not in visited:
                letter = grid[i][j]
                region = flood_fill_dfs(i, j, letter, [])
                all_regions.append(region)

    return all_regions

def solve(input_file):
    """
    Produce the solution to the day 12 problem - Garden Groups
    Return the price for all the fences
    """
    price = 0

    grid = parse_grid(input_file)
    regions = flood_fill_search(grid)

    for region in regions:
        #print(region)
        price += compute_perimeter(region) * compute_area(region)
        #print(price)
    return price


def compute_sides(grid):
    num_sides = 0
    visited_sides = set()

    for cell in grid:
        for dir_code, movement in enumerate(direction_vector):
            neighbor = sum_tuple(cell, movement)

            if neighbor not in grid:
                edge = (cell, dir_code)

                if edge not in visited_sides:
                    print(f"Starting new side from edge {edge}")
                    flood_fill_edges(edge, grid, visited_sides)
                    num_sides += 1
    return num_sides


def flood_fill_edges(start_edge, grid, visited):
    if start_edge in visited:
        return
    
    print(f"  Visiting edge: {start_edge}")

    cell, dir_code = start_edge
    # Mark this edge as visited
    visited.add(start_edge)
    
    # Find adjacent edges
    adj_edges = find_adjacent_edges(cell, dir_code)
    
    # iterate through adjacent edges
    for adj_edge in adj_edges:
        adj_cell, adj_dir_code = adj_edge

        # Check if this adjacent edges exists
        adj_neighbor = sum_tuple(adj_cell, direction_vector[adj_dir_code])
        edge_exists = (adj_cell in grid) and (adj_neighbor not in grid)
        
        # If this edge exists, check if they are visited
        if edge_exists and adj_edge not in visited:
            flood_fill_edges(adj_edge, grid, visited)

def find_adjacent_edges(cell, dir_code):
    # (0, 1) and (0, -1) moves right and left respectively
    # (1, 0) and (-1, 0) moves down and up respectively
    # i.e. direction_vector[i]: i < 2 means edge has to be vertical
    # i >= 2 means edge is horizonal
    if dir_code // 2 == 0: # vertical edge
        return [(sum_tuple(cell, (1, 0)), dir_code), 
                (sum_tuple(cell, (-1, 0)), dir_code)]
    elif dir_code // 2 == 1: # horizontal edge
        return [(sum_tuple(cell, (0, 1)), dir_code),
                (sum_tuple(cell, (0, -1)), dir_code)]
    return 0

def solve_part2(input_file):
    """
    Produce the solution to the day 12 problem - Garden Groups
    Return the price for all the fences
    """
    price = 0

    grid = parse_grid(input_file)
    regions = flood_fill_search(grid)

    for region in regions:
        print(region)
        num_sides, area = compute_sides(region), compute_area(region)
        print(num_sides, area)
        price += num_sides * area
    return price

if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    # input = 'smalltest.txt'
    print(solve(input))
    print(solve_part2(input))