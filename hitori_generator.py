import random

from board import Board
from checker import Checker
from hexagon import Color
from hexagonal_linked_grid import Direction, LinkedHexagon


class Generator:

    def __init__(self, size: int):
        self.size = size
        self.board = None

    def generate(self) -> list[list[int]]:
        while True:
            try:
                self.generate_empty_color_field()
                self.fill_field_with_numbers()
                return self.convert_matrix_to_list(self.board.grid.matrix)
            except IndexError:
                pass

    def generate_empty_color_field(self) -> None:
        matrix = [[0] * self.size for _ in range(self.size)]
        self.board = Board(matrix)
        grid = self.board.grid
        max_count = self.get_max_count_black_hexagon()
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
            self.clear_board()

    def fill_field_with_numbers(self) -> None:
        grid = self.board.grid
        for x in range(grid.height):
            for y in range(grid.width):
                h = grid.get_by_index(x, y)
                if h.color == Color.gray:
                    h.value = list(range(1, self.size + 1))

        for hexagon in self.get_next_hexagon():
            hexagon.value = random.choice(hexagon.value)
            hexagon.color = Color.white
            for h in self.get_all_lines_from_hexagon(hexagon):
                if h.color == Color.gray and hexagon.value in h.value:
                    h.value.remove(hexagon.value)

        for x in range(grid.height):
            for y in range(grid.width):
                h = grid.get_by_index(x, y)
                if h.color == Color.black:
                    h.value = random.randint(1, self.size)

    def get_max_count_black_hexagon(self) -> int:
        a, b = divmod(self.size, 3)
        max_count_black_hexagon = a * self.size
        if b == 2:
            max_count_black_hexagon += self.size
        elif b == 1:
            max_count_black_hexagon += self.size // 2
        return max_count_black_hexagon

    def get_next_hexagon(self) -> iter:
        grid = self.board.grid
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

    def clear_board(self) -> None:
        grid = self.board.grid
        for x in range(grid.height):
            for y in range(grid.width):
                if hexagon := grid.get_by_index(x, y):
                    hexagon.color = Color.gray

    @staticmethod
    def get_line(hexagon: LinkedHexagon, direction: Direction) -> list:
        result = []
        while hexagon := getattr(hexagon, direction.value):
            result.append(hexagon)
        return result

    @staticmethod
    def get_all_lines_from_hexagon(hexagon: LinkedHexagon) -> iter:
        for direction in Direction:
            yield from Generator.get_line(hexagon, direction)

    @staticmethod
    def convert_matrix_to_list(matrix: list[list[LinkedHexagon]]) -> list[list[int]]:
        result = []
        for line in matrix:
            result.append(list(map(lambda h: h.value, line)))
        return result


def main():
    gen = Generator(5)
    print(gen.generate())


if __name__ == "__main__":
    main()
