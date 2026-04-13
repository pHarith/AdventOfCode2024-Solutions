# Solution to day 22: Monkey Market

# Constant used for the pruning function.
PRUNE_CONST = 16777216

# Constant for how many times each buyer evolves their secret number/price
REPEAT_CONST = 2000

def mix(num, to_mix):
    """
    Mix the numbers according to the problem's description.
    """        
    return num ^ to_mix

def prune(num):
    """
    Prune the number <num> according to the problem's description.
    """        
    return num % PRUNE_CONST

def evolve(num):
    """
    Evolves the number <num> according to the problem's description.
    """        
    first = prune(mix(num, num * 64))
    second = prune(mix(first, first // 32))
    final = prune(mix(second, second * 2048))
    return final

def read_input(file):
    with open(file, "r") as num_file:
        return [int(line.strip()) for line in num_file]

def solve(input_file, num_repeat=REPEAT_CONST):
    """
    Produce the solution to the day 22 problem - Monkey Market
    """
    secret_nums = read_input(input_file)
    for i in range(len(secret_nums)):
        for _ in range(num_repeat):
            # Evolve the scret number/price
            secret_nums[i] = evolve(secret_nums[i])

    return sum(secret_nums)


def solve_part2(input_file, num_repeat=REPEAT_CONST):
    """
    Produce the solution to part 2 of the day 22 problem - Monkey Market
    """
    # Initialize a dictionary that stores unique 4 changes seqeuences and sums of prices from
    # every buyer/secret number
    sum_sequence_to_price = {}

    secret_nums = read_input(input_file)

    for i in range(len(secret_nums)):
        
        # Initialize the last digit of the secret number (the current price)
        curr_price = secret_nums[i] % 10

        # Initial a list to keep track of changes
        changes = []

        # Initialize a local dictionary to keep track of unique sequences of 4 changes to the final price
        # for a single buyer/secret number
        sequence_to_price = {}

        for _ in range(num_repeat):
            # Evolve the scret number/price
            secret_nums[i] = evolve(secret_nums[i])

            new_price = secret_nums[i] % 10

            # Compute the change between the extracted last digits of the new and old secret numbers
            change = new_price - curr_price

            changes.append(change)

            if len(changes) >= 4:
                # Extract the most recent seqeunce of 4 changes
                sequence = tuple(changes[-4:])

                # Store a valid sequence of changes with the final price as key, value pairs
                if sequence not in sequence_to_price:
                    sequence_to_price[sequence] = new_price

            # Update the current price
            curr_price = new_price

        # Update the larger dictionary
        for sequence, price in sequence_to_price.items():
            if sequence in sum_sequence_to_price:
                sum_sequence_to_price[sequence] += price
            else:
                sum_sequence_to_price[sequence] = price

    # Return the highest summed price across all sequences
    return max(sum_sequence_to_price.values())


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))
    print(solve_part2(input))
