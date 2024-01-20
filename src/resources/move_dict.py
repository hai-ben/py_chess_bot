"""A set of dictionaries used to look-up legal pieces for moves"""
from src.resources.move_dict_generator import move_dict_for_vectors

KING_MOVES = move_dict_for_vectors([(1, 1), (-1, 1), (1, -1), (-1, -1),
                                    (1, 0), (-1, 0), (0, -1), (0, 1)])
KNIGHT_MOVES = move_dict_for_vectors([(2, 1), (2, -1), (-2, 1), (-2, -1),
                                    (1, 2), (-1, 2), (1, -2), (-1, -2)])
