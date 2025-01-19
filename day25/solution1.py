def run(lines):
    locks, keys = get_locks_and_keys(lines)
    result = 0
    for lock in locks:
        for key in keys:
            if not overlaps(lock, key):
                result += 1
    return result


def get_locks_and_keys(lines):
    """Create items by calculating the number #s in each columm (minus 1). We subtract 1
    to account for the row that indicates if the item is a key or a lock."""
    locks, keys = [], []
    for block in get_input_blocks(lines):
        is_lock = block[0] == "#####"
        item = [-1 for _ in range(len(block[0]))]
        for line in block:
            for idx, char in enumerate(line):
                if char == '#':
                    item[idx] += 1
        if is_lock:
            locks.append(item)
        else:
            keys.append(item)
    return locks, keys


def get_input_blocks(lines):
    """Partition the input by blank rows."""
    result = []
    for line in lines:
        if line == '':
            yield result
            result = []
        else:
            result.append(line)
    if result:
        yield result


def overlaps(lock: list[int], key: list[int]):
    """Determine if there's any column were the totals exceed 5."""
    for idx in range(len(lock)):
        if lock[idx] + key[idx] > 5:
            return True
    return False