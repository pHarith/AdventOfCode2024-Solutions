# Solution to day 5: Print Queue

#### SUMMARY OF TASKS ####
# PART 1:
# 1. Read the input file and read the rules (X|Y)
# 2. 

# PART 2:
# 1. 
# 2. 


def parse_print_manual(input_string):
    # 
    rule_dict = {}

    #
    rules_str, queues_str = input_string.split("\n\n", 1)
    
    #
    rules = rules_str.split('\n')
    queues = [queue.split(',') for queue in queues_str.strip().split('\n')]

    # 
    for rule in rules:
        value, key = rule.split('|')
        if key in rule_dict:
            rule_dict[key].append(value)
        else:
            rule_dict[key] = [value]
    return rule_dict, queues


def reorder_queue(rules, queue):
    # NOTE: solution would not work if there is a cycle within the rules 
    i = 0
    while i < len(queue):
        swapped = False
        if queue[i] in rules:
            for element in rules[queue[i]]:
                if element in queue:
                    found_index = queue.index(element)
                    if found_index > i:
                        swapped = True
                        queue[i], queue[found_index] = queue[found_index], queue[i]
        if not swapped:
            i += 1


def is_valid_queue(rules, queue):
    for i in range(len(queue)):
        if queue[i] in rules:
            for element in rules[queue[i]]:
                if element in queue and queue.index(element) > i:
                    return False
    return True

def solve(input_file):
    """
    Produce the solution to the day 4 problem - 
    """
    sum = 0
    with open(input_file, "r") as file:
        manual_string = file.read()
        rules_dict, print_queues = parse_print_manual(manual_string)
    
        for queue in print_queues:
            # reorder_queue(rules_dict, queue)
            if is_valid_queue(rules_dict, queue):
                sum += int(queue[len(queue)//2])
    return sum

def solve_2(input_file):
    """
    Produce the solution to the day 5 problem - 
    """
    sum = 0
    with open(input_file, "r") as file:
        manual_string = file.read()
        rules_dict, print_queues = parse_print_manual(manual_string)

        print(rules_dict)
    
        for queue in print_queues:
            # reorder_queue(rules_dict, queue)
            if not is_valid_queue(rules_dict, queue):
                print(queue)
                reorder_queue(rules_dict, queue)
                print(queue)
                sum += int(queue[len(queue)//2])
    return sum


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    print(solve(input))
    print(solve_2(input))

