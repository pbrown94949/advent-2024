import re

mul_pattern = re.compile(r"""
                     mul                   # multiplication command
                     \(                    # open parenthesis
                     ([1-9][0-9]{0,2})     # first number           - group 1
                     ,                     # comma
                     ([1-9][0-9]{0,2})     # second number          - group 2
                     \)                    # close parenthesis
                     """, re.X)

do_pattern = re.compile(r"do\(\)")
dont_pattern = re.compile(r"don't\(\)")

all_patterns = re.compile(f"{mul_pattern.pattern}|{do_pattern.pattern}|{dont_pattern.pattern}", re.X)

def run(lines):
    result = 0
    multiplication_enabled = True
    for instruction in get_instructions(lines):
        if match := mul_pattern.fullmatch(instruction):
            if multiplication_enabled:
                a, b = int(match.group(1)), int(match.group(2))
                result += (a * b)
        elif do_pattern.fullmatch(instruction):
            multiplication_enabled = True
        elif dont_pattern.fullmatch(instruction):
            multiplication_enabled = False
        else:
            print('Error', instruction)
    return result


def get_instructions(lines):
    for line in lines:
        for match in re.finditer(all_patterns, line):
            yield match.group(0)
