from enum import Enum

class PlayerColor(Enum):
    WHITE = 1
    BLACK = -1


class ChessPiece:
    def __init__(self, player_color: PlayerColor, position) -> None:
        self.attack_range = 8
        self.attack_vectors = []
        self.has_moved = False
        self.position = position
        self.player = player_color
        self.move_range = 8
        self.move_vectors = []
        self.moves = set()
        self.attacks = set()
    
    def move_or_attack(self) -> None:
        self.has_moved = True
    
    def get_sprite(self):
        # TODO
        pass


class Rook(ChessPiece):
    ATTACK_VECTORS = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    ATTACK_RANGE = 8
    def __init__(self, player_color: PlayerColor) -> None:
        super().__init__(player_color)
        self.attack_vectors = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.move_vectors = self.attack_vectors


class Bishop(ChessPiece):
    ATTACK_VECTORS = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
    ATTACK_RANGE = 8
    def __init__(self, player_color: PlayerColor) -> None:
        super().__init__(player_color)
        self.attack_vectors = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
        self.move_vectors = self.attack_vectors


class Queen(ChessPiece):
    ATTACK_VECTORS = [[1, 0], [-1, 0], [0, 1], [0, -1],
                      [1, 1], [-1, -1], [-1, 1], [1, -1]]
    ATTACK_RANGE = 8
    def __init__(self, player_color: PlayerColor) -> None:
        super().__init__(player_color)
        self.attack_vectors = [[1, 0], [-1, 0], [0, 1], [0, -1],
                               [1, 1], [-1, -1], [-1, 1], [1, -1]]
        self.move_vectors = self.attack_vectors


class King(ChessPiece):
    ATTACK_VECTORS = [[1, 0], [-1, 0], [0, 1], [0, -1],
                      [1, 1], [-1, -1], [-1, 1], [1, -1]]
    ATTACK_RANGE = 1
    def __init__(self, player_color: PlayerColor) -> None:
        super().__init__(player_color)
        self.attack_range = 1
        self.attack_vectors = [[1, 0], [-1, 0], [0, 1], [0, -1],
                               [1, 1], [-1, -1], [-1, 1], [1, -1]]
        self.move_range = 1
        self.move_vectors = self.attack_vectors


class Knight(ChessPiece):
    ATTACK_VECTORS = [[1, 2], [1, -2], [-1, 2], [-1, -2],
                      [2, 1], [2, -1], [-2, 1], [-2, -1]]
    ATTACK_RANGE = 1
    def __init__(self, player_color: PlayerColor) -> None:
        super().__init__(player_color)
        self.attack_range = 1
        self.attack_obstructed = False
        self.attack_vectors = [[1, 2], [1, -2], [-1, 2], [-1, -2],
                               [2, 1], [2, -1], [-2, 1], [-2, -1]]
        self.move_range = 1
        self.move_obstructed = False
        self.move_vectors = self.attack_vectors


class Pawn(ChessPiece):
    ATTACK_VECTORS = [[1, 1], [-1, 1]]
    ATTACK_RANGE = 1
    def __init__(self, player_color: PlayerColor) -> None:
        super().__init__(player_color)
        self.attack_range = 1
        self.attack_vectors = [[1, 1], [-1, 1]]
        self.move_range = 2
        self.move_vectors = [[0, 1]]
    
    def move_or_attack(self) -> None:
        self.move_range = 1
        return super().move_or_attack()
            
