from collections import namedtuple
import re


gate_pattern = re.compile(r"""
                            (\w{3})     # input 1
                            \s
                            (\w{2,3})   # AND, OR, XOR
                            \s
                            (\w{3})     # input 2
                            \s->\s
                            (\w{3})     # output
                            """, re.X)

Gate = namedtuple('Gate', ['input1', 'input2', 'action', 'output'])


def run(lines):
    """Run until you find four swaps. After finding a swap, update the gates and look for another."""
    gates = get_gates(lines)
    swaps = []
    while len(swaps) < 4:
        swap = find_next_swap(gates)
        swaps.append(swap)
        gates = apply_swap(swap, gates)
    return ','.join(sorted([a for b in swaps for a in b]))


def get_gates(lines) -> list[Gate]:
    """Read the gates from the input."""
    result = []
    for line in lines:
        match = gate_pattern.fullmatch(line)
        if match:
            operation = Gate(match.group(1), match.group(3), match.group(2), match.group(4))
            result.append(operation)
    return result


def find_next_swap(gates: list[Gate]) -> tuple[str, str]:
    """Run until you find something that needs to be swapped. Then calculate the needed swap and return.
    This works because the gates are implementing bitwise addition where:
    - XOR adds two bits
    - AND calculates a carry bit
    - OR combines two carry bits
    """
    a = find_gate_matching_both_inputs('x00', 'y00', 'AND', gates)
    n = 1
    while True:
        x_input, y_input = f'x{n:02}', f'y{n:02}'
        b = find_gate_matching_both_inputs(x_input, y_input, 'XOR', gates)
        if b is None:
            return find_swap(x_input, y_input, 'XOR', gates)
        c = find_gate_matching_both_inputs(a.output, b.output, 'AND', gates)
        if c is None:
            return find_swap(a.output, b.output, 'AND', gates)
        d = find_gate_matching_both_inputs(x_input, y_input, 'AND', gates)
        if d is None:
            return find_swap(x_input, y_input, 'AND', gates)
        e = find_gate_matching_both_inputs(c.output, d.output, 'OR', gates)
        if e is None:
            return find_swap(c.output, d.output, 'OR', gates)
        a = e
        n += 1


def find_gate_matching_both_inputs(input1: str, input2: str, action: str, gates: list[Gate]):
    """Search all gates looking for a gate that has the provided inputs and action. 
    input1 and input2 in the parameters can match either input1 or input2 on the gate."""
    for gate in gates:
        if gate.action == action and {input1, input2} == {gate.input1, gate.input2}:
            return gate
    return None


def find_swap(input1: str, input2: str, action: str, gates: list[Gate]):
    """Find the gate with the provided action and one of the provided inputs. The unmatched input on this gate
    tells us which output needs to be swapped."""
    match = find_gate_matching_either_input(input1, action, gates)
    if match:
        return (input2, match.input1 if match.input1 not in {input1, input2} else match.input2)
    else:
        match = find_gate_matching_either_input(input2, action, gates)
        if match:
            return (input1, match.input1 if match.input1 not in {input1, input2} else match.input2)
    return None


def find_gate_matching_either_input(input1: str, action: str, gates: list[Gate]):
    """Find a gate with the provided action where either of the gate's inputs matches the provided input1 value."""
    for gate in gates:
        if gate.action == action and input1 in {gate.input1, gate.input2}:
            return gate
    return None


def apply_swap(swap: tuple[str, str], gates: list[Gate]):
    """Rewrite the list of gates by swapping the output of the two gates indicated in swap."""
    result = [g for g in gates if g.output not in swap]
    gate1 = [g for g in gates if g.output == swap[0]][0]
    gate2 = [g for g in gates if g.output == swap[1]][0]
    result.append(Gate(gate1.input1, gate1.input2, gate1.action, gate2.output))
    result.append(Gate(gate2.input1, gate2.input2, gate2.action, gate1.output))
    return result
