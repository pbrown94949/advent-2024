from collections import Counter
from collections.abc import Iterable


def run(lines: Iterable[str]) -> int:
    counter = get_initial_counter(lines)
    for _ in range(75):
        counter = advance_counter(counter)
    return sum(counter.values())


def get_initial_counter(lines) -> Counter[int]:
    result: Counter[int] = Counter()
    for n in [int(x) for x in lines[0].split()]:
        result[n] += 1
    return result


def advance_counter(counter: Counter[int]) -> Counter[int]:
    result: Counter[int] = Counter()
    for k, v in counter.items():
        for n in get_next_numbers(k):
            result[n] += v
    return result


def get_next_numbers(n: int) -> Iterable[int]:
    if n == 0:
        return [1]
    s = str(n)
    if len(s) % 2 == 0:
        midpoint = len(s) // 2
        return [int(s[:midpoint]), int(s[midpoint:])]
    return [n * 2024]
