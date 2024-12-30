from collections import defaultdict
import math
import re


class Robot:

    def __init__(self, initial_position, velocity, room):
        self._position = initial_position
        self._velocity = velocity
        self._room = room

    def move(self):
        x, y = self._position[0] + self._velocity[0], self._position[1] + self._velocity[1]
        x = x % self._room[0]
        y = y % self._room[1]
        self._position = (x, y)

    @property
    def position(self):
        return self._position


input_pattern = re.compile(r"""
                           p=
                           ([0-9]+)       # x position
                           ,
                           ([0-9]+)       # y position
                           \s
                           v=
                           ([-]?[0-9]+)   # x velocity
                           ,
                           ([-]?[0-9]+)   # y velocity
""", re.X)


def run(lines):
    room, dividers = get_room(lines)
    robots = get_robots(lines, room)
    for _ in range(100):
        for robot in robots:
            robot.move()
    totals = defaultdict(int)
    for robot in robots:
        quadrant = calculate_quadrant(robot.position, dividers)
        if quadrant is not None:
            totals[quadrant] += 1
    return math.prod(totals.values())


def get_room(lines):
    """the size of the room changes depending on if we are using sample input or real input"""
    big_room = len(lines) > 20
    room = (101, 103) if big_room else (11, 7)
    dividers = tuple((x - 1) // 2 for x in room)
    return room, dividers


def calculate_quadrant(position, dividers):
    """We can represent each quadrant with a pair of booleans."""
    if position[0] == dividers[0] or position[1] == dividers[1]:
        return None
    return (position[0] < dividers[0], position[1] < dividers[1])


def get_robots(lines, room) -> list[Robot]:
    """Read the robots from the input file."""
    result = []
    for line in lines:
        match = input_pattern.fullmatch(line)
        initial_position = (int(match.group(1)), int(match.group(2)))
        velocity = (int(match.group(3)), int(match.group(4)))
        robot = Robot(initial_position, velocity, room)
        result.append(robot)
    return result


def print_positions(robots, room):
    counts = defaultdict(int)
    for robot in robots:
        counts[robot.position] += 1
    for y in range(room[1]):
        for x in range(room[0]):
            position = (x, y)
            count = counts[position]
            char = count if count > 0 else '.'
            print(char, end='')
        print()