directions = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1),
}


def run(lines):
    lab = get_lab(lines)
    obstacles = get_obstacles(lines)
    visited = set()
    position = get_starting_position(lines)
    direction = 'N'
    while position in lab:
        visited.add(position)
        movement = directions[direction]
        new_position = (position[0] + movement[0], position[1] + movement[1])
        if new_position in obstacles:
            direction = turn_right(direction)
        else:
            position = new_position
    return len(visited)            
    


def get_starting_position(lines):
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '^':
                return row, col
    raise Exception('No starting position found')


def get_lab(lines):
    result = set()
    for row, line in enumerate(lines):
        for col, _ in enumerate(line):
            result.add((row, col))
    return result


def get_obstacles(lines):
    result = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                result.add((row, col))
    return result


def turn_right(direction):
    keys = list(directions.keys())
    index = keys.index(direction)
    return keys[(index + 1) % 4]