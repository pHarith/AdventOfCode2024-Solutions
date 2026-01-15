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

def init_directional_keypad():
    """
    Returns a dictionary that represents the directional keypad
    """
    return {(0, 0): '7', (0, 1): '8', (0, 2): '9',
            (1, 0): '4', (1, 1): '5', (1, 2): '6',
            (2, 0): '1', (2, 1): '2', (2, 2): '3',
            (3, 0): None, (3, 1): '0', (3, 2): 'A'}

def init_numeric_keypad():
    """
    Returns a dictionary that represents the numeric keypad
    """
    return {(0, 0): None, (0, 1): UP, (0, 2): 'A',
            (1, 0): LEFT, (1, 1): DOWN, (1, 2): RIGHT}

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