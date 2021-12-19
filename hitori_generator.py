import random
from operator import mul
from solver import Solver
from hexagonal_linked_grid import Grid, Direction
from board import Board
from hexagon import Color
from functools import reduce
from checker import Checker
from hitori_exceptions import RecolorException, NoSolution


def reshape(lst, shape):
    if len(shape) == 1:
        return lst
    n = reduce(mul, shape[1:])
    return [reshape(lst[i * n:(i + 1) * n], shape[1:]) for i in range(len(lst) // n)]


def random_generate_field(n: int) -> list[list[int]]:
    lst = random.choices(list(range(1, 1 + n)), k=n ** 2)
    return reshape(lst, [n, n])


def clear_board(grid: Grid) -> None:
    for x in range(grid.height):
        for y in range(grid.width):
            if hexagon := grid.get_by_index(x, y):
                hexagon.color = Color.gray


def regenerate_board(n: int, grid: Grid) -> None:
    for x in range(grid.height):
        for y in range(grid.width):
            if hexagon := grid.get_by_index(x, y):
                if hexagon.color != Color.white:
                    hexagon.value = random.randint(1, n)
                    hexagon.color = Color.gray


def generate_standard_field(n: int) -> list[list[int]]:
    data = [0] * (n ** 2)
    for r in range(n):
        for c in range(n):
            data[c + r * n] = (c + r) % n + 1
    return reshape(data, [n, n])


def extend_field(max_num, field: list[list[int]]) -> list[list[int]]:
    n = len(field) + 1
    for line in field:
        line.append(random.randint(1, max_num))
    field.append(random.choices(range(1, max_num + 1), k=n))
    return field


def layer_generator(n: int):
    field = [[random.randint(1, n)]]
    for _ in range(1, n):
        print(field)
        extend_field(n, field)
        while True:
            s = Solver(field, 1)
            try:
                s.solve()
                break
            except NoSolution:
                for line in field:
                    line[-1] = random.randint(1, n)
                field[-1] = random.choices(range(1, n + 1), k=len(field))
    return field


def generate_right_hitori(n: int):
    init_board = random_generate_field(n)
    s = Solver(init_board, 1)
    for i in range(50):
        try:
            s.solve()
            return s.grid.matrix
        except RecolorException as e:
            print("RecolorException")
            e.hexagon_initiator.color = Color.gray
            s.board.print_board()
            regenerate_board(n, s.grid)
            clear_board(s.grid)
        except NoSolution:
            print("NoSolution")
            return generate_right_hitori(n)


def get_max_count_black_hexagon(n: int) -> int:
    a, b = divmod(n, 3)
    max_count_black_hexagon = a * n
    if b == 2:
        max_count_black_hexagon += n
    elif b == 1:
        max_count_black_hexagon += n // 2
    return max_count_black_hexagon


def get_all_lines_from_hexagon(grid: Grid, x: int, y: int):
    line1 = grid.get_line(x, y, Direction.up)
    line2 = grid.get_line(x, y, Direction.down)
    line3 = grid.get_line(x, y, Direction.left_up)
    line4 = grid.get_line(x, y, Direction.left_down)
    line5 = grid.get_line(x, y, Direction.right_up)
    line6 = grid.get_line(x, y, Direction.right_down)
    return line1 + line2 + line3 + line4 + line5 + line6


def generate_empty_color_field(n: int):
    matrix = [[0]*n for i in range(n)]
    b = Board(matrix)
    grid = b.grid
    max_count = get_max_count_black_hexagon(n)
    while True:
        count = random.randint(max_count // 2, max_count)
        for i in range(count):
            x = random.randint(0, grid.height - 1)
            y = random.randint(0, grid.width - 1)
            hexagon = grid.get_by_index(x, y)
            hexagon.color = Color.black
        if not Checker.has_near_two_black_hexagons(grid):
            break
        clear_board(grid)
    for x in range(grid.height):
        for y in range(grid.width):
            h = grid.get_by_index(x, y)
            if h.color == Color.black:
                continue
            possible_numbers = list(range(1, n + 1))
            for hexagon in get_all_lines_from_hexagon(grid, x, y):
                if hexagon.color == Color.white and hexagon.value in possible_numbers:
                    possible_numbers.remove(hexagon.value)
            if len(possible_numbers) == 0:
                return generate_empty_color_field(n)
            h.value = random.choice(possible_numbers)
            h.color = Color.white
    return b


def main():
    a = generate_empty_color_field(8)
    a.print_board()
    print(Checker.check(a, None))


if __name__ == "__main__":
    main()
