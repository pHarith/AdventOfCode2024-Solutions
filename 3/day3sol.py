# Solution to day 3: Mull It Over

#### SUMMARY OF TASKS ####
# 1. Read each line, identify those with valid syntax using regex
# 2. If valid, extract them into a list and then run eval() on each expression
# 3. Sum up the values returned


# Part 2: Scan for do() and don't()
# 1. do() = mul() instructions should be evaluated
# 2. don't() = mul() instructions should not be evaluated


import re

# Raw string that matches for mul(x,y) operation
mul_regex = r"\bmul\(\d+,\d+\)"


# Raw string that matches do() and don't() operations
dont_regex = r"don't\(\)"
do_regex = r"\bdo\(\)"

def find_valid_mul(line):
    """
    Given a line of text, extract valid mul(x,y) operations and return a list of these operations.
    """
    return re.findall(mul_regex, line)

def find_valid_opr(line):
    """
    Given a line of text, extract valid mul(x,y), do() and don't() operations and return a list of these operations.
    """
    return re.compile("(%s|%s|%s)" % (mul_regex, do_regex, dont_regex)).findall(line)
    

# Hardcoded multiplication function to call eval() on
def mul(a, b):
    return a*b


def solve_1(input_file):
    """
    Produce the solution to the day 3 problem - Mull It Over
    """
    sum = 0
    with open(input_file, "r") as memory:
        for line in memory:
            # print(line)
            # Extract all valid mul() operations in the line
            opr_lst = find_valid_mul(line)
            # print(opr_lst)
            for opr in opr_lst:
                # Evaluate valid mul operations and add the values to sum
                sum += eval(opr)
    return sum


def solve_2(input_file):
    """
    Produce the solution to the day 3 problem - Mull It Over
    """
    sum, can_do = 0, True
    with open(input_file, "r") as memory:
        for line in memory:
            # print(line)
            opr_lst = find_valid_opr(line)
            # print(opr_lst)
            for opr in opr_lst:
                # Match for don't()
                if re.match(dont_regex, opr):
                    can_do = False  # Disable mul() 

                # Match for do()
                elif re.match(do_regex, opr):
                    can_do = True   # Enable mul()
                
                # Check if a valid mul() operation
                # and is enabled
                if re.match(mul_regex, opr) and can_do:
                    sum += eval(opr)
    return sum


if __name__ == "__main__":
    input = 'input.txt'
    print(solve_1(input))
    print(solve_2(input))