"""The code used to generate move_set_generators.py"""
from collections import defaultdict
from src.prototyping.chess_pieces import King, Knight
from src.prototyping.small_board import SmallBoard, FILE_NAME, RANK_NAME



def make_check_dict() -> dict[int, dict[str, list[list[tuple[str, set]]]]]:
    """e.g. SKIPABLE_THREAT_DICT[player][tile] =\
      [[(tile1, threat_set)], [(tile2, threat_set2), (tile3, threat_set3)]]"""
    # Add horizontals
    skipable_threat_dict = {1: defaultdict(list), 0: defaultdict(list)}
    for vector in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        for start_file, start_file_name in FILE_NAME.items():
            for start_rank, start_rank_name in RANK_NAME.items():
                from_tile = start_file_name + start_rank_name
                move_list = []
                for i in range(1, 8):
                    new_file = start_file + i * vector[0]
                    if new_file > 7 or new_file < 0:
                        break
                    new_rank = start_rank + i * vector[1]
                    if new_rank > 7 or new_rank < 0:
                        break
                    to_tile = f"{FILE_NAME[new_file]}{RANK_NAME[new_rank]}"
                    move_list.append((to_tile, "ROOK_QUEEN_KING" if i == 1 else "ROOK_QUEEN"))
                if move_list:
                    skipable_threat_dict[1][from_tile].append(move_list)
                    skipable_threat_dict[0][from_tile].append(move_list)

    # Add Diagonals
    for vector in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        for start_file, start_file_name in FILE_NAME.items():
            for start_rank, start_rank_name in RANK_NAME.items():
                from_tile = start_file_name + start_rank_name
                for player in [0, 1]:
                    move_list = []
                    for i in range(1, 8):
                        new_file = start_file + i * vector[0]
                        if new_file > 7 or new_file < 0:
                            break
                        new_rank = start_rank + i * vector[1]
                        if new_rank > 7 or new_rank < 0:
                            break
                        to_tile = f"{FILE_NAME[new_file]}{RANK_NAME[new_rank]}"
                        if i == 1:
                            player_dir = 1 if player else -1
                            if player_dir == vector[1]:
                                move_list.append((to_tile, "PAWN_BISHOP_QUEEN_KING"))
                            else:
                                move_list.append((to_tile, "BISHOP_QUEEN_KING"))
                        else:
                            move_list.append((to_tile, "BISHOP_QUEEN"))
                    if move_list:
                        skipable_threat_dict[player][from_tile].append(move_list)

    # Add horses
    for vector in [(1, 2), (-1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1)]:
        for start_file, start_file_name in FILE_NAME.items():
            for start_rank, start_rank_name in RANK_NAME.items():
                from_tile = start_file_name + start_rank_name
                move_list = []
                new_file = start_file + vector[0]
                if new_file > 7 or new_file < 0:
                    continue
                new_rank = start_rank + vector[1]
                if new_rank > 7 or new_rank < 0:
                    continue
                to_tile = f"{FILE_NAME[new_file]}{RANK_NAME[new_rank]}"
                move_list.append((to_tile, "Knight"))
                skipable_threat_dict[1][from_tile].append(move_list)
                skipable_threat_dict[0][from_tile].append(move_list)
    return skipable_threat_dict


def make_knight_move_dict() -> dict[str, list[str]]:
    """Gets all the knight moves at each tile"""
    moves = {}
    for file_name in FILE_NAME.values():
        for rank_name in RANK_NAME.values():
            from_tile = file_name + rank_name
            new_board = SmallBoard()
            new_board.set_tile_to(from_tile, Knight, 1)
            raw_moves = list(new_board.get_all_moves().keys())
            moves[from_tile] = [move[3:] for move in raw_moves]
    return moves


def make_moves_for_piece(piece: type) -> dict[str, list[list[str]]]:
    """Gets all the moves for piece at each square"""
    moves = defaultdict(list)
    for vector in piece.ATTACK_VECTORS:
        for start_file, start_file_name in FILE_NAME.items():
            for start_rank, start_rank_name in RANK_NAME.items():
                from_tile = start_file_name + start_rank_name
                move_list = []
                for i in range(1, piece.ATTACK_RANGE + 1):
                    new_file = start_file + i * vector[0]
                    if new_file > 7 or new_file < 0:
                        break
                    new_rank = start_rank + i * vector[1]
                    if new_rank > 7 or new_rank < 0:
                        break
                    to_tile = f"{FILE_NAME[new_file]}{RANK_NAME[new_rank]}"
                    move_list.append(to_tile)
                if move_list:
                    moves[from_tile].append(move_list)
    return moves


def make_moves_for_king() -> dict[str, list[str]]:
    """Gets all the moves for the king at each square"""
    moves = defaultdict(list)
    for vector in King.ATTACK_VECTORS:
        for start_file, start_file_name in FILE_NAME.items():
            for start_rank, start_rank_name in RANK_NAME.items():
                from_tile = start_file_name + start_rank_name
                new_file = start_file + vector[0]
                if new_file > 7 or new_file < 0:
                    continue
                new_rank = start_rank + vector[1]
                if new_rank > 7 or new_rank < 0:
                    continue
                to_tile = f"{FILE_NAME[new_file]}{RANK_NAME[new_rank]}"
                moves[from_tile].append(to_tile)
    return moves


def make_pawn_attack_dict(player: int) -> dict[str, list[str]]:
    """Gets all the pawn attacks for player at each square"""
    rank_direction = 1 if player else -1
    moves = defaultdict(list)
    for start_file, start_file_name in FILE_NAME.items():
        for start_rank, start_rank_name in RANK_NAME.items():
            # Pawns can't exist on the top or bottom rows
            if start_rank == 0 or start_rank == 7:
                continue
            from_tile = start_file_name + start_rank_name
            new_rank = start_rank + rank_direction
            # Attack_left
            if start_file > 0:
                to_tile = f"{FILE_NAME[start_file - 1]}{RANK_NAME[new_rank]}"
                moves[from_tile].extend([f"{start_file_name}x{to_tile}"])
            # Attack right
            if start_file < 7:
                to_tile = f"{FILE_NAME[start_file + 1]}{RANK_NAME[new_rank]}"
                moves[from_tile].extend([f"{start_file_name}x{to_tile}"])
    return moves


def make_pawn_move_dict(player: int) -> dict[str, list[str]]:
    """Gets all the pawn moves for player at each square"""
    rank_direction = 1 if player else -1
    starting_rank = 1 if player else 6
    moves = {}
    for _start_file, start_file_name in FILE_NAME.items():
        for start_rank, start_rank_name in RANK_NAME.items():
            # Pawns can't exist on the top or bottom rows
            if start_rank == 0 or start_rank == 7:
                continue
            new_moves = []
            from_tile = start_file_name + start_rank_name
            new_rank = start_rank + rank_direction
            new_moves.append(start_file_name + RANK_NAME[new_rank])
            if start_rank == starting_rank:
                new_moves.append(start_file_name + RANK_NAME[new_rank + rank_direction])
            moves[from_tile] = new_moves
    return moves
