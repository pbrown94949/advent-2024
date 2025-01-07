def run(lines):
    patterns = get_patterns(lines)
    designs = get_designs(lines)
    result = 0
    for design in designs:
        result += process_design(design, patterns)
    return result


def get_patterns(lines):
    return set(lines[0].split(', '))


def get_designs(lines):
    return list(lines[2:])


def process_design(design, patterns):
    """Count how many ways there are to acheive the provided design using the provided patterns.
    
    Loop through every character in the design. Find any locations you can reach from the current location (i)
    and copy the total from the current location to the next location. 

    If the copy attempt is out of bounds, that just means we have fully consumed the design and should add whatever
    total we have to the result.
    """
    result = 0
    totals = [0 for _ in range(len(design))]
    totals[0] = 1
    for i in range(len(totals)):
        if totals[i] > 0:
            for pattern in patterns:
                if design.startswith(pattern, i):
                    try:
                        totals[i + len(pattern)] += totals[i]
                    except IndexError:
                        result += totals[i]
            totals[i] = 0
    return result
