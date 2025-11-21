# Solution to day 15: Warehouse Woes
#### SUMMARY OF TASKS ####
# 1. Read the input file, split into movements and board.
# 2. Navigate the board using the movements
# 3. Record the positions of the boxes on the board
# 4. Compute the "GPS" of each box

# Constants for items on board
WALL = '#'
ROBOT = '@'
BOX = 'O'

# Dictionaries to help us define movement
movement_dictionary = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)} 


def compute_gps_score(box_coord):
    """
    Return the gps of a box from their coordinates (x, y) where:

    gps_score = 100 * y + x
    """
    x, y = box_coord
    return 100 * y + x


def parse_board_and_movement(input_file):
    """
    Given an input file, read the board and movement instruction into a nested list.
    Returns the board and movement instructions.
    """
    board = []
    movement_instr = []
    with open(input_file, "r") as file:
        board_str, movement_instr = file.read().split('\n\n') # split the board and movement upon the first empty line

        # Split the board into a nested list of strings
        board = [list(row) for row in board_str.split('\n')]
    return board, movement_instr


def move_robot_on_board(robot_pos, board, movement):
    pass

def find_robot_pos(board):
    for i in range(len(board)):
        if ROBOT in board[i]:
            # Inverse rows and cols for x and y 
            # x coord = col, y coord = row
            return (board[i].index(ROBOT), i)
    
    return None
        
def gps_sum(board):
    pass

def solve(input_file):
    """
    Produce the solution to the day 15 problem - Warehouse Woes
    """
    board, movement_instr = parse_board_and_movement(input_file)
    init_robot_pos = find_robot_pos(board)
    if init_robot_pos is not None:
        move_robot_on_board(init_robot_pos, board, movement_instr)
    return gps_sum(board)

if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))