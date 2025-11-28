# Solution to day 15: Warehouse Woes
#### SUMMARY OF TASKS ####
# 1. Read the input file, split into movements and board.
# 2. Navigate the board using the movements
# 3. Record the positions of the boxes on the board
# 4. Compute the "GPS" of each box

#### SUMMARY OF TASKS (Part 2) ####
# 1. Transform board into the larger board
# 2. Alter move_robot_on_board to factor in new rules
# 3. Alter sum_gps to factor in new rules

# Constants for items on board
WALL = '#'
ROBOT = '@'
BOX = 'O'
EMPTY_SPACE = '.'

# Dictionaries to help us define movement
movement_dictionary = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)} 

# Dictionary to transform objects on board in part 1 to objects in part 2
transform_dict = {WALL: '##', ROBOT: '@.', BOX: '[]', EMPTY_SPACE: '..'}

# CONSTANTS FOR PART 2
BOX_LEFT = '['
BOX_RIGHT = ']'


def compute_gps_score(box_coord):
    """
    Return the gps of a box from their coordinates (x, y) where:

    gps_score = 100 * y + x
    """
    x, y = box_coord
    return 100 * y + x

def sum_tuple(a, b):
    return (a[0] + b[0], a[1] + b[1])


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
        movement_instr = movement_instr.replace("\n", "")
    return board, movement_instr


def move_robot_on_board(robot_pos, board, movement):
    init_pos = robot_pos
    for move in movement:
        valid_move = True

        # Grab the movement vector from the dictionary
        move_vector = movement_dictionary[move]

        init_x, init_y = init_pos

        # Sanity check if the robot position is correct
        if not board[init_y][init_x] == ROBOT:
            continue
        
        new_pos = sum_tuple(init_pos, move_vector)

        new_x, new_y = new_pos
        
        if board[new_y][new_x] == WALL:
            # print("we hit a wall")
            continue
        
        if board[new_y][new_x] == BOX:
            # print("Box found")
            check_pos = new_pos # Begin checking adjacent positions for boxes or walls
            
            while valid_move: # Check until we hit empty space (Success) or wall (Fail)
                check_pos = sum_tuple(check_pos, move_vector)
                check_x, check_y = check_pos

                if board[check_y][check_x] == WALL:
                    valid_move = False
                elif board[check_y][check_x] == EMPTY_SPACE:
                    # Push the box
                    # print("Box pushed!")
                    board[check_y][check_x] = BOX
                    break
        
        # Execute move (this happens whether we push a box or not)
        if valid_move:
            board[init_y][init_x] = EMPTY_SPACE
            board[new_y][new_x] = ROBOT
            init_pos = new_pos
        # print_board(board)
    return
    
def find_unit_pos(board, unit):
    for i in range(len(board)):
        if unit in board[i]:
            # Inverse rows and cols for x and y 
            # x coord = col, y coord = row
            return (board[i].index(unit), i)    
    return None
        
def gps_sum(board):
    sum = 0
    num_rows, num_cols = len(board), len(board[0])

    for y in range(num_rows):
        for x in range(num_cols):
            if board[y][x] == BOX:
                sum += compute_gps_score((x, y))
    return sum

def solve(input_file):
    """
    Produce the solution to the day 15 problem - Warehouse Woes
    """
    board, movement_instr = parse_board_and_movement(input_file)
    init_robot_pos = find_unit_pos(board, unit=ROBOT)
    if init_robot_pos is not None:
        move_robot_on_board(init_robot_pos, board, movement_instr)
    print_board(board)
    return gps_sum(board)

def print_board(board):
    for row in board:
        for item in row:
            print(item, end="")
        print()


## PART 2 ##
def transform_board(board):
    """
    From the rules given in part 2, transform any board into new board:
    # becomes ##
    O becomes []
    . becomes ..
    @ becomes @.
    """
    # NOTE: @ still moves at the same pace.
    new_board = []
    for i in range(len(board)):
        new_row = []
        for j in range(len(board[0])):
            new_row.extend(list(transform_dict[board[i][j]]))
        new_board.append(new_row)
    return new_board

def get_box_pos(board, x, y):
    if board[y][x] == BOX_LEFT:
        if board[y][x+1] == BOX_RIGHT:
            return ((x, y), (x+1, y), 1)
    if board[y][x] == BOX_RIGHT:
        if board[y][x-1] == BOX_LEFT:
            return (((x-1, y), (x, y)), 0)
    return None, None

def handle_vertical_box(move, move_vector, box_info, board):
    valid_move = True

    return valid_move

def handle_horizontal_box(move, move_vector, box_info, board):
    box_pos, other_side = box_info

    check_pos = box_pos[other_side]

    while True: # Check until we hit empty space (Success) or wall (Fail)
        check_pos = sum_tuple(check_pos, move_vector)
        check_x, check_y = check_pos

        if board[check_y][check_x] == WALL:
            return False
        elif board[check_y][check_x] == EMPTY_SPACE:
            # Push the box
            
            # board[check_y][check_x] = BOX
            return True
        elif board[check_y][check_x] in [BOX_LEFT, BOX_RIGHT]:
            new_box_pos, other_side = get_box_pos(board, check_x, check_y)
            check_pos = new_box_pos[other_side]



def move_robot_on_board_2(robot_pos, board, movement):
    init_pos = robot_pos
    for move in movement:
        valid_move = True

        # Grab the movement vector from the dictionary
        move_vector = movement_dictionary[move]

        init_x, init_y = init_pos

        # Sanity check if the robot position is correct
        if not board[init_y][init_x] == ROBOT:
            continue
        
        new_pos = sum_tuple(init_pos, move_vector)

        new_x, new_y = new_pos
        
        if board[new_y][new_x] == WALL:
            # print("we hit a wall")
            continue
        
        # if board[new_y][new_x] == BOX:
        # NOTE: For part 2, change the condition to be equal to box-left or box-right
        if board[new_y][new_x] in [BOX_LEFT, BOX_RIGHT]:
            
            # Find the full box and return the other side of the search
            if not get_box_pos(board, new_x, new_y):
                return

            # Handle horizontal and vertical movement separately

            if move in ['<', '>']: # Horizontal movement
                valid_move = handle_horizontal_box(move, move_vector, get_box_pos(board, new_x, new_y), board)
        
            else: # Vertical movement
                valid_move = handle_vertical_box(move, move_vector, get_box_pos(board, new_x, new_y), board)
        
        # Execute move (this happens whether we have to push a box or walk to empty space)
        if valid_move:
            board[init_y][init_x] = EMPTY_SPACE
            board[new_y][new_x] = ROBOT
            init_pos = new_pos
        # print_board(board)
    return

def solve_part2(input_file):
    """
    Produce the solution to part 2 of the day 15 problem - Warehouse Woes
    """
    board, movement_instr = parse_board_and_movement(input_file)
    new_board = transform_board(board)
    # init_robot_pos = find_unit_pos(board, unit=ROBOT)
    # if init_robot_pos is not None:
    #    move_robot_on_board(init_robot_pos, board, movement_instr)
    print_board(new_board)
    return


if __name__ == "__main__":
    #input = 'input.txt'
    #input = 'test.txt'
    input = 'smalltest.txt'
    # print(solve(input))
    print(solve_part2(input))