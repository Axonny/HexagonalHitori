import random
from operator import mul
from solver import Solver
from hexagonal_linked_grid import Grid, Direction, LinkedHexagon
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


def get_line(hexagon, direction: Direction) -> list:
    result = []
    while hexagon := getattr(hexagon, direction.value):
        result.append(hexagon)
    return result


def get_all_lines_from_hexagon(hexagon):
    for direction in Direction:
        yield from get_line(hexagon, direction)


def generate_empty_color_field(n: int):
    matrix = [[0]*n for i in range(n)]
    b = Board(matrix)
    grid = b.grid
    max_count = get_max_count_black_hexagon(n)
    while True:
        count = random.randint(max_count // 2, max_count)
        count_black = 0
        while count_black < count:
            x = random.randint(0, grid.height - 1)
            y = random.randint(0, grid.width - 1)
            hexagon = grid.get_by_index(x, y)
            if hexagon.color == Color.black:
                continue
            hexagon.color = Color.black
            count_black += 1
        if not Checker.has_near_two_black_hexagons(grid):
            break
        clear_board(grid)
    for x in range(grid.height):
        for y in range(grid.width):
            h = grid.get_by_index(x, y)
            if h.color == Color.gray:
                h.value = list(range(1, n + 1))

    for hexagon in get_next_hexagon(grid):
        hexagon.value = random.choice(hexagon.value)
        hexagon.color = Color.white
        for h in get_all_lines_from_hexagon(hexagon):
            if h.color == Color.gray and hexagon.value in h.value:
                h.value.remove(hexagon.value)

    for x in range(grid.height):
        for y in range(grid.width):
            h = grid.get_by_index(x, y)
            if h.color == Color.black:
                h.value = random.randint(1, n)

    return b


def _is_hexagon_can_be_shadow(hexagon):
    for direction in Direction:
        line = get_line(hexagon, direction)
        for i in range(1, len(line)):
            if line[i] == line[i - 1]:
                pass


def get_next_hexagon(grid: Grid):
    while True:
        min_hexagon = None
        min_len = float("+inf")
        for x in range(grid.height):
            for y in range(grid.width):
                h = grid.get_by_index(x, y)
                if h.color == Color.gray:
                    if len(h.value) < min_len:
                        min_hexagon = h
                        min_len = len(h.value)
        if min_hexagon is None:
            return
        yield min_hexagon


def convert_matrix_to_list(matrix: list[list[LinkedHexagon]]) -> list[list[int]]:
    result = []
    for line in matrix:
        result.append(list(map(lambda h: h.value, line)))
    return result

def main():
    while True:
        try:
            a = generate_empty_color_field(5)
            a.print_board()
            print(Checker.check(a, None))
            clear_board(a.grid)
            a.print_board()
            s = Solver(convert_matrix_to_list(a.grid.matrix), 1)
            b = s.solve()
            b[0].print_board()
            break
        except NoSolution:
            print("NoSolution")
            break
        except:
            pass


if __name__ == "__main__":
    main()
