# Solution to day 1: Historian Hysteria problem

#### SUMMARY OF TASKS ####
# 1. Read a txt file of 2 columns, each columns in a list
# 2. Sort each list in ascending order
# 3. Find the absolute difference of each corresponding pairs
# 4. Sum up the values

import numpy


def read_txt_cols(input_file):
    """
    Given a .txt file, read each column into a list. 
    Return a list of all the lists.
    """
    left, right = [], []
    with open(input_file, "r") as input:
        # Code goes here
        for line in input:
            val1, val2 = line.split()
            left.append(int(val1))
            right.append(int(val2))
        return [left, right]


def solve_day_1(input_file):
    """
    Produce the solution to the day 1 problem - Historian Hysteria
    """
    cols = read_txt_cols(input_file)
    distances = []

    if cols == []:
        return -1
    
    for col in cols:
        col.sort()
    
    left, right = cols[0], cols[1]

    for i in range(len(cols[0])):
        distances.append(abs(left[i] - right[i]))

    sim_score = find_similarity_score(left, right)

    return sum(distances), sim_score


def find_similarity_score(left, right):
    """
    Return similarity score between two lists, which calculated by:

    sim_score = sum(left[i] * times_appeared_in_right)

    where i < len(left).
    """
    sim_score = 0
    for l in left:
        sim_score += l * right.count(l)
    return sim_score

    # Solve with numpy instead


if __name__ == "__main__":
    input = 'input.txt'
    print(solve_day_1(input))

# The answer is 1834060 (distances)
# The answer to part 2 is 21607792 (sim score)