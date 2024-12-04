directions = {
    'N': (-1, 0),
    'NE': (-1, 1),
    'E': (0, 1),
    'SE': (1, 1),
    'S': (1, 0),
    'SW': (1, -1),
    'W': (0, -1),
    'NW': (-1, -1)
}


class Grid:

    def __init__(self):
        self._dict = {}

    def add(self, row, col, value):
        self._dict[(row, col)] = value

    @property
    def max_row(self):
        return max(row for row, _ in self._dict.keys())

    @property
    def max_col(self):
        return max(col for _, col in self._dict.keys())

    def get_word(self, row, col, direction):
        result = ''
        adjustment = directions[direction]
        for _ in range(4):
            letter = self._dict.get((row, col), '')
            result += letter
            row, col = row + adjustment[0], col + adjustment[1]
        return result


def run(lines):
    result = 0
    grid = build_grid(lines)
    for word in get_words(grid):
        if word == 'XMAS':
            result += 1
    return result


def build_grid(lines):
    result = Grid()
    for row, line in enumerate(lines):
        for col, letter in enumerate(line):
            result.add(row, col, letter)
    return result


def get_words(grid: Grid):
    for row in range(grid.max_row + 1):
        for col in range(grid.max_col + 1):
            for direction in directions.keys():
                yield grid.get_word(row, col, direction)
