directions = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}


def run(lines):
    """For each space on the track, look two coordinates in every direction. If that coordinate is also a track, see how much time you would save by hopping over there. The hop takes two seconds, so reduce the savings by that much."""
    start, _, tracks, walls = read_input(lines)
    times = assign_times(start, tracks)
    result = 0
    for track in tracks:
        for d in 'NSEW':
            n1 = add(track, directions[d])
            n2 = add(n1, directions[d])
            if n1 in walls and n2 in tracks:
                time_saved = times[track] - times[n2] - 2
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


def add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])
