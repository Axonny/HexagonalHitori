import math
from hexagonal_linked_grid import Grid, Direction


class Board:

    def __init__(self, values: list[list[int]]):
        self.grid = Grid(values)
        self.h = len(values)
        self.w = len(values[0])

    def get_lines(self):
        up_down = [self.grid.get_line(0, i, Direction.down) for i in range(self.w)]
        right_down = [self.grid.get_line(i, 0, Direction.right_down) for i in range(self.h)] + \
                     [self.grid.get_line(0, i, Direction.right_down) for i in range(2, self.w, 2)]
        right_up = [self.grid.get_line(i, 0, Direction.right_up) for i in range(self.h)] + \
                   [self.grid.get_line(self.h - 1, i, Direction.right_down) for i in range(1, self.w, 2)]

        return up_down + right_down + right_up

    def print_board(self) -> None:
        print("", "__    " * math.ceil(self.w / 2))
        for j, line in enumerate(self.grid.matrix):
            result = ""
            for i in range(0, len(line), 2):
                result += fr"/{line[i]:<2}\__"
            if self.w % 2 != 0:
                result = result[:-2]
            elif j != 0:
                result += "/"
            result += '\n'
            for i in range(1, len(line), 2):
                result += fr"\__/{line[i]:<2}"
            result += r"\__/" if self.w % 2 == 1 else "\\"
            print(result)
        print(" ", end='')
        for i in range(self.w // 2):
            print(r"  \__/", end='')
        print()


if __name__ == "__main__":
    b = [[4 * i + j for j in range(4)] for i in range(4)]
    board = Board(b)
    board.print_board()
    print(*board.get_lines(), sep='\n')
