def run(lines):
    blocks = get_blocks(lines)
    empty_block_iterator = get_empty_block_iterator(blocks)
    file_block_iterator = get_file_block_iterator(blocks)
    empty_block, file_block = next(empty_block_iterator), next(file_block_iterator)
    while empty_block < file_block:
        blocks[empty_block] = blocks[file_block]
        blocks[file_block] = None
        empty_block, file_block = next(empty_block_iterator), next(file_block_iterator)
    result = 0
    for block_id, file_id in enumerate(blocks):
        if file_id is not None:
            result += (block_id * file_id)
    return result


def get_blocks(lines):
    result = []
    for group in get_block_groups(lines):
        result.extend(group)
    return result


def get_block_groups(lines):
    file_mode, file_id = True, 0
    for n in lines[0]:
        n = int(n)
        if file_mode:
            yield [file_id] * n
            file_id += 1
            file_mode = False
        else:
            yield [None] * n
            file_mode = True


def get_empty_block_iterator(blocks):
    i = 0
    while True:
        if blocks[i] is None:
            yield i
        i += 1


def get_file_block_iterator(blocks):
    i = len(blocks) - 1
    while True:
        if blocks[i] is not None:
            yield i
        i -= 1
