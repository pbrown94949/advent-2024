from __future__ import annotations
from collections import defaultdict, deque

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

    def __init__(self):
        self.distance: int = None
        self.visited: bool = False
        self.previous: list[Node] = []

    def __repr__(self):
        return f'NodeState(distance={self.distance}, visited={self.visited})'


def run(lines) -> int:
    numeric_keypad_rewrite_rules = get_rewrite_rules_for_numeric_keyboard()
    directional_keypad_rewrite_rules = get_rewrite_rules_for_directional_keyboard()
    result = 0
    for line in lines:
        result += calculate_complexity(line, numeric_keypad_rewrite_rules, directional_keypad_rewrite_rules)
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


def get_shortest_paths(nodes: list[Node]) -> dict[tuple[str, str], str]:
    """Find the shortest paths between every pair of nodes in the provided list.

    The result is a dict where the dict keys are tuples (a, b) where a and b are 
    keys on the keypad. The dict values are the shortest paths for moving from 
    key a to key b. The paths are represented by strings using the characters: ^ v < >. 

    Notice that the inputs are nodes but the outputs are strings because at this point 
    we don't need the nodes anymore. 
    """
    result = defaultdict(list)
    for n1 in nodes:
        dijkstra_from_n1 = dijkstra(n1, nodes)
        for n2 in dijkstra_from_n1:
            for path in represent_shortest_paths_as_strings(n2, dijkstra_from_n1):
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


def represent_shortest_paths_as_strings(node: Node, nodes_to_states: dict[Node, NodeState]) -> list[str]:
    """Using the information we got from Djikstra's algorithm, reconstruct the shortest paths used to reach the
    provided node. There is an implied start_node in this function because the data in nodes_to_states came from 
    running Djikstra's algorithm for a specific start node. But we don't reference that start node explicitly in this
    function because we don't need it.
    
    The strings generated here contain the characters: ^ v < > to indicate direction of movement.
    """
    result = []
    q = deque([(node, '')])
    while q:
        node, path = q.pop()
        state = nodes_to_states[node]
        if not state.previous:
            result.append(path)
        else:
            for previous in state.previous:
                direction = [k for k, v in previous.get_neighbors().items() if v == node][0]
                q.append((previous, direction + path))
    return result


def calculate_complexity(code: str, numeric_keypad_rewrite_rules: dict[tuple[str, str], str], directional_keypad_rewrite_rules: dict[tuple[str, str], str]) -> int:
    """Calculate the complexity of a code according to the rules of the problem."""
    numeric_part_of_code = int(code[:3])
    length_of_shortest_sequence = get_length_of_shortest_sequence(code, numeric_keypad_rewrite_rules, directional_keypad_rewrite_rules)
    return numeric_part_of_code * length_of_shortest_sequence


def get_length_of_shortest_sequence(code: str, numeric_keypad_rewrite_rules: dict[tuple[str, str], str], directional_keypad_rewrite_rules: dict[tuple[str, str], str]) -> int:
    """Rewrite the code three times using rules generated above and return the length of the shortest result."""
    messages = [code]
    for paths in [numeric_keypad_rewrite_rules, directional_keypad_rewrite_rules, directional_keypad_rewrite_rules]:
        messages = rewrite_messages(messages, paths)
        shortest_message = min(len(x) for x in messages)
        messages = [x for x in messages if len(x) == shortest_message]
    return len(messages[0])


def rewrite_messages(messages: list[str], rewrite_rules: dict[tuple[str, str], str]) -> list[str]:
    """Rewrite a list of messages using the provided rules. We prepend 'A' because every write operation starts on the 'A' key."""
    result = []
    for message in messages:
        result.extend(rewrite_message('A' + message, rewrite_rules))
    return result


def rewrite_message(message: str, rewrite_rules: dict[tuple[str, str], str]) -> list[str]:
    """Rewrite a single message using the provided rules. Postpend 'A' """
    applicable_rules = rewrite_rules[(message[0], message[1])]
    if len(message) == 2:
        return [rule + 'A' for rule in applicable_rules]
    result = []
    for rule in applicable_rules:
        for rewritten_message in rewrite_message(message[1:], rewrite_rules):
            result.append(rule + 'A' + rewritten_message)
    return result
