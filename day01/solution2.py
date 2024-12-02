from collections import defaultdict


def run(lines):
    left, right = get_lists(lines)
    counts = count_occurrences(right)
    result = 0
    for item in left:
        result += (item * counts[item])
    return result


def get_lists(lines):
    line: str
    left, right = [], []
    for line in lines:
        split = [int(x) for x in line.split()]
        left.append(split[0])
        right.append(split[1])
    left.sort()
    right.sort()
    return left, right


def count_occurrences(list):
    result = defaultdict(int)
    for item in list:
        result[item] += 1
    return result
