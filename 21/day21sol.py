# Solution to day 21: Keypad Conundrum
#### SUMMARY OF TASKS ####
# Part 1:
# 1. Create a numeric keypad and directional keypad matrix/list
# 2. Read the input and create a function to find the lowest number of keypad presses
# 3. Compute the complexity score of each input 
# 4. Sum the complexity score and return

import math

# NOTE: using (row, col) for this problem

UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'
movement_vectors = {UP: (-1, 0), RIGHT: (0, 1), DOWN: (1, 0), LEFT: (0, -1)} 

# Read the input from the input file
def read_input(input_file):
    with open(input_file, "r") as numeric_file:
        return [line.strip() for line in numeric_file]
    
def sum_tuple(a, b):
    return (a[0] + b[0], a[1] + b[1])

def init_numeric_keypad():
    """
    Returns a dictionary that represents the numeric keypad
    """
    return {(0, 0): '7', (0, 1): '8', (0, 2): '9',
            (1, 0): '4', (1, 1): '5', (1, 2): '6',
            (2, 0): '1', (2, 1): '2', (2, 2): '3',
            (3, 0): None, (3, 1): '0', (3, 2): 'A'}

def init_directional_keypad():
    """
    Returns a dictionary that represents the directional keypad
    """
    return {(0, 0): None, (0, 1): UP, (0, 2): 'A',
            (1, 0): LEFT, (1, 1): DOWN, (1, 2): RIGHT}


# Helper function to get the coordinate of button in the keypad dictionary
def get_button_position(keypad, button):
    """
    Given a <keypad> dict and a <button> value, return its (row, col) coordinate.
    """
    # Extract the button coordinate into a list
    button = [k for k, v in keypad.items() if v == button]

    # Return the first element of the list (sole button)
    return button[0] if button else -1

# Helper function to extract numeric paths of a door code
def extract_numeric_code(code):
    num_code = ""
    for char in code:
        if char.isdigit():
            num_code += char
    try:
        return int(num_code)
    except ValueError:
        raise ValueError("Num code extraction failed.")

def get_paths(start_pos, end_pos, keypad):
    """
    Given start_pos and end_pos, return a list of paths from one to the other on
    the <keypad>.
    """
    paths = []

    # Base case: same button, press A to return
    if start_pos == end_pos:
        return ['A']

    # Inner helper function:
    def test_path(path):
        curr_pos = start_pos
        next_pos = None
        for move in path:
            next_pos = sum_tuple(curr_pos, move)
            if next_pos in keypad:
                # Filter out paths that steps on None space
                if keypad[next_pos] == None:
                    return False
                curr_pos = next_pos
            else:
                return False
        return next_pos == end_pos

    # NOTE: coordinates are (row, cols)

    # Compute the change in rows and cols on the keypad
    d_row, d_col = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]

    # Determine the direction of movement
    hori_dir = LEFT if d_col < 0 else RIGHT
    vert_dir = UP if d_row < 0 else DOWN

    # Build movements as a list
    hori_movements = [movement_vectors[hori_dir]] * abs(d_col)
    vert_movements = [movement_vectors[vert_dir]] * abs(d_row)

    # Test paths from start to end
    for path in [hori_movements + vert_movements, vert_movements + hori_movements]:
        if test_path(path): # path test successful; does not move over gaps
            
            # Convert movement into path (string) of buttons on keypad
            path_string = "".join([dir for move in path for dir in get_button_position(movement_vectors, move)]) + "A"

            if path_string not in paths:
                paths.append(path_string) # Add unqiue paths to the list to be returned
    return paths
        
def solve(input_file):
    """
    Produce the solution to the day 21 problem - Keypad Conundrum
    """
    codes = read_input(input_file)
    complexity_score = 0

    for code in codes:
        numeric_code = extract_numeric_code(code)
        
        shortest_path = solve_helper(code, depth=3)

        complexity = numeric_code * len(shortest_path)

        complexity_score += complexity
    return complexity_score

memo = {}

def solve_helper(target_code, depth):
    # Base case: we reached the user
    if depth == 0:
        #print(f"base case reached, returning {target_code}")
        return target_code
    
    if (target_code, depth) in memo:
        return memo[(target_code, depth)]
    
    if depth == 3: # Not numeric pad
        keypad = init_numeric_keypad()
    else:
        keypad = init_directional_keypad()

    # Initialize the current position
    curr_pos = get_button_position(keypad, "A")

    # Initialize the full shortest sequence
    full_shortest_sequence = ""
    
    # Recursive Case: We want to pick the minimum length sequence for each layer
    for char in target_code:
        char_pos = get_button_position(keypad, char)
        all_paths = get_paths(curr_pos, char_pos, keypad)

        min_sequence = None

        for path in all_paths:
            path_sequence = solve_helper(path, depth - 1)
            if min_sequence is None:
                min_sequence = path_sequence
            else:
                min_sequence = min(min_sequence, path_sequence, key=len)

        if min_sequence is not None:
            full_shortest_sequence += min_sequence
        
        curr_pos = char_pos

    memo[(target_code, depth)] = full_shortest_sequence
    return full_shortest_sequence


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))