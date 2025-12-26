# Solution to day 18: RAM Run
#### SUMMARY OF TASKS ####
# 1. Read the file as a list of corrupted bytes coordinates
# 2. Create a board of specific size, and placing corrupted bits as such
# 3. 

EMPTY_SPACE = '.'
CORRUPTED = '#'

def read_corrupted_coordinates(input_file):
    corrupted_coordinates = []
    with open(input_file, "r") as corrupted_bytes:
        for byte in corrupted_bytes:
            x, y = byte.strip().split(',')
            corrupted_coordinates.append((int(x), int(y)))
    print(corrupted_coordinates)
    return corrupted_coordinates

def create_board(board_size):
    return [[EMPTY_SPACE] * board_size for _ in range(board_size)]

def add_corrupted_bytes(board, corrupted_coordinates):
    i = 0
    for coordinate in corrupted_coordinates:
        board[coordinate[1]][coordinate[0]] = CORRUPTED

def find_shortest_path(start, end, board):
    pass

def print_board(board):
    for row in board:
        for item in row:
            print(item, end="")
        print()


def solve(input_file, board_size):
    """
    Produce the solution to the day 18 problem - RAM Run
    """
    board = create_board(board_size)
    corrupted_bytes = read_corrupted_coordinates(input_file)
    add_corrupted_bytes(board, corrupted_bytes)
    print_board(board)
    return 


if __name__ == "__main__":
    # input, board_size = 'input.txt', 71
    input, board_size = 'test.txt', 7
    print(solve(input, board_size))