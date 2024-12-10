from collections import defaultdict


def run(lines):
    grid = get_grid(lines)
    trails = get_trail_heads(grid)
    for _ in range(9):
        trails = advance_trails(trails, grid)
    ratings = get_ratings(trails)
    return sum(ratings)


def get_grid(lines):
    result = {}
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            result[(row, col)] = int(char)
    return result


def get_trail_heads(grid):
    result = []
    for k, v in grid.items():
        if v == 0:
            result.append([k])
    return result


def advance_trails(trails, grid):
    result = []
    for trail in trails:
        last_position = trail[-1]
        last_height = grid[last_position]
        for adjacent_position in get_adjacent_positions(last_position):
            if grid.get(adjacent_position, None) == last_height + 1:
                new_trail = list(trail) + [adjacent_position]
                result.append(new_trail)
    return result


def get_adjacent_positions(position):
    row, col = position
    return [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]


def get_ratings(trails):
    temp = defaultdict(set)
    for trail in trails:
        trail_head = trail[0]
        temp[trail_head].add(tuple(trail))
    return [len(x) for x in temp.values()]
