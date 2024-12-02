def run(lines):
    left, right = get_lists(lines)
    result = 0
    for pair in zip(left, right):
        distance = abs(pair[0] - pair[1])
        result += distance
    return result


def get_lists(lines):
    left, right = [], []
    for line in lines:
        split = [int(x) for x in line.split()]
        left.append(split[0])
        right.append(split[1])
    left.sort()
    right.sort()
    return left, right
