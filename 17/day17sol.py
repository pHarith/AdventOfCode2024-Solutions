# Solution to day 17: Chronospatial Computer
#### SUMMARY OF TASKS ####
# 1. 

def read_register(input_file):
    """
    Read 3-bit computer and return the values of registers and programs
    """
    registers = {}
    programs = []

    with open(input_file, "r") as computer:
        for instruction in computer:
            if instruction == '\n':
                continue
            type, values = instruction.strip('\n').split(":")
            if "Register" in type:
                register_key = type.split( )[1]
                registers[register_key] = int(values)
            elif "Program" in type:
                programs = [int(val) for val in values.split(',')]
    return registers, programs


def run_program(registers, programs):

    output = []

    # Initialize the instruction pointer as i
    i = 0

    def handle_combo_operand(operand):
        if operand <= 3:
            return operand
        if operand == 4:
            return registers['A']
        if operand == 5:
            return registers['B']
        if operand == 6:
            return registers['C']
        if operand == 7:
            raise ValueError("Operand 7 is reserved and should not appear in regular programs.")

    while i + 1 < len(programs):
        opcode, operand = programs[i], programs[i+1]
        match opcode:
            case 0: # adv instruction
                # A = A // (2 ^ combo_operand)
                registers['A'] = registers['A'] // (2 ** handle_combo_operand(operand))
            case 1: # bxl instruction
                # B = B ^ literal_operand
                registers['B'] = registers['B'] ^ operand 
            case 2: # bst instruction
                # B = combo_operand % 8
                registers['B'] = handle_combo_operand(operand) % 8
            case 3: # jnx instruction
                # Jump to operand if A != 0
                if registers['A'] == 0:
                    # do nothing
                    pass
                else:
                    i = operand
                    continue
            case 4: # bxc instruction
                registers['B'] = registers['B'] ^ registers['C']
            case 5: # out instruction
                output.append(handle_combo_operand(operand) % 8)
            case 6: # bdv instruction
                # B = A // (2 ^ combo_operand)
                registers['B'] = registers['A'] // (2 ** handle_combo_operand(operand))
            case 7: # cdv instruction
                # C = A // (2 ^ combo_operand)
                registers['C'] = registers['A'] // (2 ** handle_combo_operand(operand))
        i += 2
        
    return output



def solve(input_file):
    """
    Produce the solution to the day 17 problem - Chronospatial Computer
    """
    registers, programs = read_register(input_file)

    output = run_program(registers, programs)

    new_A = find_regA(programs)

    # registers['A'] = new_A
    # output_2 = run_program(registers, programs)

    return ",".join(str(out) for out in output), new_A


# Code for part 2
def find_regA(program):
    '''
    Find the suitable value in register A so that the solution produces the same output as program 1
    where <program> is a list of instructions, including opcodes and operands.
    '''
    # NOTE: We use backtracking, since the computer processes data in 3-bit chunks.
    # A is the only register with a starting value. A gets smaller whenever we arrive at opcode = 0, by a factor of 2.
    # Registers B and C start from 0, and becomes a factor of some version of A if non zero.
    # opcode = 5 produces output via % 8 operation, using either a 2, 4, 8 or one of the registers. Each output is a 3-bit.
    # So using output + 8 * <number> brings us to a factor of A, potentially a version A at some point.
    # Through enough iteration, we can backtrack to a potential candidate of A to produce all the desired output.

    # Initialize a length for the program
    prog_length = len(program)

    # Initialize an empty register
    registers = {'A': 0, 'B': 0, 'C': 0}

    # Initialize range of candidates (begin with 3 bits)
    candidates = range(8)
    
    for target_length in range(1, prog_length + 1):
        new_candidates = []
        for candidate in candidates:
            registers['A'] = candidate
            # Run the program on candidate
            out = run_program(registers, program)
            if program[-target_length:] == out[-target_length:]:    # Check if the output matches the original program up to target_length, starting from the last element
                if target_length == prog_length:
                    # Stop expanding the list of possible candidates of A as we have reached target length
                    new_candidates.append(candidate)
                else:
                    for digit in range(8):
                        # Generate new candidates to be tested and produce the subsequent element of target program
                        new_candidates.append(8 * candidate + digit)
        candidates = new_candidates
    return min(candidates)  # Return smallest valid A


if __name__ == "__main__":
    input = 'input.txt'
    #input = 'test.txt'
    #input = 'test2.txt'
    print(solve(input))