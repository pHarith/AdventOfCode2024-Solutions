direction_vector = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def sum_tuple(a, b):
    return (a[0] + b[0], a[1] + b[1])

def compute_sides(grid):
    num_sides = 0
    visited_sides = set()

    for cell in grid:
        for dir_code, movement in enumerate(direction_vector):
            neighbor = sum_tuple(cell, movement)

            if neighbor not in grid:
                edge = (cell, dir_code)

                if edge not in visited_sides:
                    flood_fill_edges(edge, grid, visited_sides)
                    num_sides += 1
    return num_sides


def flood_fill_edges(start_edge, grid, visited):
    cell, dir_code = start_edge
    # Mark this edge as visited
    visited.add(start_edge)
    
    # Find adjacent edges
    adj_edges = find_adjacent_edges(cell, dir_code)
    
    # iterate through adjacent edges
    for adj_edge in adj_edges:
        adj_cell, adj_dir_code = adj_edge

        # Check if this adjacent edges exists
        adj_neighbor = adj_cell + direction_vector[adj_dir_code]
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

if __name__ == "__main__":
    test_grid = [['A', 'A'], ['A']]
    test_coord = [(0, 0), (1, 0), (0, 1)]
    for test in test_grid:
        print(test)
    print(compute_sides(test_coord))