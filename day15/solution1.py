from enum import Enum

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
        current_value = self.get(row, col)
        if current_value != '@':
            raise Exception(f'Unexpected value: {current_value}')
        adj_row, adj_col = moves[move]
        if self._send(row + adj_row, col + adj_col, move, current_value):
            self.set(row, col, '.')
            return (row + adj_row, col + adj_col)
        else:
            return (row, col)

    def _send(self, row, col, move, value):
        current_value = self.get(row, col)
        if current_value == '#':
            return False
        if current_value == '.':
            self.set(row, col, value)
            return True
        if self.get(row, col) == 'O':
            adj_row, adj_col = moves[move]
            if self._send(row + adj_row, col + adj_col, move, current_value):
                self.set(row, col, value)
                return True
            else:
                return False
        raise Exception(f'Unexpected value: {current_value}')

    def print(self):
        for row in self._rows:
            for col in row:
                print(col, end='')
            print()
    
    def sum(self):
        result = 0
        for r, row in enumerate(self._rows):
            for c, value in enumerate(row):
                if value == 'O':
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
        width = len(line)
        height += 1
    warehouse = Warehouse(width, height)
    robot = None
    for row, line in enumerate(get_warehouse_lines(lines)):
        for col, char in enumerate(line):
            warehouse.set(row, col, char)
            if char == '@':
                robot = (row, col)
    return warehouse, robot


def get_warehouse_lines(lines):
    for line in lines:
        if line.startswith('#'):
            yield line


def get_moves(lines):
    for line in lines:
        if not line.startswith('#'):
            for char in line:
                yield char