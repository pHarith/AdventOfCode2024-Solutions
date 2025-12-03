# Solution to day 16: Reindeer Maze
#### SUMMARY OF TASKS ####
# 1. Read input file into a map, as usual
# 2. 

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
                start = (j, i)
            
            if board[j][i] == END:
                end = (j, i)
    return start, end

def find_optimal_maze_path(start_pos, end_pos, board):
    """
    Using Djakstra's algorithm, return the score of the most optimal path to exit the maze. Rules are:
    + 1 pt for each step
    + 1000 pts for any clockwise or anti-clockwise turn made
    """
    num_rows, num_cols = len(board), len(board[0])

    # Inner help function
    def is_valid_move(pos):
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
    score = find_optimal_maze_path(start_pos, end_pos, board)
    print_board(board)
    return score


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))