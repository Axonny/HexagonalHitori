from itertools import product
from functools import reduce
from operator import mul
from solver import Solver, NoSolution


def reshape(lst, shape):
    if len(shape) == 1:
        return lst
    n = reduce(mul, shape[1:])
    return [reshape(lst[i * n:(i + 1) * n], shape[1:]) for i in range(len(lst) // n)]


def generate(n: int):
    for i in product(range(1, 1 + n), repeat=n ** 2):
        yield reshape(list(i), [n, n])


def main():
    n = 3
    count = 0
    for num, i in enumerate(generate(n)):
        s = Solver(i)
        try:
            a = s.solve()
            # print('Решение есть', num)
            count += 1
            # a[0].print_board()
        except NoSolution:
            pass
    print(count)


if __name__ == "__main__":
    main()
