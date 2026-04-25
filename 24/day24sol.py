# Solution to day 24: Crossed Wires


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


if __name__ == "__main__":
    input = 'input.txt'
    # input = 'test.txt'
    # input = 'smalltest.txt'
    print(solve(input))