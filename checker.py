from board import Board
from hexagon import Color
from collections import Counter
from hexagonal_linked_grid import LinkedHexagon, Grid


class Checker:
    @staticmethod
    def check(board: Board, required_sum: int | None) -> bool:
        if Checker._has_two_white_equals_number_in_line(board.get_lines()):
            return False
        if Checker.has_near_two_black_hexagons(board.grid):
            return False
        if required_sum is None:
            return True
        return Checker._sum_in_lines_less_than_required_sum(board.get_lines(), required_sum)

    @staticmethod
    def _has_two_white_equals_number_in_line(lines: list[list[LinkedHexagon]]) -> bool:
        for line in lines:
            numbers = Counter()
            for hexagon in line:
                if hexagon.color == Color.white:
                    numbers[hexagon.value] += 1
            if len(numbers) > 0 and numbers.most_common(1)[0][1] > 1:
                return True
        return False

    @staticmethod
    def has_near_two_black_hexagons(grid: Grid) -> bool:
        for x in range(grid.height):
            for y in range(grid.width):
                if hexagon := grid.get_by_index(x, y):
                    if hexagon.color == Color.black and \
                            any(map(lambda h: h.color == Color.black, hexagon.get_neighbors())):
                        return True
        return False

    @staticmethod
    def _sum_in_lines_less_than_required_sum(lines: list[list[LinkedHexagon]], req_sum: int) -> bool:
        for line in lines:
            white_hexagons = filter(lambda x: x.color == Color.white, line)
            cur_sum = sum(map(lambda x: x.value, white_hexagons))
            if cur_sum > req_sum:
                return False
        return True
