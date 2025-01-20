from __future__ import annotations
from collections import defaultdict, deque
from functools import cache

reverse_direction_map = {'^': 'v', 'v': '^', '>': '<', '<': '>'}


class Node:

    def __init__(self, value):
        self._value = value
        self._neighbors = {}

    def __repr__(self):
        return f'Node(value={self._value})'

    @property
    def value(self):
        return self._value

    def link(self, direction: str, node: Node):
        self._link(direction, node)
        node._link(reverse_direction_map[direction], self)

    def _link(self, direction: str, node: Node):
        self._neighbors[direction] = node

    def get_neighbors(self):
        return self._neighbors


class NodeState:
    """This class stores the state of a Node during and after processing by Djikstra's algorithm."""

    def __init__(self):
        self.distance: int = None
        self.visited: bool = False
        self.previous: list[Node] = []

    def __repr__(self):
        return f'NodeState(distance={self.distance}, visited={self.visited})'


class Rewriter:

    def __init__(self, rules):
        self._rules = rules

    def rewrite(self, message: str) -> list[str]:
        """Rewrite a single message using the rewriter's rules. A given message may be rewriteable in more than
        one way. Hence we return a list."""
        if len(message) < 2:
            return ['']
        result = []
        for rule in self._rules[(message[0], message[1])]:
            for rewritten_message in self.rewrite(message[1:]):
                result.append(rule + rewritten_message)
        return result


class RewriteLengthCalculator:
    """This class can calculate how long a string will be after it has been rewritten a certain number of times."""

    def __init__(self, rules):
        self._rules = rules

    def calculate_minimum_length(self, message: str, rewrites: int) -> int:
        """Calculate the length of a message after it has been rewriten x number of times in the shortest possible way.
        There may be other ways of rewriting the message that are longer."""
        if rewrites < 0:
            raise ValueError()
        result = self._calculate_minimum_length(None, message[0], rewrites)
        for i in range(1, len(message)):
            result += self._calculate_minimum_length(message[i-1], message[i], rewrites)
        return result

    @cache
    def _calculate_minimum_length(self, preceding_character: str, character: str, rewrites: int) -> int:
        """Calculate the length of a character after it has been rewritten x number of times in the shortest possible way.
        We get this length by taking the rewrite rule that applies to the character and calculating
        its minimum length after x - 1 rewrites. 
        Since multiple rewrite rules may apply, we take the rule that returns the shortest value.
        We cache the results of this method otherwise the calculations take too long.
        """
        if rewrites == 0:
            return 1
        if preceding_character is None:
            preceding_character = 'A'
        result = None
        for rule in self._rules[(preceding_character, character)]:
            temp = self.calculate_minimum_length(rule, rewrites - 1)
            if result is None or result > temp:
                result = temp
        return result


def run(lines) -> int:
    numeric_keypad_rewrite_rules = get_rewrite_rules_for_numeric_keyboard()
    directional_keypad_rewrite_rules = get_rewrite_rules_for_directional_keyboard()
    rewriter = Rewriter(numeric_keypad_rewrite_rules)
    length_calculator = RewriteLengthCalculator(directional_keypad_rewrite_rules)
    rewrites = 25
    result = 0
    for line in lines:
        complexity = calculate_complexity(line, rewrites, length_calculator, rewriter)
        result += complexity
    return result


def get_rewrite_rules_for_numeric_keyboard() -> dict[tuple[str, str], str]:
    graph = build_numeric_keypad_graph()
    return get_shortest_paths(graph)


def get_rewrite_rules_for_directional_keyboard() -> dict[tuple[str, str], str]:
    graph = build_directional_keypad_graph()
    return get_shortest_paths(graph)


def build_numeric_keypad_graph() -> list[Node]:
    """Build a graph that represents the relationship between the keys on a numeric keypad."""
    nodes = {str(n): Node(str(n)) for n in range(0, 10)}
    nodes['A'] = Node('A')
    links = []
    links.extend([(n, 'v', n - 3) for n in [4, 5, 6, 7, 8, 9]])    # vertical relationship between keys
    links.extend([(n, '>', n + 1) for n in [1, 2, 4, 5, 7, 8]])    # horizontal relationship between keys
    links.append(('2', 'v', '0'))                                  # special handling for 0 and A
    links.append(('3', 'v', 'A'))
    links.append(('0', '>', 'A'))
    for a, direction, b in links:
        nodes[str(a)].link(direction, nodes[str(b)])
    return list(nodes.values())


