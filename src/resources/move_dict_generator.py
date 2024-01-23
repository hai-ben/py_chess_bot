"""Used to generator the move dictionaries in move_dict.py"""
from itertools import product

W_PAWN_BISHOP_QUEEN_KING = {1, 3, 5, 6}
W_BISHOP_QUEEN_KING = {3, 5, 6}
W_BISHOP_QUEEN = {3, 5}
W_ROOK_QUEEN_KING = {4, 5, 6}
W_ROOK_QUEEN = {4, 5}

B_PAWN_BISHOP_QUEEN_KING = {7, 9, 11, 12}
B_BISHOP_QUEEN_KING = {9, 11, 12}
B_BISHOP_QUEEN = {9, 11}
B_ROOK_QUEEN_KING = {10, 11, 12}
B_ROOK_QUEEN = {10, 11}


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


def move_dict_for_directions(vectors: list[tuple[int]]) -> dict[int, list[list[int]]]:
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


def make_blockable_attacks_dict(player_is_white: bool)\
        -> dict[int, list[list[tuple[int, set[int]]]]]:
    """Makes a dictionary lookup that helps determine if a tile is being attacked.
    The key to the dictionary represents the square being attacked.
    The value represents a list of directions that the square can be attacked from.
    Each entry in the list is tuple of squares that a piece in the set
    can attack the start square from. This allows aborting a direction and moving to
    the next if a blocking piece is found.
    Essentially the return dict for the white player will have entries like:
    {e4: [[(e5 {rook, queen, king}), (e6 {rook, queen}),...], [(f5, {pawn, bishop...}),...]...]}

    For performance reasons knight attacks are stored in a seperate dict to avoid
    excessive loop instaniating as each single attack would be it's own direction.
    """
    attack_dict = {}
    # This represents cardinal directions on the board to consider
    directions = [(1, 0), (0, 1), (0, -1), (-1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]
    # threats[idx] represents the pieces that can threaten a square
    # in the direction directions[idx]. The tuple represents the pieces that are
    # (threatening_at_distance_1, threatening_at_any_unblocked_distance)
    if player_is_white:
        threats = [(W_ROOK_QUEEN_KING, W_ROOK_QUEEN)] * 4\
                + [(W_PAWN_BISHOP_QUEEN_KING, W_BISHOP_QUEEN)] * 2\
                + [(W_BISHOP_QUEEN_KING, W_BISHOP_QUEEN)] * 2
    else:
        threats = [(B_ROOK_QUEEN_KING, B_ROOK_QUEEN)] * 4\
                + [(B_BISHOP_QUEEN_KING, B_BISHOP_QUEEN)] * 2\
                + [(B_PAWN_BISHOP_QUEEN_KING, B_BISHOP_QUEEN)] * 2
    for square_idx in range(64):
        start_rank, start_file = square_idx // 8, square_idx % 8
        attack_dict[square_idx] = []
        # For all the directions remembering a8 = 0, h1 = 63
        for (file_direciton, rank_direction), (close_threats, far_threats)\
                in zip(directions, threats):
            attack_on_direction = []
            for i in range(1, 8):
                new_file = start_file + i * file_direciton
                new_rank = start_rank + i * rank_direction
                if not ((0 <= new_file <= 7) and (0 <= new_rank <= 7)):
                    break
                if i == 1:
                    attack_on_direction.append((new_rank * 8 + new_file, close_threats))
                else:
                    attack_on_direction.append((new_rank * 8 + new_file, far_threats))
            if attack_on_direction:
                attack_dict[square_idx].append(attack_on_direction)
    return attack_dict
