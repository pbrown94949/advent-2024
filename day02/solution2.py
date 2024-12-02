def run(lines):
    reports = get_reports(lines)
    result = 0
    for report in reports:
        if is_safe_report(report) or is_safe_report_with_dampener(report):
            result += 1
    return result


def get_reports(lines):
    result = []
    for line in lines:
        split = line.split()
        result.append([int(x) for x in split])
    return result


def is_safe_report(report):
    correct_sign = sign(report[1] - report[0])
    for i in range(len(report) - 1):
        difference = report[i+1] - report[i]
        if difference == 0 or sign(difference) != correct_sign or abs(difference) > 3:
            return False
    return True


def is_safe_report_with_dampener(report):
    for modified_report in drop_level_from_report(report):
        if is_safe_report(modified_report):
            return True
    return False

# return copies of the report with one item removed


def drop_level_from_report(report):
    for i in range(len(report)):
        yield [item for idx, item in enumerate(report) if idx != i]


def sign(n: int):
    return (n > 0) - (n < 0)
