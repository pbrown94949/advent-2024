directions = {
    'NE': (-1, 1),
    'SE': (1, 1),
    'SW': (1, -1),
    'NW': (-1, -1)
}


class Grid:

    def __init__(self):
        self._dict = {}

    def add(self, row, col, value):
        self._dict[(row, col)] = value

    def get(self, row, col, direction=None):
        if direction is not None:
            adjustment = directions[direction]
            row, col = row + adjustment[0], col + adjustment[1]
        return self._dict.get((row, col), '')

    @property
    def max_row(self):
        return max(row for row, _ in self._dict.keys())

    @property
    def max_col(self):
        return max(col for _, col in self._dict.keys())


def run(lines):
    result = 0
    grid = build_grid(lines)
    for row in range(grid.max_row + 1):
        for col in range(grid.max_col + 1):
            if grid.get(row, col) == 'A' and is_a_cross(row, col, grid):
                result += 1
    return result


def build_grid(lines):
    result = Grid()
    for row, line in enumerate(lines):
        for col, letter in enumerate(line):
            result.add(row, col, letter)
    return result


def is_a_cross(row, col, grid: Grid):
    back_slash = {grid.get(row, col, direction) for direction in ['NW', 'SE']}
    forward_slash = {grid.get(row, col, direction) for direction in ['NE', 'SW']}
    return 'M' in back_slash and 'S' in back_slash and 'M' in forward_slash and 'S' in forward_slash
