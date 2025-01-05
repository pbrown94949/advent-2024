from __future__ import annotations
from dataclasses import dataclass


class Node:
    """A node in a weighted graph. value cannot be changed once set. edges can only be modified through the link() method. distance and visited can be updated as needed to perform Dijkstra's algorithm."""

    def __init__(self, value):
        self._value = value
        self._edges: list[Edge] = []
        self.distance = None
        self.visited = False

    def __repr__(self):
        return f'Node(value={self._value}, distance={self.distance}, visited={self.visited})'

    @property
    def value(self):
        return self._value

    @property
    def edges(self) -> list[Edge]:
        return list(self._edges)

    def link(self, neighbor: Node, cost: int):
        self._edges.append(Edge(neighbor, cost))


@dataclass
class Edge:
    """Represents a unidirectional link to a node in a weighted graph."""
    node: Node
    weight: int


class WeightedGraph:
    """Nodes are stored in a dictionary keyed by value to make get_node_by_value() fast. """

    def __init__(self, nodes: list[Node]):
        self._dict = {node.value: node for node in nodes}

    @property
    def nodes(self) -> list[Node]:
        return list(self._dict.values())

    def get_node_by_value(self, value) -> Node | None:
        return self._dict.get(value, None)

    def get_dijkstra_current_node(self) -> Node | None:
        nodes = [node for node in self._dict.values() if not node.visited and node.distance is not None]
        return min(nodes, key=lambda node: node.distance, default=None)


directions = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}

LINES_TO_READ = 1024
GRID_SIZE = 70


def run(lines):
    weighted_graph = get_weighted_graph(lines)
    current_node = weighted_graph.get_node_by_value((0, 0))
    current_node.distance = 0
    while current_node is not None:
        for edge in current_node.edges:
            distance = current_node.distance + edge.weight
            if not edge.node.visited:
                if edge.node.distance is None or edge.node.distance > distance:
                    edge.node.distance = distance
        current_node.visited = True
        current_node = weighted_graph.get_dijkstra_current_node()
    return weighted_graph.get_node_by_value((GRID_SIZE, GRID_SIZE)).distance


def get_weighted_graph(lines):
    points = get_points(lines)
    nodes = []
    # Build nodes
    for point in points:
        nodes.append(Node(point))
    weighted_graph = WeightedGraph(nodes)
    for node in weighted_graph.nodes:
        point = node.value
        for direction in 'NSEW':
            neighbor_point = add(point, directions[direction])
            neighbor = weighted_graph.get_node_by_value(neighbor_point)
            if neighbor is not None:
                node.link(neighbor, 1)
    return weighted_graph


def get_points(lines):
    corrupted_points = set()
    for line in lines[:LINES_TO_READ]:
        point = tuple(int(x) for x in line.split(','))
        corrupted_points.add(point)
    for x in range(GRID_SIZE + 1):
        for y in range(GRID_SIZE + 1):
            point = (x, y)
            if not point in corrupted_points:
                yield point


def add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])
