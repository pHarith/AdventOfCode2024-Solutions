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

def sum_tuples_mod(a, b, rows, cols):
    return ((a[0] + b[0]) % cols, (a[1] + b[1]) % rows) 

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
    rows, cols = len(board), len(board[0])
    for init_pos, velocity in robots_info:
        for i in range(secs):
            new_pos = sum_tuples_mod(init_pos, velocity, rows, cols)
            init_pos = new_pos

        # NOTE: rows and cols are       
        y_coord, x_coord = new_pos
        board[x_coord][y_coord] += 1    
    return

def divide_board(board):
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
    #print_board(board)
    robot_info = parse_robots_info(input_file)
    simulate_movement(board, robot_info)

    #print("After simulation: ")
    #print_board(board)
    quadrants = divide_board(board)
    return compute_safety_rating(quadrants)

def print_board(board):
    for b in board:
        print(b)

if __name__ == "__main__":
    input = 'input.txt'
    test_input = 'test.txt'
    test_board = TEST_ROWS, TEST_COLS
    input_board = NUM_ROWS, NUM_COLS
    print(solve(input, board_size=input_board))