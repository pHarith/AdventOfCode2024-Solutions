# Solution to day 19: Linen Layout
#### SUMMARY OF TASKS ####
# 1. Read the towel stripes and desired arrangements into two separate list.
# 2. Iterate through each arrangement and check if any combinations of stripes can reproduce it.
# 3. Increment and returnt he number of possible combinations.


        
def read_towel_designs(input_file):
    """
    Read and return a list of available towel stripe patterns and a list of desired arrangement design of towels.
    
    :param input_file: a file containing two strings separated by a newspace. First string represent towel stripe designs while the second string are patterns representing the desired arrangement of towels for display.
    """
    with open(input_file, "r") as towel_file:
        pattern_str, design_str = towel_file.read().split('\n\n')
        patterns = [pattern.strip() for pattern in pattern_str.strip().split(',')]
        designs = design_str.split('\n')
        return patterns, designs

def can_match_pattern(design, patterns):
    """
    Check if a given <design> can be matched from any combination from <patterns>
    
    :param patterns: A list of strings, with each letter representing a color.
    :param design: A longer string of letters, each representing a color.
    """

    design_len = len(design)

    # Inner help function
    def match_from_index(index):
        """
        Match a design starting from <index>.
        """

        # Base Case:
        if index == design_len:
            return True # We matched to very end
        
        # Recursive Case
        for pattern in patterns:
            # Check if the design from index starts with one of the patterns
            if design[index:].startswith(pattern):
                new_index = index + len(pattern)
                if match_from_index(new_index):
                    return True  # Return recursive call

        # Failed to match any
        return False

    return match_from_index(0)

def count_possible_designs(patterns, designs):
    possible_designs = 0

    for design in designs:
        possible_designs += can_match_pattern(design, patterns)
    
    return possible_designs


def solve(input_file):
    """
    Produce the solution to the day 19 problem - Linen Layout
    """
    patterns, designs = read_towel_designs(input_file)
    return count_possible_designs(patterns, designs)


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))