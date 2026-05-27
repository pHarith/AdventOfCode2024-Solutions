# Solution to day 24: Crossed Wires
from collections import defaultdict

def read_wire_config(input_file):
    """
    Return two dictionaries from reading the input file:
    - First dictionary stores the name of wires as keys and their values are 0 or 1
    - Second dictionary stores the name of gates as keys and their values are tuples of 3 wires, (input1, input2, output)
    """
    wires = {}
    gates = {}

    with open(input_file, "r") as wire_config:
        wire_info, gates_info = wire_config.read().split('\n\n') # split the file into two sections

        for line in wire_info.split('\n'):
            wire, value = line.strip().split(':')
            wires[wire.strip()] = int(value.strip())

        for line in gates_info.split('\n'):
            inputs, output = line.strip().split('->')

            input1, gate, input2 = inputs.strip().split()
            
            gates[output.strip()] = (input1.strip(), input2.strip(), gate.strip())
            
    return wires, gates

def extract_binary_from_wires(wires, target):
    """
    Given a dictionary of wires, extract the values of any wire starting with <target>
    and return the binary value string of the extracted values.
    """
    
    # Filter out the desired wires into a list and get them sorted
    target_wires_sorted = sorted([wire for wire in wires if wire.startswith(target)])

    try:
        binary_str = "".join([str(wires[wire]) for wire in target_wires_sorted])
    except ValueError:
        raise ValueError("Incorrect Input.")

    # NOTE: the binary string is in reverse, so return it in reversed
    return binary_str[::-1]

def compute_gates(wires, gates):

    # Helper function to compute gate operations (tuples)
    def gate_operation(input1, input2, operation):
        match operation:
            case 'AND':
                return wires[input1] & wires[input2]
            case 'OR':
                return wires[input1] | wires[input2]
            case 'XOR':
                return wires[input1] ^ wires[input2]
            case _:
                raise ValueError(f"Unknown operation: {operation}")

    # Make a shallow copy of all gates operations
    unsolved_gates = gates.copy()

    # Iterate until there are no more unsolved gates
    while unsolved_gates:
        # Make a secondary shallow copy to avoid unintended Runtime Errors
        for output_wire in unsolved_gates.copy():
            input1, input2, operation = unsolved_gates[output_wire]
            if input1 in wires and input2 in wires:
                wires[output_wire] = gate_operation(input1, input2, operation)
                unsolved_gates.pop(output_wire, None)
    return


def solve(input_file):
    """
    Produce the solution to the day 24 problem - Crossed Wires
    """
    # Read the wire values and logic gates
    wires, gates = read_wire_config(input_file)
    
    compute_gates(wires, gates)

    binary_str = extract_binary_from_wires(wires, target='z')

    return int(binary_str, 2)



#### PART 2 ####
# NOTE: The adder function is not used for the solution, but is helpful 
# in breaking down the logic and the flow of the gates operations
# when performing bit addition
def adder(input1, input2, carry_in_bit):
    """
    A function to perform addition between two binary input bits, 
    including the carry bit from previous digits.

    Return the sum bit and the carry bit from the operation.
    """
    partial_sum = input1 ^ input2
    full_sum = partial_sum ^ carry_in_bit
    partial_carry_out = input1 & input2
    full_carry_out = partial_sum & carry_in_bit
    true_carry_out = partial_carry_out | full_carry_out
    return full_sum, true_carry_out


# Helper function
def find_swapped_wires(gates):

    swapped = set()
    
    # Helper function to build a dictionary which uses inputs as key and gate tuples as values
    def build_inputs_to_gate(gates):
        """
        Build a dictionary from <gates> where the keys are wires, with a list of corresponding
        gates as values.
        """
        input_gates = defaultdict(list)

        for output, (input1, input2, operation) in gates.items():
            input_gates[input1].append((input2, output, operation))
            input_gates[input2].append((input1, output, operation))
        return input_gates
    
    # Build a dictionary to track which wire is used in which gates
    inputs_to_gate = build_inputs_to_gate(gates)

    # Note the final z wire that stores a carry out value (not sum)
    z_wires = [wire for wire in gates if wire.startswith('z')]
    last_zwire = sorted(z_wires)[-1]

    # Iterate through the gates dictionary
    for output, (input1, input2, operation) in gates.items():

        # Check if a pair of input is x, y pair
        is_xy_pair = (input1.startswith('x') and input2.startswith('y')) \
                    or (input2.startswith('x') and input1.startswith('y'))
        
        # Case 1: Partial Sum
        # partial_sum = 
        # Partial Sum's output should feed into 1 XOR operation (full sum)
        # and 1 AND operation (full carry)
        if operation == 'XOR' and is_xy_pair:
            set_op = {op for (_, _, op) in inputs_to_gate[output]}
            if set_op and set_op != {'XOR', 'AND'}:
                swapped.add(output)
        
        # Case 2: Partial Carry
        if operation == 'AND' and is_xy_pair:
            set_op = {op for (_, _, op) in inputs_to_gate[output]}
            if set_op and set_op != {'OR'}:
                is_bit_0 = input1 == 'x00' and input2 == 'y00' \
                        or input2 == 'x00' and input1 == 'y00'
                if not is_bit_0 or set_op != {'XOR', 'AND'}:
                    swapped.add(output)

        # Case 3: Full Sum
        # Output must be a z wire, and since full_sum = partial_sum ^ carry_in,
        # the inputs are non x, y wires (intermediate wires)
        if operation == "XOR" and not is_xy_pair:
            if not output.startswith('z'):
                swapped.add(output)

        # Case 4: Full Carry
        # full_carry = partial_sum & carry_in
        # inputs are non x, y wires (intermediate) and feeds into 'OR' (true carry)
        if operation == "AND" and not is_xy_pair:
            set_op = {op for (_, _, op) in inputs_to_gate[output]}
            if set_op and set_op != {'OR'}:
                swapped.add(output)

        # Backdoor Case: Check z wires that are produced faulty
        # The last Z wire is produced from an OR operation as it has to store
        # any carry outs from the previous operation
        if output.startswith('z') and operation != 'XOR' and output != last_zwire:
            swapped.add(output)
        
    return swapped

def solve_part2(input_file):
    """
    Produce the solution to part 2 of the day 24 problem - Crossed Wires
    """
    # Read the wire values and logic gates
    wires, gates = read_wire_config(input_file)

    swapped = find_swapped_wires(gates)
    return ",".join(sorted(swapped))


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    # input = 'smalltest.txt'
    print(solve(input))
    print(solve_part2(input))