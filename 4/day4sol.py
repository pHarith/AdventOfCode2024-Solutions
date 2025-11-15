# Solution to day 4: Ceres Search

#### SUMMARY OF TASKS ####
# 1. Read the text into a matrix
# 2. 

import re

WORD = 'MAS'

# Hardcoded 8 directional vectors to traverse the matrix
direction_vectors = [(1,1), (1, 0), (0, 1), (-1,1), (1,-1), (-1,-1), (-1, 0), (0, -1)]


def solve(input_file, word):
    """
    Produce the solution to the day 4 problem - 
    """
    count = 0
    word_search = []
    with open(input_file, "r") as lines:
        for line in lines:
            word_search.append([letter for letter in line.strip()])

    num_rows, num_cols = len(word_search), len(word_search[0])

    # Traverse through rows and cols
    for i in range(num_rows):
        for j in range(num_cols):

            # Check if we find the first letter of the word
            if word_search[i][j] == word[0]:
                for dir_row, dir_col in direction_vectors:
                    # Reset the word back to only the first letter each time
                    found_word = word[0]
                    
                    # Check for the remaining 3 letters
                    for k in range(1, len(word)):
                        # Compute if the direction vector results in a valid index:
                        new_row = i + dir_row * k
                        new_col = j + dir_col * k

                        # Check for out of bounds
                        if new_row in range(0, num_rows) and new_col in range(0, num_cols):
                            # Check if the letter matches matches
                            if word_search[new_row][new_col] == word[k]:
                                found_word += word[k]
                            
                    # Check if word found matches
                    if found_word == word:
                        count += 1
    return count

"""
def generate_x_pattern(word):
    ""
    if len(word) != 3:
        return -1
    
    return [(0, 0, word[0]), (1, 1, word[1]), (2, 2, word[2]), # diagonal-down-right 
            (0, 2, word[0]), (2, 0, word[2]), # diagonal-up-right
            (0, 2, word[2]), (2, 0, word[0]), # diagonal-up-left
            (0, 0, word[2]), (2, 2, word[0])  # diagonal-down-left
            ]
"""

# Hardcoded diagonal coordinates of a 3x3 grid
diagonal_coord = [[(0,0), (1,1), (2,2)], [(0,2), (1, 1), (2,0)]]

def solve_2(input_file, word):
    """
    Produce the solution to the day 4 problem - 
    """
    count = 0
    word_search = []
    # pattern_grid = generate_x_pattern(word)

    # reverse the word
    reverse_word = word[::-1]
    # print(pattern_grid)

    with open(input_file, "r") as lines:
        for line in lines:
            word_search.append([letter for letter in line.strip()])

    num_rows, num_cols = len(word_search), len(word_search[0])

    # Traverse through rows and cols
    for i in range(num_rows - 2):
        for j in range(num_cols - 2):
            # Check the center of the pattern
            if word_search[i+1][j+1] == word[1]:
                found = True
                for coord in diagonal_coord:
                    diag_word = "".join(word_search[i+k][j+l] for k, l in coord)
                    print(diag_word, word, reverse_word)
                    if not (diag_word == word or diag_word == reverse_word):
                        found = False
                        break
                count += found
    return count
            

if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test1.txt'
    # input = 'test2.txt'
    word = WORD
    print(solve_2(input, word))

# The answer is 