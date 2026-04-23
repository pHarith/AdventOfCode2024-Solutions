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
            if gate not in gates:
                gates[gate] = [(input1, input2, output)]
            else:
                gates[gate].append((input1, input2, output))
    return wires, gates


def read_z_binary():
    """
    Return the binary and decimal value of the results written into
    the z wires
    """

        



def solve(input_file):
    """
    Produce the solution to the day 24 problem - Crossed Wires
    """
    # Read the wire values and logic gates
    wires, gates = read_wire_config(input_file)


    return 


if __name__ == "__main__":
    input = 'input.txt'
    input = 'test.txt'
    # input = 'smalltest.txt'
    print(solve(input))