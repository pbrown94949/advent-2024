from collections import defaultdict


def run(lines):
    """Find the sequence with the total highest price."""
    totals = defaultdict(int)
    for line in lines:
        n = int(line)
        subtotals = accumulate_sequences(n)
        for k, v in subtotals.items():
            totals[k] += v
    return max(totals.values())


def accumulate_sequences(start_value: int):
    """For each sequence we find, store the first price associated with it."""
    result = {}
    for sequence, price in get_sequences(start_value):
        if sequence not in result:
            result[sequence] = price
    return result


def get_sequences(start_value: int):
    """Return sequences of four price changes and the price after the last change."""
    generator = get_secret_numbers(start_value)
    prior_price = start_value % 10
    price_changes = []
    for _ in range(2000):
        current_price = next(generator) % 10
        price_changes.append(current_price - prior_price)
        if len(price_changes) >= 4:
            price_changes = price_changes[-4:]
            yield tuple(price_changes), current_price
        prior_price = current_price


def get_secret_numbers(start_value: int):
    """Generate a list of secret numbers using the start_value and the algorithm described in the problem."""
    secret_number = start_value
    while True:
        n = secret_number * 64
        secret_number = secret_number ^ n
        secret_number = secret_number % 16777216
        n = secret_number // 32
        secret_number = secret_number ^ n
        secret_number = secret_number % 16777216
        n = secret_number * 2048
        secret_number = secret_number ^ n
        secret_number = secret_number % 16777216
        yield secret_number
