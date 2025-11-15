# Solution to day 8: Resonant Collinearity
#### SUMMARY OF TASKS ####
# 1. 


import itertools

def parse_board(input_file):
    """
    Given a text file, create a matrix representing board.
    """
    # Read the file and convert the text into a board
    with open(input_file, "r") as file:
        board_str = file.read()
        board = [list(row) for row in board_str.strip().split('\n')]
    
    return board


def sort_signals(board, num_rows, num_cols):
    """
    Given a board of size m x n, return a dictionary k:v where
    k - the signal frequency
    v - a list of coordinates where these signal frequencies are located
    and a list of empty spaces on the board
    """
    signals = {}
    empty_spaces = []
    for i in range(num_rows):
        for j in range(num_cols):
            if board[i][j] != '.': # not a free spot
                if board[i][j] in signals:
                    signals[board[i][j]].append((i, j))
                else:
                    signals[board[i][j]] = [(i, j)]
            else:
                empty_spaces.append((i, j))
    return signals, empty_spaces


def spawn_antinodes(coords, num_rows, num_cols):
    coord_combinations = itertools.combinations(coords, 2) # Form pairs of combinations
    new_antinodes = set()

    for pair in coord_combinations:
        dr, dc = pair[0][0] - pair[1][0], pair[0][1] - pair[1][1]
        node1, node2 = (pair[0][0] + dr, pair[0][1] + dc), (pair[1][0] - dr, pair[1][1] - dc)
        if 0 <= node1[0] < num_rows and 0 <= node1[1] < num_cols:
            new_antinodes.add(node1)
        if 0 <= node2[0] < num_rows and 0 <= node2[1] < num_cols:
            new_antinodes.add(node2)
    return new_antinodes

def spawn_antinodes_2(coords, num_rows, num_cols):
    coord_combinations = itertools.combinations(coords, 2) # Form pairs of combinations
    new_antinodes = set()

    for pair in coord_combinations:
        new_antinodes.update(set(pair))
        dr, dc = pair[0][0] - pair[1][0], pair[0][1] - pair[1][1]

        node1, node2 = (pair[0][0] + dr, pair[0][1] + dc), (pair[1][0] - dr, pair[1][1] - dc)

        while 0 <= node1[0] < num_rows and 0 <= node1[1] < num_cols:
            new_antinodes.add(node1)
            node1 = (node1[0] + dr, node1[1] + dc)

        while 0 <= node2[0] < num_rows and 0 <= node2[1] < num_cols:
            new_antinodes.add(node2)
            node2 = (node2[0] - dr, node2[1] - dc)
    return new_antinodes


def solve(input_file):
    """
    Produce the solution to the day 8 problem - Resonant Collinearity
    """

    antinodes = set()

    board = parse_board(input_file)
    row, col = len(board), len(board[0])
    signals, empty_spaces = sort_signals(board, row, col)

    # print(signals)

    for signal, coord in signals.items():
        # print(signal, coord)
        # antinodes.update(spawn_antinodes(coord, row, col))
        antinodes.update(spawn_antinodes_2(coord, row, col))

    # print(antinodes)
    return len(antinodes)


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))

    # Change the spawn_antinodes function in solve() to adjust for part 1 or part 2