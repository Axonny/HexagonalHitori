import os
from solver import Solver
from argparse import ArgumentParser
from hitori_exceptions import NoSolution


def import_from_file(filename: str) -> list[list[int]]:
    if not os.path.exists(filename):
        print("Error: File isn't exists")
        exit(1)
    with open(filename, 'r', encoding='utf-8') as f:
        data = list(map(lambda l: l.strip().split(), f.readlines()))
    sizes = {*map(lambda x: len(x), data), len(data)}
    if len(sizes) != 1:
        print("Error: Field isn't square")
        exit(2)
    try:
        return [list(map(int, i)) for i in data]
    except ValueError:
        print("Error: File contains something besides numbers")
        exit(3)


def solve(data: list[list[int]], count_solves: int, required_sum: int) -> None:
    s = Solver(data, count_solves, required_sum)
    s.board.print_board()
    try:
        results = s.solve()
        print(f"Solve count: {len(results)}")
        for result in results:
            result.print_board()
    except NoSolution:
        print("No Solution")
        exit(0)


def main():
    p = ArgumentParser()
    p.add_argument('filename', type=str, help='Path to file')
    p.add_argument('-c', "--count", type=int, default=None, help='Find n solves. Default is all')
    p.add_argument('-s', "--sum", type=int, default=None, help='Limit on the amount per line. Default is no limit')

    args = p.parse_args()

    data = import_from_file(args.filename)
    solve(data, args.count, args.sum)


if __name__ == '__main__':
    main()
