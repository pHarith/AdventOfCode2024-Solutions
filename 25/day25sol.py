# Solution to day 25: Code Chronicle
#### SUMMARY OF TASKS (part 1) ####
# 1. Read the schematics from the input file, likely a matrix, separating locks and keys
# 2. Convert the matrix into a list of heights, and group them into 2 sets: locks, keys.
# 3. Attempt matching the key, locks by checking if: 
# height_of_key_col + height_of_lock_col <= height_of_available_col
# 4. Return the number of key-lock pairs that fit


# Helper functions for part 1
def read_key_lock_schematics(input):
    keys, locks = [], []
    with open(input, "r") as schematics:
        # Split the file into strings of schematics
        key_locks_str = schematics.read().split('\n\n')
        
        print(f"{key_locks_str}")

        key_locks_lst = [item_str.strip().split('\n') for item_str in key_locks_str]

        # Convert each string item into a matrix
        for mtx in key_locks_lst:
            num_rows, num_cols = len(mtx), len(mtx[0])
            count_mtx = convert_mtx_into_height_lst(mtx, num_cols)
            if mtx[0][0] == '#':   # is a lock
                #locks.append(mtx)
                locks.append(count_mtx)
            elif mtx[0][0] == '.': # is a key
                #keys.append(mtx)
                keys.append(count_mtx)
            else:
                raise ValueError("Expected '.' or '#' characters. Invalid File.")
    print(f'{num_rows = } , {num_cols = }')
    print(f'{keys = }')
    print(f'{locks = }')
    return num_rows, num_cols, keys, locks   


def convert_mtx_into_height_lst(mtx, num_cols):
    count = [0] * num_cols
    # TODO: Convert each matrix into a list of numbers based on numbers of # in each column
    for row in mtx:
        for j in range(num_cols):
            if row[j] == '#':
                count[j] += 1
            elif row[j] != '.':
                raise ValueError("Expected '.' or '#' characters. Invalid Matrix.")
    return count



def solve(input_file):
    """
    Produce the solution to the day 25 problem - Code Chronicle
    """
    
    valid_combos = []

    num_rows, num_cols, keys, locks = read_key_lock_schematics(input)

    for key in keys:
        for lock in locks:
            
            invalid = False

            for i in range(num_cols):
                if invalid:
                    break
                elif key[i] + lock[i] > num_rows:
                    invalid = True
                
            if not invalid:
                valid_combos.append((keys, locks))

    return valid_combos, len(valid_combos)


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))