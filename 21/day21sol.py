# Solution to day 21: Keypad Conundrum
#### SUMMARY OF TASKS ####
# Part 1:
# 1. Create a numeric keypad and directional keypad matrix/list
# 2. Read the input and create a function to find the lowest number of keypad presses
# 3. Compute the complexity score of each input 
# 4. Sum the complexity score and return

UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'
movement_vectors = {UP: (0, -1), RIGHT: (1, 0), DOWN: (0, 1), LEFT: (-1, 0)} 

# Read the input from the input file
def read_input(input_file):
    with open(input_file, "r") as numeric_file:
        return [line.strip() for line in numeric_file]

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

def get_keypad_presses(target_code, keypad_type):
    """
    Based on <keypad_type>, find and generate a string sequence such that the <target_code>
    can be obtained using that keypad.
    
    :param target_code: A numeric or directional code, in string format.
    :param keypad_type: numeric keypad or directional keypad
    """
    if keypad_type == "numeric":
        keypad = init_numeric_keypad()
    elif keypad_type == "directional":
        keypad = init_directional_keypad
    else:
        raise ValueError('<keypad_type> must be "numeric" or "directional".')
    
    # Initialize position at "A"
    curr_pos = keypad.keys()[keypad.values.index("A")]


    # Initial keypad sequence
    result = ""

    for char in target_code:

        char_pos = keypad.keys()[keypad.values.index(char)]
        # Find path from current pos to the postion of the character:
        path = find_path(curr_pos, char_pos, keypad)

        result += path + "A"

        curr_pos = char_pos

    return result

def find_path(start_pos, end_pos, keypad):
    """
    Find the best path between <start_pos> and <end_pos> on <keypad>
    
    :param start_pos: position of the button we are on.
    :param end_pos: position of the button we want our both to move to and press.
    :param keypad: dictionary which describes a keypad, numeric or directional.
    """
    path = ""

    # Compute the manhatten distance to move from start_pos to end_pos
    dx, dy = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]

    # NOTE: To optimize movement, group horizontal or vertical movements together. This way, robots controlling on the 
    # upper layers would only have to move to a button once, then press A as needed.

    hori_dir = LEFT if dx < 0 else RIGHT
    hori_movements = [movement_vectors[hori_dir]] * abs(dx)
    verti_dir = UP if dy > 0 else DOWN
    verti_movements = [movement_vectors[verti_dir]] * abs(dy)

    # TODO: Write a function to test if which arrangements of movement is ideal

    # Test horizontal moves first, vertical moves later

    # Test vertical moves first, horizontal moves later

    

    return path


def compute_complexity_score(code_numeric, sequence_length):
    return code_numeric * sequence_length


def solve(input_file):
    """
    Produce the solution to the day 21 problem - Keypad Conundrum
    """
    return read_input(input_file)


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))