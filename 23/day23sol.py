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


# Helper function
def get_neighbors(node, connections):
    """
    Return a set of adjacent nodes to <node> in connections.
    """
    neighbors = set()
    for pair in connections:
        if node == pair[0]:
            neighbors.add(pair[1])

        elif node == pair[1]:
            neighbors.add(pair[0])

    return neighbors

def solve_part2(input_file):
    """
    Produce the solution to part 2 of day 23 problem - LAN Party
    """
    computers, connections = read_network_map(input_file)
    

    # TODO: Implement the bron-kerbosch algorithm to build the largest LAN party
    def bron_kerbosch(R, P, X, connections=connections):
        """ 
        Build <largest> recursively using <connections> where:
        R: the maximal clique, the largest clique in.
        P: the list of all possible candidates - computers that we have not explored.
        X: the list of explored candidates - computers that are confirmed as part of or not part of 
        the current clique, but if our maximal clique changes, they can be re-explored.
        """
        # Base case: 
        # Check if R is maximal - R is maximal if we can't add anymore from P nor X
        if len(P) == 0 and len(X) == 0:
            return R

        # Initialize a copy of the largest (set) LAN party
        largest = R

        # Recursive case:
        # Iterate through each candidate with a list copy of P
        # NOTE: this is to avoid runtime issues and alter P in the next recursive steps 
        # and not in the current one
        for candidate in list(P):
            # Grab neighbors of the candidate
            neighbors = get_neighbors(candidate, connections)

            # For the next iteration, update R, P and X

            # Update R to include the current candidate
            R_new = R.union({candidate})

            # Eliminate nodes in P that are not neighbors of the current candidate
            P_new = P.intersection(neighbors)

            # Eliminiate nodes in X that are are not neighbors of the current candidate,
            # in case we need to backtrack to explored nodes from previous recursions
            X_new = X.intersection(neighbors)

            # Update the largest set based on length
            largest = max(largest, bron_kerbosch(R_new, P_new, X_new), key=len)

            # Remove candidate from P and add candidate
            P.remove(candidate)
            X.add(candidate)
    
        return largest


    lan_party = bron_kerbosch(R=set(), P=computers, X=set())
    # TODO: Form the password to the largest LAN party by:
    # 1. arrange all computers returned from the helper function in alphabetical order
    # 2. concaternate into a string, separated by commas
    password = ",".join((sorted(lan_party)))

    return password

if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))

    print(solve_part2(input))