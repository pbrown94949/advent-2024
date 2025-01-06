from collections import deque


def run(lines):
    patterns = get_patterns(lines)
    designs = get_designs(lines)
    result = 0
    for design in designs:
        if is_design_possible(design, patterns):
            result += 1
    return result


def get_patterns(lines):
    return set(lines[0].split(', '))


def get_designs(lines):
    return list(lines[2:])


def is_design_possible(design: str, patterns: set[str]):
    already_seen, current_indexes = set(), set([0])
    while current_indexes:
        next_indexes = set()
        for index in current_indexes:
            for pattern in patterns:
                if design.startswith(pattern, index):
                    next_index = index + len(pattern)
                    if next_index == len(design):
                        return True
                    next_indexes.add(next_index)
        already_seen.update(current_indexes)
        current_indexes = next_indexes - already_seen
    return False
