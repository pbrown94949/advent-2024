from collections import deque

moves = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}


class Warehouse:

    def __init__(self, width, height):
        self._rows = []
        for _ in range(height):
            row = [None for _ in range(width)]
            self._rows.append(row)

    def set(self, row, col, value):
        self._rows[row][col] = value

    def get(self, row, col):
        return self._rows[row][col]

    def move(self, robot, move):
        row, col = robot
        if self.get(row, col) != '@':
            raise Exception(f'Not a robot: {row}, {col}')
        adj_row, adj_col = moves[move]
        to_process, to_update = deque([(row, col)]), set()
        while to_process:
            r, c = to_process.popleft()
            value = self.get(r, c)            
            if value == '#': 
                return (row, col)
            if value in '@[]':
                to_update.add((r, c))
                to_process.append((r + adj_row, c + adj_col))
                if move in '^v' and value in '[]':
                    offset = 1 if value == '[' else -1
                    to_update.add((r, c + offset))
                    to_process.append((r + adj_row, c + offset))

        updates = [(r, c, '.') for r, c in to_update]
        updates += [(r + adj_row, c + adj_col, self.get(r, c)) for r, c in to_update]
        for r, c, value in updates:
            self.set(r, c, value)
        return (row + adj_row, col + adj_col)

    def print(self):
        for row in self._rows:
            for col in row:
                print(col, end='')
            print()

    def sum(self):
        result = 0
        for r, row in enumerate(self._rows):
            for c, value in enumerate(row):
                if value == '[':
                    result += 100 * r + c
        return result


def run(lines):
    warehouse, robot = build_warehouse(lines)
    for movement in get_moves(lines):
        robot = warehouse.move(robot, movement)
    warehouse.print()
    return warehouse.sum()


def build_warehouse(lines):
    width = height = 0
    for line in get_warehouse_lines(lines):
        width = len(line) * 2
        height += 1
    warehouse = Warehouse(width, height)
    robot = None
    for row, line in enumerate(get_warehouse_lines(lines)):
        for col, char in enumerate(expand_line(line)):
            warehouse.set(row, col, char)
            if char == '@':
                robot = (row, col)
    return warehouse, robot


def expand_line(line):
    """The input needs to be expanded, replacing each single character with a pair of characters."""
    char_map = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.'
    }
    result = ''
    for char in line:
        result += char_map[char]
    return result


def get_warehouse_lines(lines):
    for line in lines:
        if line.startswith('#'):
            yield line


def get_moves(lines):
    for line in lines:
        if not line.startswith('#'):
            for char in line:
                yield char
