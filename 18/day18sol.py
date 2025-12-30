# Solution to day 18: RAM Run
#### SUMMARY OF TASKS ####
# 1. Read the file as a list of corrupted bytes coordinates
# 2. Create a board of specific size, and placing corrupted bits as such
# 3. 

EMPTY_SPACE = '.'
CORRUPTED = '#'

UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'

# Dictionaries to help us define movement
movement_vectors = {UP: (0, -1), RIGHT: (1, 0), DOWN: (0, 1), LEFT: (-1, 0)} 

from collections import deque


def sum_tuple(a, b):
    return (a[0] + b[0], a[1] + b[1])

def read_corrupted_coordinates(input_file):
    corrupted_coordinates = []
    with open(input_file, "r") as corrupted_bytes:
        for byte in corrupted_bytes:
            x, y = byte.strip().split(',')
            corrupted_coordinates.append((int(x), int(y)))
    # print(corrupted_coordinates)
    return corrupted_coordinates

def create_board(board_size):
    return [[EMPTY_SPACE] * board_size for _ in range(board_size)]

def add_corrupted_bytes(board, corrupted_coordinates, byte_fallen):
    if len(corrupted_coordinates) < byte_fallen:
        raise ValueError("<byte_fallen> must be a higher value than length of <corrupted_coordinates>")

    # Make a copy of the board
    corrupted_board = [row[:] for row in board]

    for i in range(byte_fallen):
        x, y = corrupted_coordinates[i][0], corrupted_coordinates[i][1]
        corrupted_board[y][x] = CORRUPTED

    return corrupted_board


def find_shortest_path(start_pos, end_pos, board):
    """
    Using BFS, returns the shortest path through the corrupted memory space.
    """
    num_rows, num_cols = len(board), len(board[0])

    def is_valid_move(pos):
        """
        Returns if move made by the user is valid.
        
        :param pos: (x, y) - where x is the x coordinate of the object on the board
        and y is the y-coordinate of the object on the board.
        """
        x, y = pos
        if 0 <= x < num_cols and 0 <= y < num_rows:
            return board[y][x] != CORRUPTED
        return False
    
    # Initialize path and visited set
    path_queue = [(0, start_pos)] # path stores (<distance from start_pos>, <curr_pos>)
    queue = deque(path_queue)
    visited = set()
    visited.add(start_pos)

    while queue:
        dist, curr_pos = queue.popleft()

        if curr_pos == end_pos:
            return dist
        
        for vector in movement_vectors.values():
            new_pos = sum_tuple(curr_pos, vector)
            if is_valid_move(new_pos) and new_pos not in visited:
                visited.add(new_pos)
                queue.append((dist + 1, new_pos))

    return -1



def print_board(board):
    for row in board:
        for item in row:
            print(item, end="")
        print()


def solve(input_file, board_size, byte_fallen):
    """
    Produce the solution to the day 18 problem - RAM Run
    """
    board = create_board(board_size)
    corrupted_bytes = read_corrupted_coordinates(input_file)
    corrupted_board = add_corrupted_bytes(board, corrupted_bytes, byte_fallen)
    # print_board(board)
    return find_shortest_path((0, 0), (board_size - 1, board_size - 1), corrupted_board)

# Part 2 Code goes here
# NOTE: Binary Search helps narrowing down which amount of byte_fallen to check

def find_min_path_end(board, corrupted_bytes):
    num_corrupted = len(corrupted_bytes)
    left, right = 0, num_corrupted
    
    blocking_byte = (0, 0)

    while left <= right:
        mid = (left + right) // 2
        print(mid, corrupted_bytes[mid])
        
        test_board = add_corrupted_bytes(board, corrupted_bytes, mid+1)

        if find_shortest_path((0, 0), (board_size - 1, board_size - 1), test_board) != -1: # No blockage occurs
            left = mid + 1 # Narrow search from mid to right
        else:   # Blockage occurs
            blocking_byte = corrupted_bytes[mid] # Save potential first blocking byte
            right = mid - 1 # Narrow search from left to mid

    return blocking_byte


def solve_part2(input_file, board_size, byte_fallen):
    """
    Produce the solution to the day 18 problem - RAM Run
    """
    board = create_board(board_size)
    corrupted_bytes = read_corrupted_coordinates(input_file)
    return find_min_path_end(board, corrupted_bytes)

if __name__ == "__main__":
    input, board_size, byte_fallen = 'input.txt', 71, 1024
    # input, board_size, byte_fallen = 'test.txt', 7, 12
    print(solve(input, board_size, byte_fallen))
    print(solve_part2(input, board_size, byte_fallen))