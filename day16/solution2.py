from __future__ import annotations
from collections import deque
from dataclasses import dataclass


class Node:
    """A node in a weighted graph. value cannot be changed once set. edges can only be modified through the link() method. distance and visited can be updated as needed to perform Dijkstra's algorithm."""

    def __init__(self, value):
        self._value = value
        self._edges: list[Edge] = []
        self.distance = None
        self.visited = False
        self.previous: list[Node] = []

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


def run(lines):
    start, end = get_start_and_end(lines)
    weighted_graph = get_weighted_graph(lines)
    current_node = weighted_graph.get_node_by_value((start, 'E'))
    current_node.distance = 0
    while current_node is not None:
        for edge in current_node.edges:
            distance = current_node.distance + edge.weight
            if not edge.node.visited:
                if edge.node.distance is None or edge.node.distance > distance:
                    edge.node.distance = distance
                    edge.node.previous = [current_node]
                elif edge.node.distance == distance:
                    edge.node.previous.append(current_node)
        current_node.visited = True
        current_node = weighted_graph.get_dijkstra_current_node()
    # We could have exited in any of the four directions, so check all four cases.
    exit_nodes = [weighted_graph.get_node_by_value((end, direction)) for direction in 'NSEW']
    lowest_score = min([node.distance for node in exit_nodes if node.distance is not None])
    queue = deque([node for node in exit_nodes if node.distance == lowest_score])
    points_on_best_path = set()
    while queue:
        node = queue.popleft()
        for previous in node.previous:
            queue.append(previous)
        point, _ = node.value
        points_on_best_path.add(point)
    return len(points_on_best_path)


directions = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}


def get_weighted_graph(lines):
    """Represent the maze as a weighted graph. 
    There are four times as many nodes in the graph as there are locations in the maze because we track direction of travel as well as location. So in the graph we would have nodes for position x, y travelling north, south, east, and west.
    At any node you have the option of turning left or right, changing your direction without changing your position. This has a weight of 1000. Additionally if there's no wall in the way you have the option of moving forward in your current direction. This has a weight of 1. 
    So each node has either two or three edges. """
    points = get_points(lines)
    nodes = []
    # Build nodes
    for point in points:
        for direction in 'NSEW':
            maze_position = (point, direction)
            nodes.append(Node(maze_position))
    weighted_graph = WeightedGraph(nodes)
    # Link nodes
    for node in weighted_graph.nodes:
        point, direction = node.value
        # The cost of travelling to your neighbor in your current direction is 1
        neighbor_value = (add(point, directions[direction]), direction)
        neighbor = weighted_graph.get_node_by_value(neighbor_value)
        if neighbor is not None:
            node.link(neighbor, 1)
        # The cost of turning right or left is 1000
        turn_directions = 'NS' if direction in 'EW' else 'EW'
        for turn_direction in turn_directions:
            neighbor = weighted_graph.get_node_by_value((point, turn_direction))
            node.link(neighbor, 1000)
    return weighted_graph


def get_points(lines):
    """Return all points in the input that are not a wall."""
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char in '.ES':
                yield (row, col)


def get_start_and_end(lines):
    """Return the coordinates of the start point and exit point."""
    start = end = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == 'S':
                start = (row, col)
            elif char == 'E':
                end = (row, col)
    return start, end


def add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])
