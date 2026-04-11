# Solution to day 22: Monkey Market

PRUNE_CONST = 16777216

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

def solve(input_file):
    """
    Produce the solution to the day 22 problem - Monkey Market
    """
    secret_nums = read_input(input_file)
    for i in range(len(secret_nums)):
        for _ in range(REPEAT_CONST):
            secret_nums[i] = evolve(secret_nums[i])

    return sum(secret_nums)

def solve_part2(input_file):
    """
    Produce the solution to part 2 of the day 22 problem - Monkey Market
    """
    secret_nums = read_input(input_file)
    for i in range(len(secret_nums)):
        for _ in range(REPEAT_CONST):
            secret_nums[i] = evolve(secret_nums[i])

            # Extract the last digit
            last_digit = secret_nums[i] % 10


    return sum(secret_nums)


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))