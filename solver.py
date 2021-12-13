from ceil import Color
from board import Board
from copy import deepcopy
from checker import Checker
from hexagonal_linked_grid import LinkedHexagon


class NoSolution(Exception):
    pass


class Solver:
    def __init__(self, values: list[list[int]]):
        self.board = Board(values)
        self.grid = self.board.grid
        self.lines = self.board.get_lines()
        self.updated = True

    def solve(self) -> list[Board]:
        self.find_between()
        self._find_shadow_hexagon()
        while self.updated:
            self.updated = False
            self.paint_over_in_line()

        indexes = self.permutations()
        answers = []
        self.perm_board(answers, indexes)
        if len(answers) == 0:
            raise NoSolution()
        return answers

    def perm_board(self, answers: list[Board], indexes: list[tuple[int, int]], index: int = 0):
        if index == len(indexes):
            if Checker.check(self.board, 1):
                answers.append(deepcopy(self.board))
            return

        self.grid.get_by_index(*indexes[index]).color = Color.white
        self.perm_board(answers, indexes, index + 1)
        self.grid.get_by_index(*indexes[index]).color = Color.black
        self.perm_board(answers, indexes, index + 1)

    def permutations(self) -> list[tuple[int, int]]:
        indexes = []
        grid = self.board.grid
        for x in range(grid.height):
            for y in range(grid.width):
                if hexagon := grid.get_by_index(x, y):
                    if hexagon.color == Color.gray:
                        indexes.append((x, y))
        return indexes

    def find_between(self):
        for line in self.lines:
            for i in range(1, len(line) - 1):
                if line[i - 1] == line[i + 1]:
                    line[i].color = Color.white

    def _find_shadow_hexagon(self):
        for line in self.lines:
            for i in range(len(line) - 1):
                if line[i] == line[i + 1]:
                    self._find_shadow_hexagon_helper((i, i + 1), line)

    def _find_shadow_hexagon_helper(self, initiators: tuple[int, int], line: iter) -> None:
        for i, hexagon in enumerate(line):
            if i in initiators:
                continue
            if hexagon == line[initiators[0]]:
                self._try_paint(hexagon, Color.black)

    def paint_over_in_line(self):
        for line in self.lines:
            for i, hexagon in enumerate(line):
                if hexagon.color == Color.white:
                    self._paint_over_in_line_helper(i, line)

    def _paint_over_in_line_helper(self, initiator: int, line: iter):
        for i, hexagon in enumerate(line):
            if initiator == i:
                continue
            if hexagon == line[initiator]:
                self._try_paint(hexagon, Color.black)

    def _circle_around_black_hexagon(self, hexagon: LinkedHexagon):
        for neighbor in hexagon.get_neighbors():
            self._try_paint(neighbor, Color.white)

    def _try_paint(self, hexagon: LinkedHexagon, color: Color):
        if hexagon.color != Color.gray and hexagon.color != color:
            raise NoSolution()
        if hexagon.color == color.gray:
            self.updated = True
        hexagon.color = color
        if color == Color.black:
            self._circle_around_black_hexagon(hexagon)


if __name__ == "__main__":
    l = [[1, 1, 2], [3, 2, 3], [3, 3, 3]]

    s = Solver(l)
    s.board.print_board()
    a = s.solve()
    print(a)
    a = a[0]
    a.print_board()
