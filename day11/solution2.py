from collections import deque


class Node:

    def __init__(self, value):
        self.value = value
        self.a_count = 0
        self.b_count = 0
        self.next_nodes = []

    def push_counts_forward(self, count_type):
        for next in self.next_nodes:
            if count_type == 'a':
                next.b_count += self.a_count
            else:
                next.a_count += self.b_count
        if count_type == 'a':
            self.a_count = 0
        else:
            self.b_count = 0

    def __repr__(self):
        return f'Node(value={self.value}, a_count={self.a_count}, b_count={self.b_count})'


def run(lines):
    graph = get_graph(lines)
    push_mode = 'a'
    for _ in range(75):
        for node in graph.values():
            node.push_counts_forward(push_mode)
        push_mode = 'b' if push_mode == 'a' else 'a'
    result = 0
    for node in graph.values():
        result += node.a_count + node.b_count
    return result


def get_graph(lines):
    map = {}
    # Create a node for each value in the graph
    for n in get_all_possible_numbers(lines):
        map[n] = Node(n)
    # Link each node to its one or two next values
    for node in map.values():
        for n in get_next_numbers(node.value):
            node.next_nodes.append(map[n])
    # Initialize starting nodes to have a value of 1
    for n in [int(x) for x in lines[0].split()]:
        map[n].a_count = 1
    return map


def get_all_possible_numbers(lines):
    already_seen = set()
    queue = deque()
    for n in [int(x) for x in lines[0].split()]:
        queue.append(n)
    while queue:
        n = queue.pop()
        if n not in already_seen:
            yield n
            already_seen.add(n)
            queue.extend(get_next_numbers(n))


def get_next_numbers(n):
    if n == 0:
        return [1]
    s = str(n)
    if len(s) % 2 == 0:
        midpoint = len(s) // 2
        return [int(s[:midpoint]), int(s[midpoint:])]
    return [n * 2024]


def print_graph(graph):
    for node in graph.values():
        if node.a_count > 0 or node.b_count > 0:
            print(node)
