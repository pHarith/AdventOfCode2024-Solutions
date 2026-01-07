# Solution to day 20: Race Condition 
#### SUMMARY OF TASKS ####
# 1. 

# Constances for mapping purposes
START = 'S'
END = 'E'
WALL = '#'

UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'

from collections import deque

# Dictionaries to help us define movement
movement_vectors = {UP: (0, -1), RIGHT: (1, 0), DOWN: (0, 1), LEFT: (-1, 0)} 

def sum_tuple(a, b):
    return (a[0] + b[0], a[1] + b[1])

def parse_board(input_file):
    """
    Given an input file, read the board into a nested list.
    """
    board = []
    with open(input_file, "r") as file:
        board_str = file.read()
        # Split the board into a nested list of strings
        board = [list(row) for row in board_str.split('\n')]
    return board

def find_shortest_path(start_pos, end_pos, board):
    """
    Using BFS, returns the shortest path through the race track and a dictionary that details the nodes traversed.
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
            return board[y][x] != WALL
        return False
    
    # Initialize path and visited set
    path_queue = [(0, start_pos)] # path stores (<distance from start_pos>, <curr_pos>)
    dist_to = {start_pos: 0}
    queue = deque(path_queue)
    visited = set()
    visited.add(start_pos)

    while queue:
        dist, curr_pos = queue.popleft()

        dist_to[curr_pos] = dist

        if curr_pos == end_pos:
            return dist, dist_to
        
        for vector in movement_vectors.values():
            new_pos = sum_tuple(curr_pos, vector)
            if is_valid_move(new_pos) and new_pos not in visited:
                visited.add(new_pos)
                queue.append((dist + 1, new_pos))

    return -1, dist_to


def find_start_end(board):
    start = None
    end = None
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[j][i] == START:
                start = (i, j)
            
            if board[j][i] == END:
                end = (i, j)
    return start, end

def find_viable_cheats(board, dist_to, save_threshold):
    path_tiles = [tile for tile in dist_to.keys()]
    valid_cheats = []
    num_rows, num_cols = len(board), len(board[0])

    def is_valid_move(pos):
        """
        Returns if move made by the user is valid.
        
        :param pos: (x, y) - where x is the x coordinate of the object on the board
        and y is the y-coordinate of the object on the board.
        """
        x, y = pos
        if 0 <= x < num_cols and 0 <= y < num_rows:
            return board[y][x] != WALL
        return False

    for curr_pos in path_tiles:
        for move in [UP, DOWN, LEFT, RIGHT]:
            # Check for any walls adjacent to it
            pos_1 = sum_tuple(curr_pos, movement_vectors[move])

            if is_valid_move(pos_1):
                continue

            pos_2 = sum_tuple(pos_1, movement_vectors[move])
            
            if is_valid_move(pos_2) and pos_2 in dist_to: # tile exists on the path
                normal_dist = dist_to[pos_2] - dist_to[curr_pos]
                cheat = 2
                saving = normal_dist - cheat
                if saving >= save_threshold:
                    valid_cheats.append((curr_pos, pos_2))
                continue
            
            pos_3 = sum_tuple(pos_2, movement_vectors[move])
            if is_valid_move(pos_3) and pos_3 in dist_to: # tile exists on the path
                normal_dist = dist_to[pos_3] - dist_to[curr_pos]
                cheat = 3
                saving = normal_dist - cheat
                if saving >= save_threshold:
                    valid_cheats.append((curr_pos, pos_3))

    return len(valid_cheats)


# PART 2:
# Adjust the cheat searching phase by using a BFS
def find_viable_cheats_2(board, dist_to, save_threshold):
    path_tiles = [tile for tile in dist_to.keys()]
    valid_cheats = []
    num_rows, num_cols = len(board), len(board[0])

    def is_valid_move(pos):
        """
        Returns if move made by the user is valid.
        
        :param pos: (x, y) - where x is the x coordinate of the object on the board
        and y is the y-coordinate of the object on the board.
        """
        return not (is_out_of_bounds(pos) or is_wall(pos))

    def is_out_of_bounds(pos):
        """
        Returns if move made by the user is out of bounds of the board
        
        :param pos: (x, y) - where x is the x coordinate of the object on the board
        and y is the y-coordinate of the object on the board.
        """
        x, y = pos
        return not(0 <= x < num_cols and 0 <= y < num_rows)
    
    def is_wall(pos):
        return not is_out_of_bounds(pos) and board[pos[1]][pos[0]] == WALL
    
    def find_cheat_paths(pos, cheat_limit):
        """
        Return a list of end_pos of any valid paths.
        
        :param pos: the current position in the maze.
        """
        cheat_ends = []

        # Initialize path and visited set
        cheat_queue = [(0, pos)] # path stores (<cheat distance>, <curr_pos>)
        queue = deque(cheat_queue)
        visited = set()

        while queue:
            dist, curr_pos = queue.popleft()

            if dist >= cheat_limit:  # Surpassed 20 ps cheat limit, search a different tile
                continue
            
            for vector in movement_vectors.values():
                new_pos = sum_tuple(curr_pos, vector)   # Compute new position after moving

                if new_pos in visited or is_out_of_bounds(new_pos):
                    continue

                # Mark the new position as visited
                visited.add(new_pos)
                new_dist = dist + 1

                # Check if the new position is a free space or a wall
                if is_valid_move(new_pos) and new_pos in dist_to and dist_to[new_pos] > dist_to[pos]:   # is a space on the path and moves us forward in the maze
                    cheat_ends.append((new_dist, new_pos))
                    queue.append((new_dist, new_pos))
                else:
                    # new pos is a wall, we continue searching through it
                    queue.append((new_dist, new_pos))    

        return cheat_ends
    
    for curr_pos in path_tiles:
        cheat_end_pos = find_cheat_paths(curr_pos, cheat_limit=20)  # Append the end position of any possible cheat paths that pass the threshold
        print(f"From {curr_pos}: found {len(cheat_end_pos)} potential cheats")
        if cheat_end_pos is not None:
            for cheat_dist, end in cheat_end_pos:
                saving = dist_to[end] - dist_to[curr_pos] - cheat_dist  # Compute the amounts of picoseconds saved
            
                if saving >= save_threshold:    # Cheat saved at least <save_threshold> seconds
                    valid_cheats.append((curr_pos, end))

    return len(valid_cheats)
            

def print_board(board):
    for row in board:
        for item in row:
            print(item, end="")
        print()


def solve(input_file):
    """
    Produce the solution to the day 20 problem - Race Condition 
    """
    board = parse_board(input_file)

    start, end = find_start_end(board)

    # Record the time taken to travese race track normally and store the distance to each tile
    time, dist_to = find_shortest_path(start, end, board)

    # Return list of viable cheats
    return find_viable_cheats_2(board, dist_to, save_threshold=100)


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))