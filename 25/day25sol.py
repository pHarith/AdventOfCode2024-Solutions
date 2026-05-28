# Solution to day 25: Code Chronicle
#### SUMMARY OF TASKS (part 1) ####
# 1. Read the schematics from the input file, likely a matrix, separating locks and keys
# 2. Convert the matrix into a list of heights, and group them into 2 sets: locks, keys.
# 3. Attempt matching the key, locks by checking if: 
# height_of_key_col + height_of_lock_col <= height_of_available_col
# 4. Return the number of key-lock pairs that fit


# Helper functions for part 1
def read_key_lock_schematics(input):
    keys, locks = set(), set()
    with open(input, "r") as schematics:
        # Split the file into strings of schematics
        key_locks_str = schematics.read().split('\n\n')

        # Convert each string item into a matrix
        for item_str in key_locks_str:
            mtx = item_str.strip().split('\n')
            if item_str[0] == '#':   # is a lock
                pass
            elif item_str[0] == '.': # is a key
                pass
            else:
                raise ValueError("Expected '.' or '#' characters. File Error")

    return keys, locks   


def convert_mtx_into_number_lst(mtx):
    count = []
    # TODO: Convert each matrix into a list of numbers based on numbers of # in each column
    return count



def solve(input_file):
    """
    Produce the solution to the day 25 problem - Code Chronicle
    """
    return


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))