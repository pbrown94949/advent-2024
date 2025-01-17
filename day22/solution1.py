class SecretNumberGenerator:

    def __init__(self, secret_number: int):
        self._secret_number = secret_number

    @property
    def secret_number(self):
        return self._secret_number

    def next(self):
        self._mix(self._secret_number * 64)
        self._prune()
        self._mix(self._secret_number // 32)
        self._prune()
        self._mix(self._secret_number * 2048)
        self._prune()
        return self._secret_number

    def _mix(self, n):
        self._secret_number ^= n

    def _prune(self):
        self._secret_number = self._secret_number % 16777216


def run(lines):
    result = 0
    for n in lines:
        n = int(n)
        secret_number = get_2000th_secret_number(n)
        result += secret_number
    return result


def get_2000th_secret_number(n: int):
    sng = SecretNumberGenerator(n)
    for _ in range(2000):
        sng.next()
    return sng.secret_number
