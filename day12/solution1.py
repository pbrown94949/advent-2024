from collections import deque


def run(lines):
    result = 0
    garden = get_garden(lines)
    while True:
        plot = get_random_plot(garden)
        if plot is None:
            break
        plant, region = get_region(garden, plot)
        erase_region(garden, region)
        area, perimeter = get_area(region), get_perimeter(region)
        result += (area * perimeter)
    return result


def get_garden(lines):
    result = {}
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            result[(row, col)] = char
    return result


def get_random_plot(garden):
    for plot in garden:
        return plot
    return None


def get_region(garden, plot):
    plant = garden[plot]
    fifo = deque()
    fifo.append(plot)
    plots = set()
    while fifo:
        plot = fifo.pop()
        if plot not in plots and garden.get(plot, None) == plant:
            plots.add(plot)
            fifo.extend(get_neighbors(plot))
    return plant, plots


def erase_region(garden, region):
    for plot in region:
        del garden[plot]


def get_area(region):
    return len(region)


def get_perimeter(region):
    result = 0
    for plot in region:
        for neighbor in get_neighbors(plot):
            if neighbor not in region:
                result += 1
    return result


def get_neighbors(plot):
    row, col = plot
    return [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
