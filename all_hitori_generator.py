import random
from itertools import product
from functools import reduce
from operator import mul
from solver import Solver, NoSolution
from hexagonal_linked_grid import Grid
from hexagon import Color


def reshape(lst, shape):
    if len(shape) == 1:
        return lst
    n = reduce(mul, shape[1:])
    return [reshape(lst[i * n:(i + 1) * n], shape[1:]) for i in range(len(lst) // n)]


def generate(n: int):
    for i in product(range(1, 1 + n), repeat=n ** 2):
        yield reshape(list(i), [n, n])


def random_generate(n: int):
    while True:
        lst = random.choices(list(range(1, 1 + n)), k=n ** 2)
        yield reshape(lst, [n, n])


def clear_board(grid: Grid) -> None:
    for x in range(grid.height):
        for y in range(grid.width):
            if hexagon := grid.get_by_index(x, y):
                hexagon.color = Color.gray


def main():
    n = 3
    count = 0
    for num, i in enumerate(random_generate(n)):
        if num % 100 == 0:
            print(num)
        s = Solver(i, 1)
        try:
            a = s.solve()
            a[0].print_board()
            clear_board(a[0].grid)
            a[0].print_board()
            print('Решение есть', num)
            count += 1
            # a[0].print_board()
        except NoSolution:
            pass
    print(count)


if __name__ == "__main__":
    main()
