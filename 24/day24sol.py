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
            wires[wire] = int(value)

        for line in gates_info.split('\n'):
            inputs, output = line.strip().split('->')

            input1, gate, input2 = inputs.strip().split(' ')
            
            # NOTE: changed gates structure by using output wire as keys to ensure uniqueness
            # NOTE: also helps with later helper function as the values are immutable so shallow copy works
            gates[output] = (input1, input2, gate)
            
    return wires, gates


def read_z_binary():
    """
    Return the binary and decimal value of the results written into
    the z wires
    """


def compute_gates(wires, gates):
    # TODO: implement function to loop over <gates>, while checking preexisting wires until there are no more gates operation to perform

    # Make a shallow copy of all gates operations
    unsolved_gates = gates.copy()

    while not unsolved_gates:
        # Make a secondary shallow copy to avoid unintended Runtime Errors
        for output_wire in unsolved_gates.copy():
            input1, input2, operation = unsolved_gates[output_wire]
            if input1 in wires and input2 in wires:
                wires[output_wire] = gate_operation(input1, input2, operation)
                unsolved_gates.pop(output_wire, None)
    return

def gate_operation(input1, input2, operation):
    # TODO: implement the logic of gate operations
    match operation:
        case 'AND':
            return
        case 'OR':
            return
        case 'XOR':
            return 
        case _:
            return -1


def solve(input_file):
    """
    Produce the solution to the day 24 problem - Crossed Wires
    """
    # Read the wire values and logic gates
    wires, gates = read_wire_config(input_file)

    # TODO: Function to iterate through the program's gates configuration
    # write values to existing or new wires



    return 


if __name__ == "__main__":
    input = 'input.txt'
    input = 'test.txt'
    # input = 'smalltest.txt'
    print(solve(input))