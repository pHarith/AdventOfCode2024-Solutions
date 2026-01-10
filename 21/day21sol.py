# Solution to day 21: Keypad Conundrum
#### SUMMARY OF TASKS ####
# Part 1:
# 1. Create a numeric keypad and directional keypad matrix/list
# 2. Read the input and create a function to find the lowest number of keypad presses
# 3. Compute the complexity score of each input 
# 4. Sum the complexity score and return

# Read the input from the input file
def read_input(input_file):
    with open(input_file, "r") as numeric_file:
        return [line.strip() for line in numeric_file]

def init_directional_keypad():
    pass

def init_numeric_keypad():
    pass

def compute_complexity_score():
    pass


def solve(input_file):
    """
    Produce the solution to the day 21 problem - Keypad Conundrum
    """
    return read_input(input_file)


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))