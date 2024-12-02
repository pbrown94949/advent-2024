def run(lines):
    reports = get_reports(lines)
    result = 0
    for report in reports:
        if is_safe_report(report):
            result += 1
    return result


def get_reports(lines):
    result = []
    for line in lines:
        split = line.split()
        result.append([int(x) for x in split])
    return result


def is_safe_report(report):
    differences = [report[i+1] - report[i] for i in range(len(report) - 1)]
    negative = positive = False
    for difference in differences:
        if difference < 0:
            negative = True
        if difference > 0:
            positive = True
        if negative and positive:
            return False
        if difference == 0:
            return False
        if abs(difference) > 3:
            return False
    return True
