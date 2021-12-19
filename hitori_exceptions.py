from hexagonal_linked_grid import LinkedHexagon


class NoSolution(Exception):
    pass


class RecolorException(NoSolution):

    def __init__(self, hexagon_initiator: LinkedHexagon):
        self.hexagon_initiator = hexagon_initiator
