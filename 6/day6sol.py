# Solution to day 6: Guard Gallivant
#### SUMMARY OF TASKS ####
# 1. Read the entire input file into a matrix (nested list) to represent the board
# 2. Locate the guard character - '^' and record the coordinate
# 3. Navigate using the movement matrix, until '#' is found
# 4. For every movement made, replace the '.' with 'X', keep count of the number of '.' replaced.
# 5. Return the number of '.' replaced + 1 (number of unique positions)


# Part 2 : Brainstorm #
# 1. Keep track of (position, movement_direction) to figure out if a loop exists
# 2. Bruteforce placing an obstacle everywhere and try to navigate normally until it hits a loop
# 2.5 NOTE: placing obstacles on empty tiles where the guard never patrolled in the first place would not 
# cause a loop!
# 3. Append counts of possible obstacle placements

# Part 2: Steps #
# 1. Rerun the code from part 1, but this time, do the following:
# - Aside from the starting position, track all crossed tiles and the direction the guard is 
# moving at the moment. Use crossed tiles as possible locations to place obstacles.
#  

# Loop Error
class LoopError(Exception):
    pass

# Hardcoded positions
OBSTACLES = '#'
GUARD = '^'
FREE_TILE = '.'
CROSSED_TILE = 'X'


movement_dict = {'up': (-1, 0), 'down': (1, 0), 'right': (0, 1), 'left': (0, -1)}
rotation_dict = {'up': 'right', 'down': 'left', 'right': 'down', 'left': 'up'}


def add_tuples(a, b):
    """
    Add two tuples, return their sum
    """
    return tuple(x + y for x, y in zip(a, b))


def parse_board(input_file):
    """
    Given a text file, create a matrix representing board and position of the guard.
    """
    # Read the file and convert the text into a board
    with open(input_file, "r") as file:
        board_str = file.read()
        board = [list(row) for row in board_str.strip().split('\n')]
    
    return board

def solve(input_file):
    """
    Produce the solution to the day 6 problem - Guard Gallivant
    """
    board = parse_board(input_file)

    num_rows, num_cols = len(board), len(board[0])

    for r in range(num_rows):
        if '^' in board[r]:
            guard_position = (r, board[r].index('^'))

    _, _, distinct_tiles = traverse_board(board, num_rows, num_cols, guard_position)
    
    # print_board(board)s
    return distinct_tiles

def print_board(board):
    for row in board:
        print(row)

def traverse_board(board, num_rows, num_cols, guard_position, default_direction='up'):
    crossed_tiles = []
    guard_path = []

    while (0 <= guard_position[0] < num_rows and 0 <= guard_position[1] < num_cols):
        new_position = add_tuples(guard_position, movement_dict[default_direction])
        # print(new_position)

        # Check for loops
        if (default_direction, new_position) in guard_path: # Loop detected
            raise LoopError('loop found')

        dr, dc = new_position

        if not (0 <= dr < num_rows and 0 <= dc < num_cols):
           break

        if board[dr][dc] == FREE_TILE and new_position not in crossed_tiles:
            crossed_tiles.append(new_position)
            guard_path.append((default_direction, new_position))
            
        elif board[dr][dc] == OBSTACLES:
            default_direction = rotation_dict[default_direction]
            continue

        guard_position = new_position

    return crossed_tiles, guard_path, len(crossed_tiles) + 1


def solve_part2(input_file):
    """
    Solve part 2 to the day 6 problem - Guard Gallivant
    """
    obstacles_location = 0
    board = parse_board(input_file)

    num_rows, num_cols = len(board), len(board[0])

    for r in range(num_rows):
        if '^' in board[r]:
            guard_position = (r, board[r].index('^'))

    crossed_tiles, _, _ = traverse_board(board, num_rows, num_cols, guard_position)
    
    for tile in crossed_tiles:
        dr, dc = tile
        board[dr][dc] = OBSTACLES
        try:
            traverse_board(board, num_rows, num_cols, guard_position)
        except LoopError:
            obstacles_location += 1
        board[dr][dc] = FREE_TILE

    return obstacles_location



if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))
    # print(solve_part2(input))

# The answer to part 1 is 4752
# The answer to part 2 is 1719