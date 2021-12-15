from enum import Enum


class Color(Enum):
    gray = "_"
    white = " "
    black = "░"


class Hexagon:

    def __init__(self, value: int, color: Color = None):
        self.value = value
        self.color = color
        if color is None:
            self.color = Color.gray

    def __str__(self):
        if self.color == Color.black:
            return Color.black.value * 2
        return str(self.value)

    def __format__(self, format_spec):
        return format(str(self), format_spec)

    def __eq__(self, other):
        return isinstance(other, Hexagon) and self.value == other.value

    def __repr__(self):
        return f"Hexagon({self.value}, {self.color})"
