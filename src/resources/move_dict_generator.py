"""Used to generator the move dictionaries in move_dict.py"""
from itertools import product


def move_dict_for_vectors(vectors: list[tuple[int]]) -> dict[int: list[int]]:
    """Generates a dictionary with keys representing a starting tile index, with 
    values a list of possible finishing tile idx's.
    vectors: is a list of possible vectors the pieces can move in (file_direciton, rank_direciton)
    where a->h and 1->8 is positive."""
    moves = {idx_from: [] for idx_from in range(64)}
    for file_direciton, rank_direciton in vectors:
        for start_file, start_rank in product(range(8), range(8)):
            new_file = file_direciton + start_file
            new_rank = rank_direciton + start_rank
            if (7 >= new_file >= 0) and (7 >= new_rank >= 0):
                moves[start_file * 8 + start_rank].append(new_file * 8 + new_rank)
    return moves


def move_dict_for_directions(vectors: list[tuple[int]]) -> dict[int: list[list[int]]]:
    """Very similar to move_dict_for_vectors except the vectors are taken as a direction.
    This direction is taken until it reaches the edge of the board. The nested list
    return structure represents a list for each direction, this way, if something is
    in the way, iteration over this list can be terminated early."""
    moves = {idx_from: [] for idx_from in range(64)}
    for start_file, start_rank in product(range(8), range(8)):
        for file_direciton, rank_direciton in vectors:
            new_moves = []
            for x in range(1, 8):
                new_file = start_file + x * file_direciton
                new_rank = start_rank + x * rank_direciton
                if (7 >= new_file >= 0) and (7 >= new_rank >= 0):
                    new_moves.append(new_file * 8 + new_rank)
            if new_moves:
                moves[start_file * 8 + start_rank].append(new_moves)
    return moves


def pawn_single_move_generator(player_is_white: bool) -> dict[int, tuple]:
    """Generates the instruction set to move a pawn forward"""
    if player_is_white:
        moves = {idx: (idx, 1, idx - 8, 0) for idx in range(55, 15, -1)}
        for idx in range(14, 7, -1):
            move_tuples = []
            for piece in range(2, 6):
                move_tuples.append(((idx, 1, idx, piece), (idx, piece, idx - 8, 0)))
            moves[idx] = tuple(move_tuples)
        return moves
    moves = {idx: (idx, 7, idx + 8, 0) for idx in range(8, 48)}
    for idx in range(48, 56):
        move_tuples = []
        for piece in range(8, 12):
            move_tuples.append(((idx, 7, idx, piece), (idx, piece, idx + 8, 0)))
        moves[idx] = tuple(move_tuples)
    return moves