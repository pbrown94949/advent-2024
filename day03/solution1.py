import re

pattern = re.compile(r"""
                     mul                   # instruction
                     \(                    # open parenthesis
                     ([1-9][0-9]{0,2})     # first number
                     ,                     # comma
                     ([1-9][0-9]{0,2})     # second number
                     \)                    # close parenthesis
                     """, re.X)


def run(lines):
    result = 0
    for a, b in get_number_pairs(lines):
        result += (a * b)
    return result


def get_number_pairs(lines):
    for line in lines:
        matches = re.finditer(pattern, line)
        for match in matches:
            yield int(match.group(1)), int(match.group(2))
