# Solution to day 23: LAN Party
#### SUMMARY OF TASKS ####
# 1. Read the input file into a set of pairs
# 2. TODO: 
# 3. 

from itertools import combinations

        
def read_network_map(input_file):
    """
    Given input text file of <com-a>-<com-b> lines, return a set of unique computers
    and a set of unique connections.
    """
    coms = set()
    connections = set()
    with open(input_file, "r") as network_map:
        for pair in network_map:
            com_1, com_2 = pair.strip().split('-')
            connections.add((min(com_1, com_2), max(com_1, com_2)))
            coms.add(com_1)
            coms.add(com_2)
    return coms, connections


def solve(input_file):
    """
    Produce the solution to the day 23 problem - LAN Party
    """
    computers, connections = read_network_map(input_file)

    valid_trios = set()

    for trio in combinations(computers, 3):
        # Check that any two pairs in a trio is connected
        if all(tuple(sorted(pair)) in connections for pair in combinations(trio, 2)):
            for comp in trio:
                if comp.startswith('t'):    # Check for computers that starts with 't'
                    valid_trios.add(trio)

    return len(valid_trios)


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))