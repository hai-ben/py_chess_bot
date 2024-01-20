"""A set of constants/lookups to translate from chess-terms to the engine data structure"""
from itertools import product

SQUARE_IDX = {file + rank: idx for idx, (file, rank) in enumerate(product("abcdefgh", "87654321"))}
B_KING_IDX = 64
W_KING_IDX = 65
CASTLE_IDX = 66
EP_IDX = 67
TURN_IDX = 68

SQUARE_STATES = {
    "empty": 0,
    "w_pawn": 1, "w_knight": 2, "w_bishop": 3, "w_rook": 4, "w_queen": 5, "w_king": 6,
    "b_pawn": 7, "b_knight": 8, "b_bishop": 9, "b_rook": 10, "b_queen": 11, "b_king": 12
}

CASTLE_STATES = {
    "w_short": 0b0001,
    "w_long": 0b0010,
    "b_short": 0b0100,
    "b_long": 0b1000
}

EP_FILE = {None: -1} | {file_name: int(idx) for file_name, idx in zip("abcdefgh", "01234567")}

PLAYER_TURN = {"white": True, "black": False}
