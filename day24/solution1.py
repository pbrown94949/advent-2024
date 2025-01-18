from collections import deque, namedtuple
import re


initial_value_pattern = re.compile(r"""
                                   ([xy][0-9][0-9])   # register
                                   :\s
                                   ([01])             # value
                                   """, re.X)

operation_pattern = re.compile(r"""
                               (\w{3})     # source 1
                               \s
                               (\w{2,3})   # AND, OR, XOR
                               \s
                               (\w{3})     # source 2
                               \s->\s
                               (\w{3})     # register           
                               """, re.X)

Operation = namedtuple('Operation', ['source1', 'action', 'source2', 'target'])


def run(lines):
    registers = {register: None for register in get_all_registers(lines)}
    for register, value in get_initial_values(lines):
        registers[register] = value
    operations = get_operations(lines)
    perform_operations(registers, operations)
    return convert_to_number(registers)


def get_all_registers(lines) -> set[str]:
    """Read the input and get the names of all the registers."""
    result = set()
    for line in lines:
        if match := initial_value_pattern.fullmatch(line):
            result.add(match.group(1))
        elif match := operation_pattern.fullmatch(line):
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


def get_operations(lines) -> list[Operation]:
    """Read the operations from the input."""
    result = []
    for line in lines:
        match = operation_pattern.fullmatch(line)
        if match:
            operation = Operation(match.group(1), match.group(2), match.group(3), match.group(4))
            result.append(operation)
    return result


def perform_operations(registers: dict[str, bool], operations: list[Operation]):
    """For each operation, try to execute it. If either of its inputs is unavailable, put it 
    back on the queue and try again later. 
    Run until all operations are complete. I tried exiting early when all z-registers were set, 
    but it was the same speed.
    """
    q = deque(operations)
    while q:
        operation = q.popleft()
        source1, source2 = registers[operation.source1], registers[operation.source2]
        if source1 is None or source2 is None:
            q.append(operation)
        else:
            registers[operation.target] = perform_operation(source1, operation.action, source2)


def perform_operation(b1: bool, operation: str, b2: bool):
    """Perform whatever boolean operation is requested"""
    if operation == 'AND':
        return b1 and b2
    elif operation == 'OR':
        return b1 or b2
    else:
        return b1 != b2


def convert_to_number(registers: dict[str, bool]):
    """Looking at the z registers in order, determine what integer they represent."""
    result = 0
    z_registers = [k for k in registers if k.startswith('z')]
    for power, register in enumerate(sorted(z_registers)):
        if registers[register]:
            result += (2 ** power)
    return result