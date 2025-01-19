from collections import deque, namedtuple
import re


initial_value_pattern = re.compile(r"""
                                   ([xy][0-9][0-9])   # register
                                   :\s
                                   ([01])             # value
                                   """, re.X)

gate_pattern = re.compile(r"""
                               (\w{3})     # input 1
                               \s
                               (\w{2,3})   # AND, OR, XOR
                               \s
                               (\w{3})     # input 2
                               \s->\s
                               (\w{3})     # output
                               """, re.X)

Gate = namedtuple('Gate', ['input1', 'action', 'input2', 'output'])


def run(lines):
    registers = {register: None for register in get_all_registers(lines)}
    for register, value in get_initial_values(lines):
        registers[register] = value
    gates = get_gates(lines)
    perform_operations(registers, gates)
    return convert_to_number(registers)


def get_all_registers(lines) -> set[str]:
    """Read the input and get the names of all the registers."""
    result = set()
    for line in lines:
        if match := initial_value_pattern.fullmatch(line):
            result.add(match.group(1))
        elif match := gate_pattern.fullmatch(line):
            result.add(match.group(1))
            result.add(match.group(3))
            result.add(match.group(4))
    return result


def get_initial_values(lines) -> list[tuple[str, bool]]:
    """Return a list of the registers that have initial values and what that value is."""
    result = []
    for line in lines:
        match = initial_value_pattern.fullmatch(line)
        if match:
            register = match.group(1)
            value = match.group(2) == '1'
            result.append((register, value))
    return result


def get_gates(lines) -> list[Gate]:
    """Read the gates from the input."""
    result = []
    for line in lines:
        match = gate_pattern.fullmatch(line)
        if match:
            operation = Gate(match.group(1), match.group(2), match.group(3), match.group(4))
            result.append(operation)
    return result


def perform_operations(registers: dict[str, bool], gates: list[Gate]):
    """For each operation, try to execute it. If either of its inputs is unavailable, put it 
    back on the queue and try again later. 
    Run until all operations are complete. I tried exiting early when all z-registers were set, 
    but it was the same speed.
    """
    q = deque(gates)
    while q:
        gate = q.popleft()
        input1, input2 = registers[gate.input1], registers[gate.input2]
        if input1 is None or input2 is None:
            q.append(gate)
        else:
            registers[gate.output] = perform_operation(input1, gate.action, input2)


def perform_operation(input1: bool, operation: str, input2: bool):
    """Perform whatever boolean operation is requested"""
    if operation == 'AND':
        return input1 and input2
    elif operation == 'OR':
        return input1 or input2
    else:
        return input1 != input2


def convert_to_number(registers: dict[str, bool]):
    """Looking at the z registers in order, determine what integer they represent."""
    result = 0
    z_registers = [k for k in registers if k.startswith('z')]
    for power, register in enumerate(sorted(z_registers)):
        if registers[register]:
            result += (2 ** power)
    return result