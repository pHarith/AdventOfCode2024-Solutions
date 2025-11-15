# Solution to day 2: Red-Nosed Reports

#### SUMMARY OF TASKS ####
# 1. Read each row line by line, separate into a list of numbers
# 2. Check that this list is descending or increasing
# 3. Check that any two adjacent element differ by 1-3
# 4. if the two condition above counts, print out the number of "safe" lists


def is_safe(report):
    """
    Given a report (a list of numbers), returns whether it is safe or not.
    A report is safe if:
    - it is gradually increasing or decreasing
    - any two adjacent element differ by 1-3
    """
    is_increasing = is_decreasing = False

    for item1, item2 in zip(report, report[1:]):
        # Check that two adjacent items are within range of 1-3 in difference
        if abs(item1-item2) not in range(1, 4):
            return False

        # Check if the list is gradually increasing or decreasing
        if (item1 > item2) and not is_increasing:
            is_decreasing = True
        elif (item1 < item2) and not is_decreasing:
            is_increasing = True
        else:
            return False
    return True


def is_safe_removal(report, removal_allowed=True):
    """
    Given a report (a list of numbers), returns whether it is safe or not.
    A report is safe if:
    - it is gradually increasing or decreasing
    - any two adjacent element differ by 1-3

    If one element can be removed from the list to fulfill these conditions,
    the report is also considered safe.

    NOTE: This algorithm uses an extremely greedy method that could be substituted by dynamic programming.
    """
    is_increasing = is_decreasing = False

    #print(report)

    for i in range(len(report)-1):
        item1, item2 = report[i], report[i+1]
        # Check that two adjacent items are within range of 1-3 in difference
        if abs(item1-item2) not in range(1, 4):
            if removal_allowed:
                return is_safe_removal(report[:i]+report[i+1:], False) or is_safe_removal(report[:i+1]+report[i+2:], False)
            return False

        # Check if the list is gradually increasing or decreasing
        if (item1 > item2) and not is_increasing:
            is_decreasing = True
        elif (item1 < item2) and not is_decreasing:
            is_increasing = True
        else:
            if removal_allowed:
                return is_safe_removal(report[:i-1]+report[i:], False) or is_safe_removal(report[:i]+report[i+1:], False) or is_safe_removal(report[:i+1]+report[i+2:], False)
            return False
    return True        



def solve_day_2(input_file):
    """
    Produce the solution to the day 2 problem - Red-Nosed Reports
    """
    safe_count = 0
    # Open input text file
    with open(input_file, "r") as reports:
        # Iterate through each line (report)
        for report in reports:
            # Extract each report into a python list
            report_lst = [int(floor) for floor in report.split()]
            # safe_count += is_safe(report_lst)
            # safe_count += is_safe_removal(report_lst)
            safe = is_safe_removal(report_lst)
            safe_count += safe
            if not safe:
                print(report_lst)
                print(safe_count)
    return safe_count


if __name__ == "__main__":
    input = 'input.txt'
    print(solve_day_2(input))

# The answer is 