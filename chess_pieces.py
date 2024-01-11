from enum import Enum

class PlayerColor(Enum):
    WHITE = 1
    BLACK = -1


class Rook():
    ATTACK_VECTORS = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    ATTACK_RANGE = 8
    def __init__(self) -> None:
        pass


class Bishop():
    ATTACK_VECTORS = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
    ATTACK_RANGE = 8
    def __init__(self) -> None:
        pass


class Queen():
    ATTACK_VECTORS = [[1, 0], [-1, 0], [0, 1], [0, -1],
                      [1, 1], [-1, -1], [-1, 1], [1, -1]]
    ATTACK_RANGE = 8
    def __init__(self) -> None:
        pass


class King():
    ATTACK_VECTORS = [[1, 0], [-1, 0], [0, 1], [0, -1],
                      [1, 1], [-1, -1], [-1, 1], [1, -1]]
    ATTACK_RANGE = 1
    def __init__(self) -> None:
        pass


class Knight():
    ATTACK_VECTORS = [[1, 2], [1, -2], [-1, 2], [-1, -2],
                      [2, 1], [2, -1], [-2, 1], [-2, -1]]
    ATTACK_RANGE = 1
    def __init__(self) -> None:
        pass


class Pawn():
    ATTACK_VECTORS = [[1, 1], [-1, 1]]
    ATTACK_RANGE = 1
    def __init__(self) -> None:
        pass
            
