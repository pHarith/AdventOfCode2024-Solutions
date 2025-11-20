# Solution to day 14: Restroom Redoubt
# Summary of Tasks:
# 1. Construct an empty board-space to simulate robot movements
# 2. Read robots' position and their speed settings, then add them to the board
# 3. Loop 100 times and find the robot position after 100 seconds
# 4. Count the number of robots in 4 quadrants (divide the board into 4 quadrants)
# 5. Multiply those numbers to return a safety rating

# Define constants of the space/board
NUM_ROWS, NUM_COLS = 103, 101

TEST_ROWS, TEST_COLS = 7, 11

# Wait time for simulating robot movements
WAIT_TIME = 100

# for checking if it is a tree
MIN_CONSECUTIVE_ROWS = 7
MIN_CONSECUTIVE_ONES = 7
# i.e. we want to check for 7 consecutive rows with at least 7 consecutives ones
# NOTE: Why 7? Lucky number 7...

import copy

def robot_move(init, move, rows, cols, i):
    """
    Move a robot from <init> by <move> for <i> seconds.
    Movement restricted to be within <rows> and <cols>.
    """
    return ((init[0] + move[0] * i) % cols, (init[1] + move[1] * i) % rows) 

def create_board(rows, cols):
    return [[0] * cols for _ in range(rows)]

def parse_robots_info(input_file):
    robot_info = []
    with open(input_file, "r") as file:
        info_str = file.read()
        for info in info_str.split('\n'):
            info_tuple = tuple(tuple(int(i) for i in val[val.find('=')+1:].split(',')) for val in info.split(' '))
            robot_info.append(info_tuple)
    return robot_info

def simulate_movement(board, robots_info, secs=100):
    test_board = copy.deepcopy(board)
    rows, cols = len(board), len(board[0])
    for init_pos, velocity in robots_info:
        new_pos = robot_move(init_pos, velocity, rows, cols, secs)
        # NOTE: rows and cols are reversed of x and y coordinates
        y_coord, x_coord = new_pos
        test_board[x_coord][y_coord] += 1    
    return test_board

def divide_board(board):
    """
    Divide a <board> of m x n size into 
    """
    mid_row = len(board) // 2
    mid_col = len(board[0]) // 2

    top_left = [row[:mid_col] for row in board[:mid_row]]
    top_right = [row[mid_col + 1:] for row in board[:mid_row]]
    bottom_left = [row[:mid_col] for row in board[mid_row+1:]]
    bottom_right = [row[mid_col + 1:] for row in board[mid_row:]]

    return [top_left, top_right, bottom_left, bottom_right]

def compute_safety_rating(quadrants):
    safety_rating = 1
    for quad in quadrants:
        quad_safety_rating = sum(sum(row) for row in quad)
        safety_rating *= quad_safety_rating
    return safety_rating

def solve(input_file, board_size):
    """
    Produce the solution to the day 14 problem - Restroom Redoubt
    """
    num_rows, num_cols = board_size
    board = create_board(num_rows, num_cols)

    robot_info = parse_robots_info(input_file)
    new_board = simulate_movement(board, robot_info)

    quadrants = divide_board(new_board)
    return compute_safety_rating(quadrants)

# SOLUTION TO SOLVING PART 2
# NOTE: To form a christmas tree, it should have a noticable pattern
# Such a pattern is checking if there is a series of rows with consecutive 1s

def compute_easter_egg_time(board, robot_info, max_time=10000):
    for i in range(1, max_time):
        new_board = simulate_movement(board, robot_info, i)
        if check_christmas_tree(new_board):
            print_board_to_file(new_board)
            return i
    # Printing tree to file for sanity checking
    # print_board_to_file(new_board)
    return 0
    
def check_christmas_tree(board):
    consecutive_rows = 0
    for row in board:
        if check_consecutive_ones(row):
            consecutive_rows += 1

            # Check if there are 7 or more consecutive rows
            if consecutive_rows >= MIN_CONSECUTIVE_ROWS:
                return True
        else:
            consecutive_rows = 0
    return False


def check_consecutive_ones(row):
    max_consecutive = curr_consecutive = 0
    for item in row:
        if item == 1:
            curr_consecutive += 1
            max_consecutive = max(max_consecutive, curr_consecutive)
        else:
            # Reset our consecutive ones
            curr_consecutive = 0
    return max_consecutive >= MIN_CONSECUTIVE_ONES


def solve_part2(input_file, board_size):
    """
    Produce the solution to part 2 of the day 14 problem - Restroom Redoubt
    """
    num_rows, num_cols = board_size
    board = create_board(num_rows, num_cols)
    robot_info = parse_robots_info(input_file)
    return compute_easter_egg_time(board, robot_info)

def print_board(board):
    for row in board:
        for item in row:
            print(item, end="")
        print()

def print_board_to_file(board):
    with open("tree.txt", "w+") as tree_file:
        for row in board:
            for pos in row:
                tree_file.write(str(pos))
            tree_file.write("\n")
        

if __name__ == "__main__":
    input = 'input.txt'
    test_input = 'test.txt'
    test_board = TEST_ROWS, TEST_COLS
    input_board = NUM_ROWS, NUM_COLS

    print(solve(input, board_size=input_board))
    print(solve_part2(input, board_size=input_board))