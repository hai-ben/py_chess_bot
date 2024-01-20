"""A set of dictionaries used to look-up legal pieces for moves"""
from itertools import product
from src.resources.move_dict_generator import move_dict_for_vectors, move_dict_for_directions,\
    pawn_single_move_generator

KING_MOVES = move_dict_for_vectors([(1, 1), (-1, 1), (1, -1), (-1, -1),
                                    (1, 0), (-1, 0), (0, -1), (0, 1)])
KNIGHT_MOVES = move_dict_for_vectors([(2, 1), (2, -1), (-2, 1), (-2, -1),
                                    (1, 2), (-1, 2), (1, -2), (-1, -2)])
BISHOP_MOVES = move_dict_for_directions([(1, 1), (-1, 1), (1, -1), (-1, -1)])
ROOK_MOVES = move_dict_for_directions([(0, 1), (-1, 0), (0, -1), (1, 0)])
QUEEN_MOVES = move_dict_for_directions(set(product((-1, 0, 1), repeat=2)) - set([(0,0)]))
PAWN_SINGLE_MOVES_WHITE = pawn_single_move_generator(True)
PAWN_SINGLE_MOVES_BLACK = pawn_single_move_generator(False)
PAWN_DOUBLE_MOVES_WHITE = {idx: (idx, 1, idx - 16, 0) for idx in range(55, 47, -1)}
PAWN_DOUBLE_MOVES_BLACK = {idx: (idx, 7, idx + 16, 0) for idx in range(8, 16)}
