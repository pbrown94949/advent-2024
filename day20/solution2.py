directions = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}


def run(lines):
    start, _, tracks, walls = read_input(lines)
    times = assign_times(start, tracks)
    cheat_adjustments = get_cheat_adjustments()
    result = 0
    for track in tracks:
        cheat_points = get_cheat_points(track, cheat_adjustments, tracks, walls)
        for cheat_point in cheat_points:
            distance = calculate_distance(track, cheat_point)
            time_saved = times[cheat_point] - times[track] - distance
            if time_saved >= 100:
                result += 1
    return result


def read_input(lines):
    tracks, walls = set(), set()
    start, end = None, None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                walls.add((row, col))
            else:
                tracks.add((row, col))
            if char == 'S':
                start = (row, col)
            if char == 'E':
                end = (row, col)
    return start, end, tracks, walls


def assign_times(start, tracks):
    """Set the time it takes to reach each track for every track on the racetrack."""
    result = {}
    n, coord = 0, start
    remaining = set(tracks)
    while True:
        result[coord] = n
        remaining.remove(coord)
        n += 1
        neighbors = list(remaining & {add(coord, directions[d]) for d in 'NSEW'})
        if not neighbors:
            break
        coord = neighbors[0]
    return result


def get_cheat_adjustments():
    """Calculate the coordinates of all the spaces up to 20 spaces away from (0,0)."""
    result = set()
    for distance in range(2, 21):
        points = []
        for x in range(distance + 1):
            y = distance - x
            points.append((x, y))
        for x, y in points:
            result.update([(x, y), (x, -y), (-x, y), (-x, -y)])
    return sorted(result)


def get_cheat_points(track, cheat_adjustments, tracks, walls):
    """For the given track, determine all the cheat points. 
        A cheat point is any track within 20 spaces of the starting track
        which is adjacent to a wall on at least one side.

        I am confused why walls outside the cheat area count here 
        but I get the wrong answer without them. 
    """
    result = []
    cheat_area = {add(track, adj) for adj in cheat_adjustments}
    for candidate in cheat_area & tracks:
        neighbors = {add(candidate, directions[d]) for d in 'NSEW'} & walls
        if neighbors:
            result.append(candidate)
    return result


def add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])


def calculate_distance(t1, t2):
    return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])

