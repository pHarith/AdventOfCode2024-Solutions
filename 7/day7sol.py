# Solution to day 7: Bridge Repair
#### SUMMARY OF TASKS ####
# 1. Read the text file line by line in the following way:
# - x: a b c where x = result, a, b, c are factors in which operations between a,b,c produces x
# - dictionary - x: [a, b, c]
# 2. Iterate through the dictionary, for each, convert into ints and perform operations in order
# 3. Loop through each possible operation (left-to-right) until a solution is found


# Part 2: We add an additional operator, || - concaternate


def parse_operations(input_file):
    """
    Given a text file, create a dictionary representing the operations sheet.

    If the input file 'text.txt' is in the format:
    x: a b
    y: c d e

    >>> parse_operations('text.txt')
    {x: [a, b], y: [c, d, e]}
    """
    # Read the file and convert the text into a board
    blank_operations = {}
    with open(input_file, "r") as file:
        for line in file:
            result, operands = line.split(':')
            blank_operations[int(result)] = [int(val) for val in operands.strip().split()]
    return blank_operations


def validate_operation(target, operands, ops):
    """
    Return True if target can be described as a combination of sums and products,
    left-to-right, of elements of operands.
    >>> validate operation(190, [19, 10]) # 190 = 19 * 10
    True
    """

    # Nested function
    def dfs_solve(index, current):
        """
        index: the index of the current operand
        current: the result after applying previous operations 
        """

        if index == len(operands): # This means we have reached the end of the operands list
            return current == target
        
        for op in ops:
            # Apply the operator between current running result and the next operand
            next_val = apply_opr(op, current, operands[index])

            if dfs_solve(index + 1, next_val): # Recursive call, return True only if we managed to hit target
                return True

    return dfs_solve(1, current=operands[0]) # call the nested function on the 2nd index (1) and first operand [0]


def apply_opr(op, a, b):
    """
    Returns a (op) b where op = +, *, ||
    """
    match op:
        case '+':
            return a + b
        case '*':
            return a * b
        case '||':
            return int(str(a) + str(b))
        case _:
            raise ValueError("Incorrect operator")

def solve(input_file, operators=['+', '*']):
    """
    Produce the solution to day 7 problem: Bridge Repair
    """
    result = 0
    operation_dict = parse_operations(input_file)
    for target, operands in operation_dict.items():
        result += target if validate_operation(target, operands, operators) else 0
    return result


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))

    # Part 2
    print(solve(input,['+', '*', '||']))