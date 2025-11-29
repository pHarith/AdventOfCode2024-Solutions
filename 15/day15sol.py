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

# Imports for part 2
from collections import deque


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

def handle_vertical_box(move_vector, box_info, board):

    start_box, _ = box_info

    def adjacent_boxes_bfs():
        """
        Return adjacent boxes that is affected by the move i.e. also pushed if the robot moves
        and pushes a box.
        """

        queue = deque()
        adjacent_boxes = []
        visited = ()

        queue.append(start_box)
        visited.add(start_box)

        while queue:
            curr_box = queue.popleft()
            curr_box_left, curr_box_right = curr_box

            adj_box.append(curr_box)

            # Find their new positions
            new_box_left = sum_tuple(curr_box_left, move_vector)
            new_box_right = sum_tuple(curr_box_right, move_vector)

            # Split x and y to check board indices
            new_box_left_x, new_box_left_y = new_box_left
            new_box_right_x, new_box_right_y = new_box_right

            # Check for walls (end move)
            if board[new_box_left_x][new_box_left_y] == WALL or board[new_box_right_x][new_box_right_y] == WALL:
                return None     # No possible move

            # Check for "children" i.e. potential boxes for each side
            if new_box_left in [BOX_LEFT, BOX_RIGHT]:
                adj_box = get_box_pos(board, new_box_left_x, new_box_left_y)
                if adj_box not in visited:
                    visited.add(adj_box)
                    queue.append(adj_box)

            if new_box_right in [BOX_LEFT, BOX_RIGHT]:
                adj_box = get_box_pos(board, new_box_right_x, new_box_right_y)
                if adj_box not in visited:
                    visited.add(adj_box)
                    queue.append(adj_box)
        
        return adjacent_boxes

    boxes_to_push = adjacent_boxes_bfs()

    if boxes_to_push is None:
        return False

    # Push the box, start from the last box
    for i in range(len(boxes_to_push) - 1, -1, -1): # start from last index, go backwards by -1 until it loops back
        current_box = boxes_to_push[i]
        left_x, left_y = current_box[0]
        right_x, right_y = current_box[1]

        # Compute their new positions
        new_left_x, new_left_y = sum_tuple((left_x, left_y), move_vector)
        new_right_x, new_right_y = sum_tuple((right_x, right_y), move_vector)

        # Empty out the previous positions
        board[left_y][left_x] = EMPTY_SPACE
        board[right_y][right_x] = EMPTY_SPACE

        # Push the box in the direction of move
        board[new_left_y][new_left_x] = BOX_LEFT
        board[new_right_y][new_right_x] = BOX_RIGHT 

    return True

def handle_horizontal_box(move_vector, box_info, board):
    box_pos, other_side = box_info

    # We always want to start from the end of the box
    check_pos = box_pos[other_side]

    # Collect all the boxes (useful for pushing later)
    boxes_to_push = [box_pos]

    while True: # Check until we hit empty space (Success) or wall (Fail)
        check_pos = sum_tuple(check_pos, move_vector)
        check_x, check_y = check_pos

        if board[check_y][check_x] == WALL:
            return False
        elif board[check_y][check_x] == EMPTY_SPACE:
            # Push the box, start from the last box
            for i in range(len(boxes_to_push) - 1, -1, -1): # start from last index, go backwards by -1 until it loops back
                current_box = boxes_to_push[i]
                left_x, left_y = current_box[0]
                right_x, right_y = current_box[1]

                # Compute their new positions
                new_left_x, new_left_y = sum_tuple((left_x, left_y), move_vector)
                new_right_x, new_right_y = sum_tuple((right_x, right_y), move_vector)

                # Empty out the previous positions
                board[left_y][left_x] = EMPTY_SPACE
                board[right_y][right_x] = EMPTY_SPACE

                # Push the box in the direction of move
                board[new_left_y][new_left_x] = BOX_LEFT
                board[new_right_y][new_right_x] = BOX_RIGHT 
            
            return True
        elif board[check_y][check_x] in [BOX_LEFT, BOX_RIGHT]:
            new_box_pos, other_side = get_box_pos(board, check_x, check_y)

            if new_box_pos is None:
                return             
            boxes_to_push.append(new_box_pos)
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