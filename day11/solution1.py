class Node:

    def __init__(self, value):
        self.value = value
        self.prev, self.next = None, None

    def __repr__(self):
        return f'Node({self.value})'


def run(lines):
    head = get_stones(lines)
    for blink in range(1, 26):
        head = process_stones(head)
    return len(list(iterate_node_list(head)))


def get_stones(lines):
    stones = [int(x) for x in lines[0].split()]
    stones = [Node(x) for x in stones]
    for i in range(len(stones) - 1):
        link(stones[i], stones[i+1])
    return stones[0]


def process_stones(head):
    stones = list(iterate_node_list(head))
    head = process_stone(stones[0])
    for stone in stones[1:]:
        process_stone(stone)
    return head


def process_stone(stone):
    # apply the rules to change the stone number
    # return the left most stone so caller can know if the head of the list has changed
    if stone.value == 0:
        stone.value = 1
        return stone
    s = str(stone.value)
    if len(s) % 2 == 0:
        midpoint = len(s) // 2
        left, right = s[:midpoint], s[midpoint:]
        left, right = Node(int(left)), Node(int(right))
        link(left, right)
        splice(stone.prev, left, stone.next)
        return left
    else:
        stone.value *= 2024
        return stone


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


def iterate_node_list(node, forward=True):
    while node is not None:
        yield node
        node = node.next if forward else node.prev
