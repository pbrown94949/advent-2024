import argparse
import importlib
import os
import time

argparser = argparse.ArgumentParser()
argparser.add_argument('day', type=int)
argparser.add_argument('solution', type=int, choices=[1, 2])
argparser.add_argument('input', choices=['a', 'b'])


def main():
    init()
    process()
    wrapup()


def init():
    global args
    args = argparser.parse_args()
    global start_time
    start_time = time.time()



def process():
    solution = get_solution(args.day, args.solution)
    answer = solution.run(get_input_lines(args.day, args.input))
    print(f'Answer: {answer}')


def get_solution(day, solution):
    module_name = f'day{day:02d}.solution{solution}'
    return importlib.import_module(module_name)


def get_input_lines(day, input_id):
    file_name = f'input_{input_id}.txt'
    file_path = os.path.join(f'day{day:02d}', file_name)
    for line in open(file_path):
        yield line.strip()


def wrapup():
    print("--- %s seconds ---" % int(time.time() - start_time))


if __name__ == "__main__":
    main()
