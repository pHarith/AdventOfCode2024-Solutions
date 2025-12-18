# Solution to day 16: Reindeer Maze
#### SUMMARY OF TASKS ####
# 1. Read input file into a map, as usual
# 2. Use Dijakstra's algorithm to construct a path to the end

# FOR PART 2:
# 1. Add a path length variable to keep track of the best cost path

# Import heapq to assist with path finding algorithm
from heapq import heappop, heappush

# NOTE: heapq turns list into a min-heap so it gives easy access to path with lowest score

# Constances for mapping purposes
START = 'S'
END = 'E'
WALL = '#'

UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'

# Dictionaries to help us define movement
movement_vectors = {UP: (0, -1), RIGHT: (1, 0), DOWN: (0, 1), LEFT: (-1, 0)} 

# Dictionary for clockwise, counterclockwise rotation
clockwise_turn = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
counterclockwise_turn = {UP: LEFT, RIGHT: UP, DOWN: RIGHT, LEFT: DOWN}

# Dictionary for reversed movement (Part 2)
reverse = {UP: DOWN, RIGHT: LEFT, DOWN: UP, LEFT: RIGHT}

def sum_tuple(a, b):
    return (a[0] + b[0], a[1] + b[1])

def parse_board(input_file):
    """
    Given an input file, read the board into a nested list.
    """
    board = []
    movement_instr = []
    with open(input_file, "r") as file:
        board_str = file.read()
        # Split the board into a nested list of strings
        board = [list(row) for row in board_str.split('\n')]
    return board

def find_start_end(board):
    start = None
    end = None
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[j][i] == START:
                start = (i, j)
            
            if board[j][i] == END:
                end = (i, j)
    return start, end

def find_optimal_maze_path(start_pos, end_pos, board):
    """
    Using Djakstra's algorithm, return the score of the most optimal path to exit the maze. Rules are:
    + 1 pt for each step
    + 1000 pts for any clockwise or anti-clockwise turn made
    """
    num_rows, num_cols = len(board), len(board[0])

    # Inner help function(s)

    def is_valid_move(pos):
        """
        Returns if move made by the user is valid.
        
        :param pos: (x, y) - where x is the x coordinate of the object on the board
        and y is the y-coordinate of the object on the board.
        """
        x, y = pos
        if 0 <= x < num_cols and 0 <= y < num_rows:
            return board[y][x] != WALL
        return False

    # Function body here
    path_queue = [(0, start_pos, LEFT)]
    visited = set()

    while path_queue:
        cost, curr_pos, move = heappop(path_queue)

        if curr_pos == end_pos:
            return cost
        
        if (curr_pos, move) in visited:
            continue

        visited.add((curr_pos, move))

        # Move forawrd based on the direction of the move
        new_pos = sum_tuple(curr_pos, movement_vectors[move])

        if is_valid_move(new_pos):
            heappush(path_queue, (cost + 1, new_pos, move))
        
        # Try turning both clockwise and counterclockwise and add this into the path queue
        heappush(path_queue, (cost + 1000, curr_pos, clockwise_turn[move]))
        heappush(path_queue, (cost + 1000, curr_pos, counterclockwise_turn[move]))

    return -1

def print_board(board):
    for row in board:
        for item in row:
            print(item, end="")
        print()

def solve(input_file):
    """
    Produce the solution to the day 16 problem - Reindeer Maze
    """
    score = 0
    board = parse_board(input_file)
    start_pos, end_pos = find_start_end(board)
    print_board(board)
    score = find_optimal_maze_path(start_pos, end_pos, board)
    num_tiles = find_all_best_paths_tiles(start_pos, end_pos, board, score)
    print_board(board)
    return score, num_tiles

# FOR PART 2:
def find_all_best_paths_tiles(start_pos, end_pos, board, min_cost):
    """
    Using Dijkstra's algorithm, return the total number of tiles that are on one of the best paths.
    Use two-way Dijkstra's algorithm - forward to compute cost from S to every tile and backward to compute cost from E to every other tile. 
    A tile is considered as on the best path if:
    cost from S to tile + cost from E to tile = <min_cost>
    """
    num_rows, num_cols = len(board), len(board[0])

    # Inner help function(s)

    def is_valid_move(pos):
        """
        Returns if move made by the user is valid.
        
        :param pos: (x, y) - where x is the x coordinate of the object on the board
        and y is the y-coordinate of the object on the board.
        """
        x, y = pos
        if 0 <= x < num_cols and 0 <= y < num_rows:
            return board[y][x] != WALL
        return False
    
    print(start_pos, end_pos)
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    print(board[start_y][start_x], board[end_y][end_x])

    # FORWARD DIJKSTRA GOES HERE
    forward_cost = {}
    forward_queue = [(0, start_pos, LEFT)]
    while forward_queue:
        cost, curr_pos, move = heappop(forward_queue)

        curr_state = (curr_pos, move)
        
        if curr_state in forward_cost:
            continue

        forward_cost[curr_state] = cost

        # Move forawrd based on the direction of the move
        new_pos = sum_tuple(curr_pos, movement_vectors[move])

        if is_valid_move(new_pos):
            heappush(forward_queue, (cost + 1, new_pos, move))
        
        # Try turning both clockwise and counterclockwise and add this into the path queue
        heappush(forward_queue, (cost + 1000, curr_pos, clockwise_turn[move]))
        heappush(forward_queue, (cost + 1000, curr_pos, counterclockwise_turn[move]))


    # BACKWARD DIJKSTRA GOES HERE
    backward_cost = {}
    backward_queue = []

    # Build backward queue 
    for dir in [UP, DOWN, LEFT, RIGHT]:
        if (end_pos, dir) in forward_cost and forward_cost[(end_pos, dir)] == min_cost:
            heappush(backward_queue, (0, end_pos, dir))

    # Backwards Dijkstra loop:
    while backward_queue:
        cost, curr_pos, move = heappop(backward_queue)

        curr_state = (curr_pos, move)
        
        if curr_state in backward_cost:
            continue

        backward_cost[curr_state] = cost

        # Move "backwards" by reversing the direction of the move
        new_move = reverse[move]
        new_pos = sum_tuple(curr_pos, movement_vectors[new_move])

        if is_valid_move(new_pos):
            heappush(backward_queue, (cost + 1, new_pos, move))
        
        # Try turning both clockwise and counterclockwise and add this into the path queue
        heappush(backward_queue, (cost + 1000, curr_pos, clockwise_turn[move]))
        heappush(backward_queue, (cost + 1000, curr_pos, counterclockwise_turn[move]))
    
    # Prune all the tiles that lies on the optimal path(s)
    optimal_tiles = set()

    for state in forward_cost:
        if state in backward_cost and forward_cost[state] + backward_cost[state] == min_cost:
            optimal_tiles.add(state[0])

    highlight_best_path_tiles(board, optimal_tiles)

    return len(optimal_tiles)
    

def highlight_best_path_tiles(board, best_tiles):
    for x, y in best_tiles:
        board[y][x] = '0'
    return


if __name__ == "__main__":
    # input = 'input.txt'
    input = 'test.txt'
    print(solve(input)) # This should solve both part 1 and part 2