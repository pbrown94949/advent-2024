from collections import defaultdict
from itertools import combinations


def run(lines):
    size = len(lines[0])
    antennas = get_antennas(lines)
    antinodes = set()
    for nodes in antennas.values():
        for node1, node2 in combinations(nodes, 2):
            antinodes.update(get_antinodes(node1, node2, size))
    return len(antinodes)


def get_antennas(lines):
    result = defaultdict(set)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char != '.':
                result[char].add((row, col))
    return result


def get_antinodes(node1, node2, size):
    difference = subtract(node1, node2)
    result = set()
    node = node1
    while on_map(node, size):
        result.add(node)
        node = add(node, difference)
    node = node1
    while on_map(node, size):
        result.add(node)
        node = subtract(node, difference)
    return result


def on_map(node, size):
    if node[0] < 0 or node[1] < 0:
        return False
    return node[0] < size and node[1] < size


def add(node1, node2):
    return (node1[0] + node2[0], node1[1] + node2[1])


def subtract(node1, node2):
    return (node1[0] - node2[0], node1[1] - node2[1])
