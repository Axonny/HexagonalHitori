from hexagon import Hexagon, Color
from enum import Enum


class Direction(Enum):
    up = "up"
    down = "down"
    left_up = "left_up"
    left_down = "left_down"
    right_up = "right_up"
    right_down = "right_down"


class LinkedHexagon(Hexagon):
    def __init__(self, value: int, color: Color = None):
        super().__init__(value, color)
        self.up = None
        self.down = None
        self.left_up = None
        self.left_down = None
        self.right_up = None
        self.right_down = None

    def get_neighbors(self):
        yield from filter(None, [self.up, self.down, self.left_up, self.left_down, self.right_up, self.right_down])

    def __hash__(self):
        return id(self)


class Grid:
    def __init__(self, values: list[list[int]]):
        self.matrix = [[LinkedHexagon(value) for value in values[i]] for i in range(len(values))]
        self.width = len(values)
        self.height = len(values[0])
        self._link_grid()

    def _link_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                hexagon = self.matrix[i][j]
                hexagon.up = self.get_by_index(i - 1, j)
                hexagon.down = self.get_by_index(i + 1, j)
                if j % 2 == 0:
                    hexagon.left_up = self.get_by_index(i - 1, j - 1)
                    hexagon.left_down = self.get_by_index(i, j - 1)
                    hexagon.right_up = self.get_by_index(i - 1, j + 1)
                    hexagon.right_down = self.get_by_index(i, j + 1)
                else:
                    hexagon.left_up = self.get_by_index(i, j - 1)
                    hexagon.left_down = self.get_by_index(i + 1, j - 1)
                    hexagon.right_up = self.get_by_index(i, j + 1)
                    hexagon.right_down = self.get_by_index(i + 1, j + 1)

    def get_by_index(self, x: int, y: int) -> LinkedHexagon | None:
        if 0 <= x < self.height and 0 <= y < self.width:
            return self.matrix[x][y]
        return None

    def get_line(self, x: int, y: int, direction: Direction) -> list[LinkedHexagon]:
        hexagon = self.matrix[x][y]
        result = [hexagon]
        while hexagon := getattr(hexagon, direction.value):
            result.append(hexagon)
        return result
