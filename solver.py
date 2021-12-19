from hexagon import Color
from board import Board
from copy import deepcopy
from checker import Checker
from hitori_exceptions import NoSolution
from hexagonal_linked_grid import LinkedHexagon


class Solver:
    def __init__(self, values: list[list[int]], required_count_answers: int = None, required_sum: int = None):
        self.board = Board(values)
        self.grid = self.board.grid
        self.lines = self.board.get_lines()
        self.updated = True
        self.required_count_answers = required_count_answers
        self.required_sum = required_sum

    def solve(self) -> list[Board]:
        self._find_between()
        self._find_shadow_hexagon()
        while self.updated:
            self.updated = False
            self._paint_over_in_line()

        indexes = self._permutations()
        answers = []
        self._perm_board(answers, indexes)
        if len(answers) == 0:
            raise NoSolution()
        return answers

    def _perm_board(self, answers: list[Board], indexes: list[tuple[int, int]], index: int = 0) -> None:
        if index == len(indexes):
            if self.required_count_answers is not None and len(answers) >= self.required_count_answers:
                return
            if Checker.check(self.board, self.required_sum):
                answers.append(deepcopy(self.board))
            return

        self.grid.get_by_index(*indexes[index]).color = Color.white
        self._perm_board(answers, indexes, index + 1)
        self.grid.get_by_index(*indexes[index]).color = Color.black
        self._perm_board(answers, indexes, index + 1)

    def _permutations(self) -> list[tuple[int, int]]:
        indexes = []
        grid = self.board.grid
        for x in range(grid.height):
            for y in range(grid.width):
                hexagon = grid.get_by_index(x, y)
                if hexagon.color == Color.gray:
                    indexes.append((x, y))
        return indexes

    def _find_between(self) -> None:
        for line in self.lines:
            for i in range(1, len(line) - 1):
                if line[i - 1] == line[i + 1]:
                    line[i].color = Color.white

    def _find_shadow_hexagon(self) -> None:
        for line in self.lines:
            for i in range(len(line) - 1):
                if line[i] == line[i + 1]:
                    self._find_shadow_hexagon_helper((i, i + 1), line)

    def _find_shadow_hexagon_helper(self, initiators: tuple[int, int], line: list[LinkedHexagon]) -> None:
        for i, hexagon in enumerate(line):
            if i in initiators:
                continue
            if hexagon == line[initiators[0]]:
                self._paint(hexagon, Color.black)

    def _paint_over_in_line(self) -> None:
        for line in self.lines:
            for i, hexagon in enumerate(line):
                if hexagon.color == Color.white:
                    self._paint_over_in_line_helper(i, line)

    def _paint_over_in_line_helper(self, initiator: int, line: iter) -> None:
        for i, hexagon in enumerate(line):
            if initiator == i:
                continue
            if hexagon == line[initiator]:
                self._paint(hexagon, Color.black)

    def _circle_around_black_hexagon(self, hexagon: LinkedHexagon) -> None:
        for neighbor in hexagon.get_neighbors():
            self._paint(neighbor, Color.white)

    def _paint(self, hexagon: LinkedHexagon, color: Color) -> None:
        if hexagon.color != Color.gray and hexagon.color != color:
            raise NoSolution()
        if hexagon.color == color.gray:
            self.updated = True
        hexagon.color = color
        if color == Color.black:
            self._circle_around_black_hexagon(hexagon)
