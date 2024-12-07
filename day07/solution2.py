def run(lines):
    result = 0
    for left_side, right_side in parse_equation(lines):
        if left_side in apply_operators(right_side):
            result += left_side
    return result


def parse_equation(lines):
    for line in lines:
        split = line.split(': ')
        left_side = split[0]
        right_side = split[1].split(' ')
        left_side = int(left_side)
        right_side = [int(x) for x in right_side]
        yield left_side, right_side


def apply_operators(values):
    totals = set()
    totals.add(values.pop(0))
    while values:
        new_totals = set()
        right = values.pop(0)
        for left in totals:
            new_totals.add(left + right)
            new_totals.add(left * right)
            new_totals.add(int(f'{left}{right}'))
        totals = new_totals
    return totals
