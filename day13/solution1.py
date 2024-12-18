import re

integer_pattern = re.compile("[1-9][0-9]*")


def run(lines):
    result = 0
    for machine in get_machines(lines):
        button_a, button_b, prize = machine
        press_count, cost = find_cheapest_button_presses_to_get_prize(button_a, button_b, prize)
        if cost is not None:
            print(press_count, cost)
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
            prize = tuple(int(x) for x in integer_pattern.findall(prize_line))
            yield button_a, button_b, prize


def find_cheapest_button_presses_to_get_prize(button_a, button_b, prize):
    """Evaluate a list of button presses and determine which costs the least."""
    best_press, best_press_cost = None, None
    for solution in find_button_presses_to_get_prize(button_a, button_b, prize):
        if best_press is None:
            best_press = solution
            best_press_cost = calculate_cost(solution)
        elif best_press_cost > calculate_cost(solution):
            best_press_cost = calculate_cost(solution)
            best_press = solution
    return best_press, best_press_cost


def find_button_presses_to_get_prize(button_a, button_b, prize):
    """Find all combinations of button presses that will land on the prize. 
    A button press is a pair of values indicating how many times to press the A button and how many times to press the B button."""
    x_solutions = set(solve(button_a[0], button_b[0], prize[0]))
    y_solutions = set(solve(button_a[1], button_b[1], prize[1]))
    return x_solutions.intersection(y_solutions)


def solve(a, b, z):
    """Given an equation of the form ax + by = z, find solutions for x and y between 1 and 100."""
    for x in range(1, 101):
        remainder = z - (a * x)
        if remainder % b == 0:
            y = remainder // b
            if y > 0:
                yield x, y


def calculate_cost(button_press):
    """Determine the cost of a number of button presses."""
    a_press_count, b_press_count = button_press[0], button_press[1]
    return a_press_count * 3 + b_press_count
