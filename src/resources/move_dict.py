"""A set of dictionaries used to look-up legal pieces for moves"""
from itertools import product
from src.resources.move_dict_generator import move_dict_for_vectors, move_dict_for_directions,\
    pawn_single_move_generator, make_blockable_attacks_dict, unblockable_attacking_tiles,\
    blocking_moves, generate_vector_to_square_from_lookup, generate_moves_from_square_along_vector

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
BLOCKABLE_ATTACK_DICT_WHITE = make_blockable_attacks_dict(True)
BLOCKABLE_ATTACK_DICT_BLACK = make_blockable_attacks_dict(False)

UNBLOCKABLE_ATTACKS_AT = unblockable_attacking_tiles()
MOVES_TO_BLOCK_ATTACK_ON_FROM = blocking_moves()
VECTOR_TO_SQUARE_FROM = generate_vector_to_square_from_lookup()
MOVES_FROM_SQUARE_ALONG_VECTOR = generate_moves_from_square_along_vector()

WHITE_THREATS_IN_DIRECTION = {
    (1, 1): {3, 5},
    (-1, 1): {3, 5},
    (1, -1): {3, 5},
    (-1, -1): {3, 5},
    (1, 0): {4, 5},
    (-1, 0): {4, 5},
    (0, -1): {4, 5},
    (0, 1): {4, 5}
}

BLACK_THREATS_IN_DIRECTION = {
    (1, 1): {9, 11},
    (-1, 1): {9, 11},
    (1, -1): {9, 11},
    (-1, -1): {9, 11},
    (1, 0): {10, 11},
    (-1, 0): {10, 11},
    (0, -1): {10, 11},
    (0, 1): {10, 11}
}
