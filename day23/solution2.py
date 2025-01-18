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
    parties = get_all_parties(computers)
    biggest_party_size = max(len(party) for party in parties)
    biggest_party = [party for party in parties if len(party) == biggest_party_size][0]
    return ','.join(biggest_party)


def get_network(lines) -> list[Node]:
    """Convert the input into a graph of nodes representing computers on the network."""
    nodes = {}
    for line in lines:
        computer1, computer2 = line.split('-')
        if computer1 not in nodes:
            nodes[computer1] = Node(computer1)
        if computer2 not in nodes:
            nodes[computer2] = Node(computer2)
        nodes[computer1].link(nodes[computer2])
    return list(nodes.values())


def get_all_parties(computers) -> set[tuple]:
    """Accumulate all the parties by generating them for each computer. There's no risk of duplicates because get_parties() always
    returns parties where the provided computer is the first attendee."""
    result = []
    for computer in computers:
        result.extend(get_parties(computer))
    return result


def get_parties(computer) -> list[tuple]:
    """Generate all parties where this computer is alphabetically the first attendee. Generating attendees in alpha order
    cuts down the search space. 
    Returns a list of tuples. Each tuple corresponds to a party. The tuple contains the names of each computer attending the party.
    
    For each party we pop off the deque, since if any additional computers can attend it. A computer can be added to a party only if 
      - it is a neighbor of all computers already in the party .
      - its name is greater than the names of all computers already assigned to the party. 

    If no candidates are found, this is a big as the party can get. We add it to the list of results.
    """
    result = []
    deck = deque([[computer]])
    while deck:
        party = deck.popleft()
        max_computer = max(computer.value for computer in party)
        neighbors = set(party[0].get_neighbors())
        for computer in party: 
            neighbors &= computer.get_neighbors()
        candidates = [n for n in neighbors if n.value > max_computer]
        if candidates:
            for candidate in candidates:
                deck.append(party + [candidate])
        else:
            result.append(tuple(x.value for x in party))
    return result