def build_directional_keypad_graph() -> list[Node]:
    """Build a graph that represents the relationship between the keys on a directional keypad."""
    nodes: dict[any, Node] = {}
    for x in '^v<>A':
        nodes[x] = Node(x)
    nodes['^'].link('v', nodes['v'])
    nodes['A'].link('v', nodes['>'])
    nodes['^'].link('>', nodes['A'])
    nodes['<'].link('>', nodes['v'])
    nodes['v'].link('>', nodes['>'])
    return list(nodes.values())


def get_shortest_paths(nodes: list[Node]) -> dict[tuple[str, str], list[str]]:
    """Find the shortest paths between every pair of nodes in the provided list.

    The result is a dict where the dict keys are tuples (a, b) where a and b are 
    keys on the keypad. The dict values are the shortest paths for moving from 
    key a to key b. The paths are represented by strings using the characters: ^ v < > A. 

    Notice that the inputs are nodes but the outputs are strings because at this point 
    we don't need the nodes anymore. 
    """
    result = defaultdict(list)
    for n1 in nodes:
        dijkstra_from_n1 = dijkstra(n1, nodes)
        for n2 in dijkstra_from_n1:
            for path in extract_shortest_paths(n2, dijkstra_from_n1):
                result[(n1.value, n2.value)].append(path)
    return result


def dijkstra(start_node: Node, all_nodes: list[Node]) -> dict[Node, NodeState]:
    """Use Dijkstra's algorithm to find the shortest paths from start_node to all nodes in the provided list.

    The result is a dict where the keys are the provided nodes and the values are NodeState objects which
    indicate the shortest distance from the start_node and paths that attain that shortest distance.
    """

    def get_next() -> NodeState | None:
        candidates = [state for state in states_to_nodes if not state.visited and state.distance is not None]
        if candidates:
            state = min(candidates, key=lambda x: x.distance)
            return states_to_nodes[state], state
        return None, None

    nodes_to_states = {node: NodeState() for node in all_nodes}
    states_to_nodes = {v: k for k, v in nodes_to_states.items()}
    current_node, current_state = start_node, nodes_to_states[start_node]
    current_state.distance = 0
    while current_node:
        distance = current_state.distance + 1
        for neighbor_node in current_node.get_neighbors().values():
            neighbor_state = nodes_to_states[neighbor_node]
            if not neighbor_state.visited:
                if neighbor_state.distance is None or neighbor_state.distance > distance:
                    neighbor_state.distance = distance
                    neighbor_state.previous = [current_node]
                elif neighbor_state.distance == distance:
                    neighbor_state.previous.append(current_node)
        current_state.visited = True
        current_node, current_state = get_next()
    return nodes_to_states


def extract_shortest_paths(node: Node, nodes_to_states: dict[Node, NodeState]) -> list[str]:
    """Using the information we got from Djikstra's algorithm, reconstruct the shortest paths used to reach the
    provided node. There is an implied start_node in this function because the data in nodes_to_states came from 
    running Djikstra's algorithm for a specific start node. But we don't reference that start node explicitly in this
    function because we don't need it.

    The strings generated here contain the characters: ^ v < > to indicate direction of movement and A to indicate pressing a button.
    """
    result = []
    q = deque([(node, '')])
    while q:
        node, path = q.pop()
        state = nodes_to_states[node]
        if not state.previous:
            result.append(path + 'A')
        else:
            for previous in state.previous:
                direction = [k for k, v in previous.get_neighbors().items() if v == node][0]
                q.append((previous, direction + path))
    return result


def calculate_complexity(line: str, generation: int, length_calculator: RewriteLengthCalculator, rewriter: Rewriter):
    """Calculate complexity using the method stated in the problem."""
    numeric_part_of_code = int(line[:3])
    length_of_shortest_rewrite = None
    for message in rewriter.rewrite('A' + line):
        length_of_rewrite = length_calculator.calculate_minimum_length(message, generation)
        if length_of_shortest_rewrite is None or length_of_shortest_rewrite > length_of_rewrite:
            length_of_shortest_rewrite = length_of_rewrite
    return numeric_part_of_code * length_of_shortest_rewrite
