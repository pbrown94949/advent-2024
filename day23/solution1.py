from __future__ import annotations
from collections import deque


class Node:

    def __init__(self, value):
        self._value = value
        self._neighbors = set()

    def __repr__(self):
        return f'Node(value={self._value})'

    @property
    def value(self):
        return self._value

    def link(self, node: Node):
        self._link(node)
        node._link(self)

    def _link(self, node: Node):
        self._neighbors.add(node)

    def get_neighbors(self):
        return self._neighbors


def run(lines):
    computers = get_network(lines)
    cycles = find_all_cycles(computers)
    result = 0
    for cycle in cycles:
        if any([computer.startswith('t') for computer in cycle]):
            result += 1
    return result


def get_network(lines):
    nodes = {}
    for line in lines:
        computer1, computer2 = line.split('-')
        if computer1 not in nodes:
            nodes[computer1] = Node(computer1)
        if computer2 not in nodes:
            nodes[computer2] = Node(computer2)
        nodes[computer1].link(nodes[computer2])
    return nodes.values()


def find_all_cycles(computers):
    """Iterate over all computers and find all cycles. The result is a set of tuples, 
    each tuple containing the names of the three computers in the cycle."""
    result = []
    for computer in computers:
        for cycle in find_cycles_containing_computer(computer):
            result.append(cycle)
    return result


def find_cycles_containing_computer(computer):
    """For a given computer find all cycles containing it.
    We build out paths in alpha order, otherwise we'd find each cycle three times
    and have to remove duplicates later. 
    Yields tuples containing three computer names in alpha order."""
    deck = deque([[computer]])
    while deck:
        path = deck.popleft()
        if len(path) == 3 and path[-1] in path[0].get_neighbors():
            yield tuple([computer.value for computer in path])
        if len(path) < 3:
            for neighbor in path[-1].get_neighbors():
                if neighbor not in path and path[-1].value < neighbor.value:
                    deck.append(path + [neighbor])
