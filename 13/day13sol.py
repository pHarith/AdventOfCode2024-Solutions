# Solution to day 13: Claw Contraption
#### SUMMARY OF TASKS ####
# 1. 


import math


# Define constant of A and B button cost
A_COST, B_COST = 3, 1

# Define constant of max number of button pressed
MAX_PRESS = 100

# Define position error (for part 2)
POSITION_ERROR = 10000000000000

def parse_claw_settings(input_file, pos_error):
    """
    Given a text file, returns a list all the claw settings in a tuple of (a, b, p)
    a - tuple that represents movements of button A
    b - tuple that represents movements of button B
    p - tuple that represents the coordinates of prize

    Content of text file 'sample.txt':
    Button A: X+20, Y+15
    Button B: X+30, Y+45
    Prize: X=2520, Y=2400
    >>> parse_claw_settings('sample.txt')
    [((20, 15), (30, 45), (2520, 2400))]
    """
    settings = []
    error = POSITION_ERROR if pos_error else 0
    with open(input_file, "r") as file:
        raw_settings = file.read().split('\n\n')
        for raw in raw_settings:
            x, y, z = tuple(raw.split('\n'))
            x =  tuple(int(x_val[x_val.find('+')+1:]) for x_val in x[x.find(':')+1:].split('\n')[0].split(','))
            y =  tuple(int(y_val[y_val.find('+')+1:]) for y_val in y[y.find(':')+1:].split('\n')[0].split(','))
            z =  tuple(int(z_val[z_val.find('=')+1:]) + error for z_val in z[z.find(':')+1:].split('\n')[0].split(','))
            settings.append((x, y, z))
    return settings

def find_best_cost(setting):
    """
    Given a claw machine setting (a, b, p), returns the cost of least costly path.
    """
    settingA, settingB, prize = setting
    best_cost = math.inf
    best_sol = None

    a_1, a_2 = settingA
    b_1, b_2 = settingB
    p_1, p_2 = prize

    # Our two equations are:
    # a_1 * a + b_1 * b = p_1
    # a_2 * a + b_2 * b = p_2

    # Fix a as number of times we press the A button, find the optimal number of times we can press B button to reach the solution
    for a in range(MAX_PRESS + 1): # Add 1 to count from 0 to 100
        # Calculate b from equation 1 i.e. all element of settings at index [0]
        b = (p_1 - a_1 * a) / b_1

        # Check if b would be an integer
        if b == int(b):
            
            # Check if b is within bounds
            if 0 <= b <= MAX_PRESS:
                # Check if this solution satisfies equation 2
                if a_2 * a + b_2 * b == p_2:
                    # Found a valid solution
                    cost = A_COST * a + B_COST * b
                    
                    # Update best cost if possible
                    if cost < best_cost:
                        best_cost = cost
                        best_sol = (a, b)

    # Return No solution or the best cost possible
    if best_sol is None:
        return 0
    else:
        return int(best_cost)
    
def find_best_cost_part2(setting):
    settingA, settingB, prize = setting

    a_1, a_2 = settingA
    b_1, b_2 = settingB
    p_1, p_2 = prize

    # Our two equations are:
    # a_1 * a + b_1 * b = p_1
    # a_2 * a + b_2 * b = p_2

    # Solve using direct elimination, eliminate a
    b = (a_2 * p_1 - a_1 * p_2) / (a_2 * b_1 - a_1 * b_2)
    a = (p_1 - b_1 * b) / a_1

    # print(a, b)

    if (a_1 * round(a) + b_1 * round(b) == p_1) and (a_2 * round(a) + b_2 * round(b) == p_2):
        cost = A_COST * a + B_COST * b
        return cost
    
    return 0

    

def solve(input_file):
    """
    Produce the solution to the day 13 problem - Claw Contraption
    """
    total_cost = 0
    claw_settings = parse_claw_settings(input_file, pos_error=False)

    for setting in claw_settings:
        total_cost += find_best_cost(setting)
    return total_cost

def solve_part2(input_file):
    """
    Produce the solution to part 2 of the day 13 problem - Claw Contraption
    """
    total_cost = 0
    claw_settings = parse_claw_settings(input_file, pos_error=True)
    print(claw_settings)

    for setting in claw_settings:
        total_cost += find_best_cost_part2(setting)
    return total_cost


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))
    print(solve_part2(input))