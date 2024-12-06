from itertools import combinations
import re

ordering_rules_pattern = re.compile(r'([1-9][1-9])\|([1-9][1-9])')


def run(lines):
    result = 0
    rules = get_ordering_rules(lines)
    updates = get_updates(lines)
    for update in updates:
        if is_in_correct_order(rules, update):
            middle_item = update[len(update) // 2]
            result += middle_item
    return result


def get_ordering_rules(lines):
    result = set()
    for line in lines:
        if match := ordering_rules_pattern.match(line):
            a, b = int(match.group(1)), int(match.group(2))
            result.add((a, b))
    return result


def get_updates(lines):
    result = []
    for line in lines:
        if ',' in line:
            update = tuple(int(x) for x in line.split(','))
            result.append(update)
    return result


def is_in_correct_order(rules, update):
    for pair in combinations(update, 2):
        reversed_pair = (pair[1], pair[0])
        if reversed_pair in rules:
            return False
    return True
