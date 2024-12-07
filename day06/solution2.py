directions = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1),
}


def run(lines):
    result = 0
    lab, obstacles = get_lab(lines), get_obstacles(lines)
    position, direction = get_starting_position(lines), 'N'
    visited = get_visited_positions(lab, obstacles, position, direction)
    obstacle_candidates = visited.copy()
    obstacle_candidates.remove(position)
    for candidate in obstacle_candidates:
        new_obstacles = obstacles.copy()
        new_obstacles.add(candidate)
        if find_cycle(lab, new_obstacles, position, direction):
            result += 1
    return result


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


def get_visited_positions(lab, obstacles, position, direction):
    result = set()
    while position in lab:
        result.add(position)
        movement = directions[direction]
        new_position = (position[0] + movement[0], position[1] + movement[1])
        if new_position in obstacles:
            direction = turn_right(direction)
        else:
            position = new_position
    return result


def find_cycle(lab, obstacles, position, direction):
    visited = set()
    while True:
        visited.add((position, direction))
        movement = directions[direction]
        new_position = (position[0] + movement[0], position[1] + movement[1])
        if new_position not in lab:
            return False
        if new_position in obstacles:
            direction = turn_right(direction)
        else:
            position = new_position
        # if we've already been in this position traveling in the same direction, we are in a cycle
        if (position, direction) in visited:
            return True


def turn_right(direction):
    keys = list(directions.keys())
    index = keys.index(direction)
    return keys[(index + 1) % 4]
