from board import Board
from hexagon import Color
from collections import Counter
from hexagonal_linked_grid import LinkedHexagon, Grid


class Checker:
    @staticmethod
    def check(board: Board, possible_graph_components: int) -> bool:
        if Checker._has_two_white_equals_number_in_line(board.get_lines()):
            return False
        if Checker._has_near_two_black_hexagons(board.grid):
            return False
        count_components = Checker._count_graph_components(board.grid)
        return count_components <= possible_graph_components

    @staticmethod
    def _has_two_white_equals_number_in_line(lines: list[list[LinkedHexagon]]) -> bool:
        for line in lines:
            numbers = Counter()
            for hexagon in line:
                if hexagon.color == Color.white:
                    numbers[hexagon.value] += 1
            if len(numbers) == 0 or numbers.most_common(1)[0][1] > 1:
                return True
        return False

    @staticmethod
    def _has_near_two_black_hexagons(grid: Grid) -> bool:
        for x in range(grid.height):
            for y in range(grid.width):
                if hexagon := grid.get_by_index(x, y):
                    if hexagon.color == Color.black and \
                            any(map(lambda h: h.color == Color.black, hexagon.get_neighbors())):
                        return True
        return False

    @staticmethod
    def _count_graph_components(grid: Grid) -> int:
        count = 0
        visited = set()
        for x in range(grid.height):
            for y in range(grid.width):
                if hexagon := grid.get_by_index(x, y):
                    if hexagon.color == Color.white and hexagon not in visited:
                        Checker._dfs(visited, hexagon)
                        count += 1
        return count

    @staticmethod
    def _dfs(visited: set[LinkedHexagon], hexagon: LinkedHexagon) -> None:
        visited.add(hexagon)
        for neighbor in filter(lambda h: h.color == Color.white, hexagon.get_neighbors()):
            if neighbor not in visited:
                Checker._dfs(visited, neighbor)
