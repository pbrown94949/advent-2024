import math
import re

integer_pattern = re.compile("[1-9][0-9]*")


def run(lines):
    result = 0
    for machine in get_machines(lines):
        a_press_count, b_press_count = get_button_press_counts(machine)
        if a_press_count is not None:
            cost = calculate_cost(a_press_count, b_press_count)
            result += cost
    return result


def get_machines(lines):
    """Read the input and extract all machines. A machine consists of two buttons (A and B) and a prize.
    Each button consists of an x-offset and a y-offset. Each prize is a location in an x, y plane. """
    for idx, line in enumerate(lines):
        if line.startswith("Button A"):
            button_a_line = line
            button_b_line = lines[idx + 1]
            prize_line = lines[idx + 2]
            button_a = tuple(int(x) for x in integer_pattern.findall(button_a_line))
            button_b = tuple(int(x) for x in integer_pattern.findall(button_b_line))
            prize = tuple(int(x) + 10000000000000 for x in integer_pattern.findall(prize_line))
            yield button_a, button_b, prize


def get_button_press_counts(machine):
    """For a given machine, determine how many times the A and B buttons need to be pressed to reach the prize.
    Convert the machine into two diophantine equations and solve them."""
    button_a, button_b, prize = machine
    de1 = button_a[0], button_b[0], prize[0]
    de2 = button_a[1], button_b[1], prize[1]
    a_press_count, b_press_count = solve(de1, de2)
    return a_press_count, b_press_count


def solve(de1, de2):
    """Solve a pair of diophantine equations for x and y."""
    a1, b1, c1 = de1
    a2, b2, c2 = de2
    d1 = gcd(a1, b1)
    if c1 % d1 != 0:
        return None, None
    d2 = gcd(a2, b2)
    if c2 % d2 != 0:
        return None, None
    n, d = b2 * c1 - b1 * c2, a1 * b2 - a2 * b1
    # We only want integer solutions. There has to be a more mathmatical way to do this.
    if n % d != 0:
        return None, None
    x = n // d
    n, d = a2 * c1 - a1 * c2, a2 * b1 - a1 * b2
    if n % d != 0:
        return None, None
    y = n // d
    return x, y


def gcd(a, b):
    """Calculate the greatest common divisor of two numbers."""
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


def calculate_cost(a_press_count, b_press_count):
    """Determine the cost of a number of button presses."""
    return a_press_count * 3 + b_press_count
