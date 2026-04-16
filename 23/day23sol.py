# Solution to day 23: LAN Party
#### SUMMARY OF TASKS ####
# 1. Read the input file into a set of pairs
# 2. TODO: 
# 3. 


        
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
            connections.add((com_1, com_2))
            coms.add(com_1)
            coms.add(com_2)
    return coms, connections


def solve(input_file):
    """
    Produce the solution to the day 23 problem - LAN Party
    """
    computers, connections = read_network_map(input_file)

    return computers, connections


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))