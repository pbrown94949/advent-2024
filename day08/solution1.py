from collections import defaultdict
from itertools import combinations


def run(lines):
    size = len(lines[0])
    antennas = get_antennas(lines)
    antinodes = set()
    for frequency, nodes in antennas.items():
        for node1, node2 in combinations(nodes, 2):
            x = get_antinodes(node1, node2)
            antinodes.update(x)
    antinodes = [x for x in antinodes if on_map(x, size)]
    return len(antinodes)


def get_antennas(lines):
    result = defaultdict(set)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char != '.':
                result[char].add((row, col))
    return result


def get_antinodes(node1, node2):
    difference = subtract(node1, node2)
    result = set()
    result.add(add(node1, difference))
    result.add(add(node2, difference))
    result.add(subtract(node1, difference))
    result.add(subtract(node2, difference))
    result.remove(node1)
    result.remove(node2)
    return result


def add(node1, node2):
    return (node1[0] + node2[0], node1[1] + node2[1])


def subtract(node1, node2):
    return (node1[0] - node2[0], node1[1] - node2[1])


def on_map(node, size):
    if node[0] < 0 or node[1] < 0:
        return False
    return node[0] < size and node[1] < size
