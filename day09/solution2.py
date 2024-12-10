class File:

    def __init__(self, size, id=None):
        self.size = size
        self.id = id

    @property
    def empty(self):
        return self.id is None

    def __repr__(self):
        if self.id is not None:
            return f'File(size={self.size}, id={self.id})'
        else:
            return f'File(size={self.size})'


class Node:

    def __init__(self, value):
        self.value = value
        self.prev, self.next = None, None

    def __repr__(self):
        return f'Node({self.value})'


def run(lines):
    files = read_files(lines)
    nodes = build_nodes(files)
    move_files(nodes)
    return calculate_checksum(nodes[0])


def read_files(lines):
    result = []
    file_mode, file_id = True, 0
    for n in lines[0]:
        n = int(n)
        if file_mode:
            result.append(File(n, file_id))
            file_id += 1
        else:
            result.append(File(n))
        file_mode = not file_mode
    return result


def build_nodes(files):
    result = [Node(x) for x in files]
    for i in range(len(result) - 1):
        link(result[i], result[i+1])
    return result


def move_files(nodes):
    for source in reversed(nodes):
        if not source.value.empty:
            target = find_target_node(nodes[0], source)
            if target is not None:
                move_file(source, target)


def find_target_node(node, source):
    while node != source:
        if node.value.empty and node.value.size >= source.value.size:
            return node
        node = node.next
    return None


def move_file(source: Node, target: Node):
    copy_file(source, target)
    erase_file(source)


def copy_file(source, target):
    copied_file = Node(File(source.value.size, source.value.id))
    if target.value.size > source.value.size:
        leftover_space = Node(File(target.value.size - source.value.size))
        link(copied_file, leftover_space)
    splice(target.prev, copied_file, target.next)


def erase_file(node):
    # create empty blocks to replace the file we moved
    empty_space = File(node.value.size)
    # merge with the adjacent blocks if those are also empty
    prev = node.prev
    if prev is not None and prev.value.empty:
        empty_space.size += prev.value.size
        prev = prev.prev
    next = node.next
    if next is not None and next.value.empty:
        empty_space.size += next.value.size
        next = next.next
    splice(prev, Node(empty_space), next)


def calculate_checksum(node):
    result = block_id = 0
    for node in iterate_node_list(node):
        file = node.value
        if file.empty:
            block_id += file.size
        else:
            for _ in range(file.size):
                result += (block_id * file.id)
                block_id += 1
    return result


def splice(prev, insert_head, next):
    # unlink the sublist between prev and next
    if prev is not None and prev.next is not None:
        prev.next.prev = None
    if next is not None and next.prev is not None:
        next.prev.next = None
    # get the end of the insertion list
    insert_tail = insert_head
    while insert_tail.next is not None:
        insert_tail = insert_tail.next
    # link everything up
    link(prev, insert_head)
    link(insert_tail, next)


def link(left, right):
    if left is not None:
        left.next = right
    if right is not None:
        right.prev = left


def print_node_list(node, forward=True):
    for node in iterate_node_list(node, forward):
        print(node)


def iterate_node_list(node, forward=True):
    while node is not None:
        yield node
        node = node.next if forward else node.prev
