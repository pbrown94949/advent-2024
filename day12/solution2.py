from collections import deque


def run(lines):
    result = 0
    for region in get_regions(lines):
        area, edges = get_area(region), count_edges(region)
        result += (area * edges)
    return result


def get_regions(lines):
    """Iterate over a garden and return all regions in the garden. This method destroys the garden it operates on."""
    garden = get_garden(lines)
    while True:
        plot = get_any_plot(garden)
        if plot is None:
            break
        region = get_region(garden, plot)
        erase_region(garden, region)
        yield region


def get_garden(lines):
    """Convert the input into a garden. A garden is a dictionary with keys that are plots and values that are plants."""
    result = {}
    for row, line in enumerate(lines):
        for col, plant in enumerate(line):
            result[(row, col)] = plant
    return result


def get_any_plot(garden):
    """Return any plot from the garden."""
    for plot in garden:
        return plot
    return None


def get_region(garden, plot):
    """Return the region containing the provided plot. A region is all the contiguous plots growing the same plant."""
    result = set()
    plant = garden[plot]
    fifo = deque()
    fifo.append(plot)
    while fifo:
        plot = fifo.pop()
        if plot not in result and garden.get(plot, None) == plant:
            result.add(plot)
            fifo.extend(get_neighbors(plot))
    return result


def get_neighbors(plot):
    """Given a plot, return the plots north, south, east, and west of it."""
    row, col = plot
    return [(row - 1, col), (row + 1, col), (row, col + 1), (row, col - 1)]


def erase_region(garden, region):
    """Remove all plots in the region from the garden. """
    for plot in region:
        del garden[plot]


def get_area(region):
    """Calculate the area of a region."""
    return len(region)


def count_edges(region):
    """Count the number of edges a region has."""
    rows = {row for row, _ in region}
    cols = {col for _, col in region}
    result = 0
    for row in range(min(rows), max(rows) + 2):
        result += count_edges_by_row(row, cols, region)
    for col in range(min(cols), max(cols) + 2):
        result += count_edges_by_col(col, rows, region)
    return result


def count_edges_by_row(row, cols, region):
    """Count all edges between the specified row and the row to its north."""
    result = 0
    prior_edge_indicator = (False, False)
    for col in range(min(cols), max(cols) + 1):
        north, south = (row - 1, col), (row, col)
        edge_indicator = (south in region, north in region)
        if is_new_edge(edge_indicator, prior_edge_indicator):
            result += 1
        prior_edge_indicator = edge_indicator
    return result


def count_edges_by_col(col, rows, region):
    """Count all edges between the specified column and the column to its west."""
    result = 0
    prior_edge_indicator = (False, False)
    for row in range(min(rows), max(rows) + 1):
        east, west = (row, col), (row, col - 1)
        edge_indicator = (east in region, west in region)
        if is_new_edge(edge_indicator, prior_edge_indicator):
            result += 1
        prior_edge_indicator = edge_indicator
    return result


def is_new_edge(edge_indicator, prior_edge_indicator):
    """For two adjacent plots, if one is inside the region and one is outside the region, then there is an edge between them.
    If the two plots have a different relationship than the prior pair we looked at, then this is a new edge that hasn't been counted yet."""
    return any(edge_indicator) and not all(edge_indicator) and edge_indicator != prior_edge_indicator
