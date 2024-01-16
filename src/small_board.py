import math
from typing import Self
from collections import defaultdict 
from src.chess_pieces import Pawn, Bishop, Knight, Rook, Queen, King

FILE_IDX = {"a": 7, "b": 6, "c": 5, "d": 4, "e": 3, "f": 2, "g": 1, "h": 0}
RANK_IDX = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7}
FILE_NAME = {7: "a", 6: "b", 5: "c", 4: "d", 3: "e", 2: "f", 1: "g", 0: "h"}
RANK_NAME = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8"}
PIECE_TYPE = {0: None, 1: Pawn, 2: Bishop, 3: Knight, 4: Rook, 5: Queen, 6: King}
PIECE_ID = {None: 0, Pawn: 1, Bishop: 2, Knight: 3, Rook: 4, Queen: 5, King: 6}
PIECE_NAME = {King: "K", Bishop: "B", Knight: "N", Queen: "Q", Rook: "R"}
PROMOTE_TO_PIECES = [Queen, Rook, Knight, Bishop]
TO_PLAY_OFFSET = 0
BLACK_LONG_OFFSET = 1
BLACK_SHORT_OFFSET = 2
WHITE_LONG_OFFSET = 3
WHITE_SHORT_OFFSET = 4
EN_PASSANT_FILE_OFFSET = 5
EN_PASSANT_POSSIBLE_OFFSET = 8
BOARD_START_OFFSET = 9
WHITE_KING_OFFSET = 265
BLACK_KING_OFFSET = 271

# Can compute TILE_OFFSETS with:
# for file in "abcdefgh":
#     for rank in "12345678":
#         TILE_OFFSETS[file + rank] = BOARD_START_OFFSET + 4 * (FILE_IDX[file] + (8 * RANK_IDX[rank]))
TILE_OFFSETS = {
    'a1': 37, 'a2': 69, 'a3': 101, 'a4': 133, 'a5': 165, 'a6': 197, 'a7': 229, 'a8': 261,
    'b1': 33, 'b2': 65, 'b3': 97, 'b4': 129, 'b5': 161, 'b6': 193, 'b7': 225, 'b8': 257,
    'c1': 29, 'c2': 61, 'c3': 93, 'c4': 125, 'c5': 157, 'c6': 189, 'c7': 221, 'c8': 253,
    'd1': 25, 'd2': 57, 'd3': 89, 'd4': 121, 'd5': 153, 'd6': 185, 'd7': 217, 'd8': 249,
    'e1': 21, 'e2': 53, 'e3': 85, 'e4': 117, 'e5': 149, 'e6': 181, 'e7': 213, 'e8': 245,
    'f1': 17, 'f2': 49, 'f3': 81, 'f4': 113, 'f5': 145, 'f6': 177, 'f7': 209, 'f8': 241,
    'g1': 13, 'g2': 45, 'g3': 77, 'g4': 109, 'g5': 141, 'g6': 173, 'g7': 205, 'g8': 237,
    'h1': 9, 'h2': 41, 'h3': 73, 'h4': 105, 'h5': 137, 'h6': 169, 'h7': 201, 'h8': 233
}

STANDARD_START = {
    "a8": (Rook, 0), "b8": (Knight, 0), "c8": (Bishop, 0), "d8": (Queen, 0), "e8": (King, 0), "f8": (Bishop, 0), "g8": (Knight, 0), "h8": (Rook, 0),
    "a7": (Pawn, 0), "b7": (Pawn, 0), "c7": (Pawn, 0), "d7": (Pawn, 0), "e7": (Pawn, 0), "f7": (Pawn, 0), "g7": (Pawn, 0), "h7": (Pawn, 0),
    "a2": (Pawn, 1), "b2": (Pawn, 1), "c2": (Pawn, 1), "d2": (Pawn, 1), "e2": (Pawn, 1), "f2": (Pawn, 1), "g2": (Pawn, 1), "h2": (Pawn, 1),
    "a1": (Rook, 1), "b1": (Knight, 1), "c1": (Bishop, 1), "d1": (Queen, 1), "e1": (King, 1), "f1": (Bishop, 1), "g1": (Knight, 1), "h1": (Rook, 1),
}

ASCII_LOOKUP_WHITE = {Pawn: "♙", Bishop: "♗", Knight: "♘", Rook: "♖", Queen: "♕", King: "♔"}
ASCII_LOOKUP_BLACK = {Pawn: "♟︎", Bishop: "♝", Knight: "♞", Rook: "♜", Queen: "♛", King: "♚"}
LIGHT_TILE = "□"
DARK_TILE = "■"

BLACK_SHORT_SAFE_TILES = ["e8", "f8", "g8", "h8"]
WHITE_SHORT_SAFE_TILES = ["e1", "f1", "g1", "h1"]
BLACK_LONG_SAFE_TILES = ["e8", "d8", "c8", "b8", "a8"]
WHITE_LONG_SAFE_TILES = ["e1", "d1", "c1", "b1", "a1"]
THREAT_SYSTEM = [
    (Bishop.ATTACK_VECTORS, 8, set([Queen, Bishop])),
    (Rook.ATTACK_VECTORS, 8, set([Queen, Rook])),
    (Knight.ATTACK_VECTORS, 1, set([Knight])),
    (Queen.ATTACK_VECTORS, 1, set([King]))
]
DIRECTION_PIECE = {
    (1, 1): set([Bishop, Queen]),
    (-1, -1): set([Bishop, Queen]),
    (1, -1): set([Bishop, Queen]),
    (-1, 1): set([Bishop, Queen]),
    (1, 0): set([Rook, Queen]),
    (-1, 0): set([Rook, Queen]),
    (0, -1): set([Rook, Queen]),
    (0, 1): set([Rook, Queen]),
}

SUFFICIENT_MATERIAL = set([Queen, Rook, Pawn])

class SmallBoard:
    def __init__(self, board_state: int=0, flip_turn: bool=True) -> None:
        """
        The state a binary representation of a chess board laid out in the following hunks:
        [white_king_tile][black_king_tile][board_position][en_passant_info][castling_info][player_turn]
        player_turn (1 bit): 1 is White, 0 is Black
        castling_info (4 bits): [white_short, white_long, black_short, black_long]
        en_passant_info (4 bits): [en_passant_allowed (1 bit), en_passant_file (3 bits)]
        board_position (4 bits x 64 long sequence): [a8, b8, ....., g1, h1]
        each tile is broken up in the following way:
        [controlled_by_player (1 bit), piece_id (3 bits)]
        piece_id can be looked up in the dict, controlled_by_player 1 is White, 0 is Black
        """
        self.state = board_state
        self.unset_en_passant()

        # Because the turn flips on creation, the default state should be blacks turn
        if flip_turn:
            self.flip_turn()
    
    def __iter__(self):
        self.pointer = 0
        return self

    def __next__(self):
        if self.pointer < 64:
            file = self.pointer % 8
            rank = self.pointer // 8
            piece, player = self.get_tile_by_offset(BOARD_START_OFFSET + 4 * self.pointer)
            self.pointer += 1
            return file, rank, piece, player
        else:
            raise StopIteration

    def __str__(self):
        out_str = ""
        for file, rank, piece, player in self:
            if piece is None:
                if (file + rank) % 2 == 0:
                    out_str = LIGHT_TILE + " " + out_str
                else:
                    out_str = DARK_TILE + " " + out_str
            else:
                if player == 1:
                    out_str = ASCII_LOOKUP_WHITE[piece] + " " + out_str
                else:
                    out_str = ASCII_LOOKUP_BLACK[piece] + " " + out_str
            if file == 7:
                out_str = "\n" + out_str
        return out_str[1:]

    def __hash__(self):
        return hash(self.state)

    def reset(self):
        self.state = 0
        self.set_turn(1)
        self.set_white_short_castle_right(1)
        self.set_black_short_castle_right(1)
        self.set_white_long_castle_right(1)
        self.set_black_long_castle_right(1)
        self.unset_en_passant()
        self.set_king_position(0, "e8")
        self.set_king_position(1, "e1")
        for tile, (piece, player) in STANDARD_START.items():
            self.set_tile_to(tile, piece, player)

    def set_turn(self, player: int) -> None:
        self.state &= ~1
        self.state += player

    def get_turn(self) -> int:
        return self.state & 1 == 1
    
    def flip_turn(self) -> None:
        self.state ^= 1

    def set_king_position(self, player: int, tile: str) -> None:
        offset = WHITE_KING_OFFSET if player else BLACK_KING_OFFSET
        self.zero_strip_from(offset, 6)
        self.state += ((TILE_OFFSETS[tile] - BOARD_START_OFFSET) // 4) << offset

    def set_white_long_castle_right(self, has_right: int) -> None:
        self.state &= ~(1 << WHITE_LONG_OFFSET)
        self.state += (has_right << WHITE_LONG_OFFSET)
    
    def set_white_short_castle_right(self, has_right: int) -> None:
        self.state &= ~(1 << WHITE_SHORT_OFFSET)
        self.state += (has_right << WHITE_SHORT_OFFSET)
    
    def set_black_long_castle_right(self, has_right: int) -> None:
        self.state &= ~(1 << BLACK_LONG_OFFSET)
        self.state += (has_right << BLACK_LONG_OFFSET)
    
    def set_black_short_castle_right(self, has_right: int) -> None:
        self.state &= ~(1 << BLACK_SHORT_OFFSET)
        self.state += (has_right << BLACK_SHORT_OFFSET)
    
    def get_white_long_castle_right(self) -> bool:
        return (self.state >> WHITE_LONG_OFFSET) & 1 == 1
    
    def get_white_short_castle_right(self) -> bool:
        return (self.state >> WHITE_SHORT_OFFSET) & 1 == 1
    
    def get_black_long_castle_right(self) -> bool:
        return (self.state >> BLACK_LONG_OFFSET) & 1 == 1
    
    def get_black_short_castle_right(self) -> bool:
        return (self.state >> BLACK_SHORT_OFFSET) & 1 == 1

    def set_en_passant_file_idx(self, file_idx: int) -> None:
        self.unset_en_passant()
        self.state += ((1 << 3) + file_idx) << EN_PASSANT_FILE_OFFSET

    def unset_en_passant(self) -> None:
        self.zero_strip_from(EN_PASSANT_FILE_OFFSET, 4)

    def en_passant_file(self) -> None:
        return -8 + ((self.state >> EN_PASSANT_FILE_OFFSET) & 15)
    
    def set_tile_by_file_rank(self, file: int, rank: int, piece: type, player: int) -> None:
        tile = FILE_NAME[file] + RANK_NAME[rank]
        self.set_tile_to(tile, piece, player)

    def set_tile_to(self, tile: str, piece: type, player: int) -> None:
        self.unset_tile(tile)
        self.state += ((player << 3) + PIECE_ID[piece]) << TILE_OFFSETS[tile]
        if piece is King:
            self.set_king_position(player, tile)

    def unset_tile(self, tile: str) -> None:
        self.zero_strip_from(TILE_OFFSETS[tile], 4)

    def unset_tiles(self, tiles: list) -> None:
        for tile in tiles:
            self.unset_tile(tile)

    def get_tile_by_offset(self, offset: int):
        return (PIECE_TYPE[(self.state >> offset) & 7], (self.state >> (offset + 3)) & 1)

    def get_tile_by_file_rank(self, file: int, rank: int):
        return self.get_tile_by_offset(4 * (file + 8 * rank) + BOARD_START_OFFSET)

    def get_tile(self, tile: str):
        return (PIECE_TYPE[self.state >> (TILE_OFFSETS[tile]) & 7],
                ((self.state >> (TILE_OFFSETS[tile] + 3)) & 1))
    
    def zero_strip_from(self, idx_from_right: int, digits_to_left: int) -> None:
        self.state &= ~(((1 << digits_to_left) - 1) << idx_from_right)

    def find_king(self, player: int) -> str:
        tile_num = (self.state >> (WHITE_KING_OFFSET if player else BLACK_KING_OFFSET)) & 63
        return FILE_NAME[tile_num % 8] + RANK_NAME[tile_num // 8]
    
    def threatened_in_directions(self, file: int, rank: int,
                                 directions: list, distance: int,
                                 by_player: int, by_pieces: set) -> bool:
    
        for horizontal, vertical in directions:
            for i in range(1, distance + 1):
                # Get the new files and ranks and end the loop if they're off the board
                new_file = file + i * vertical
                if new_file > 7 or new_file < 0:
                    break
                new_rank = rank + i * horizontal
                if new_rank > 7 or new_rank < 0:
                    break

                piece, player = self.get_tile_by_file_rank(new_file, new_rank)
                if piece is not None:
                    if player == by_player and piece in by_pieces:
                        return True
                    break
        return False

    def tile_threatened(self, tile: str, by_player: int=None) -> bool:
        by_player = int(not self.get_turn()) if by_player is None else by_player
        file = FILE_IDX[tile[0]]
        rank = RANK_IDX[tile[1]]
        
        # Find pieces from regular pieces
        for vectors, distance, piece_set in THREAT_SYSTEM:
            if self.threatened_in_directions(file, rank, vectors, distance, by_player, piece_set):
                return True

        # If the tile is on or behind the pawn starting row of the opposite player
        if (rank <= 1 and by_player == 1) or (rank >= 6 and by_player == 0):
            return False
        
        # A tile is threatened by a white pawn if there is a white pawn "below" it
        new_rank = rank + (-1 if by_player == 1 else 1)
        # Check pawn attacks on the left and right
        if file - 1 >= 0 and (Pawn, by_player) == self.get_tile_by_file_rank(file - 1, new_rank):
            return True
        if file + 1 <= 7 and (Pawn, by_player) == self.get_tile_by_file_rank(file + 1, new_rank):
            return True
        
        # Exhausted all possible threats
        return False

    def get_tile_vector(self, from_tile, to_tile) -> tuple[int, int]:
        return (FILE_IDX[to_tile[0]] - FILE_IDX[from_tile[0]], RANK_IDX[to_tile[1]] - RANK_IDX[from_tile[1]])

    def tile_threatened_on_vector(self, start_tile:str, vector: tuple[int, int], by_pieces: set, by_player: int) -> bool:
        file = FILE_IDX[start_tile[0]]
        rank = RANK_IDX[start_tile[1]]

        for i in range(1, 9):
            new_file = file + i * vector[0]
            if new_file > 7 or new_file < 0:
                break
            new_rank = rank + i * vector[1]
            if new_rank > 7 or new_rank < 0:
                break
            piece, player = self.get_tile_by_file_rank(new_file, new_rank)
            if piece:
                if player == by_player and piece in by_pieces:
                    return True
                break
        return False

    def move_revealed_check(self, king_tile: str, player, move_string: str) -> bool:
        # If the move is a castle, the move did not reveal a check
        if move_string[0] == "O" or move_string[0] == "K":
            return False

        from_tile = move_string[:2] if move_string[0].islower() else move_string[1:3]
        check_vector = self.get_tile_vector(king_tile, from_tile)
        
        # If the vector isn't pure horizontal or diagonal, there's no threat revelaed threat
        if abs(check_vector[0]) != abs(check_vector[1]) and not any([check_vector[0] == 1, check_vector[1] == 0]):
            return False

        # Clamp the vector to size 1 in each directions
        new_vector = (max(min(check_vector[0], 1), -1), max(min(check_vector[1], 1), -1))

        if self.tile_threatened_on_vector(king_tile, check_vector, DIRECTION_PIECE[new_vector], int(not player)):
            return True
        return False

    def in_check(self, player=None, move_string: str="") -> bool:
        player = self.get_turn() if player is None else player
        king_tile = self.find_king(player)

        # if move_string and self.move_revealed_check(king_tile, player, move_string):
        #     return True

        if king_tile:
            return self.tile_threatened(king_tile, int(not player))
        else:
            return False

    def check_castle_legal(self, safe_tiles: list, player: int) -> bool:
        if (Rook, player) != self.get_tile(safe_tiles[-1]):
            return False

        for tile in safe_tiles[:-1]:
            if self.tile_threatened(tile):
                return False
        
        for tile in safe_tiles[1:-1]:
            piece, _player = self.get_tile(tile)
            if piece:
                return False
        
        return True

    def get_castle_moves(self, active_player: int) -> dict[str, Self]:
        moves = {}
        if active_player:  # If White
            # Short Castle
            if self.get_white_short_castle_right() and self.check_castle_legal(WHITE_SHORT_SAFE_TILES, 1):
                new_move = SmallBoard(self.state)
                new_move.set_white_short_castle_right(0)
                new_move.set_white_long_castle_right(0)
                new_move.unset_tiles(["e1", "h1"])
                new_move.set_tile_to("f1", Rook, 1)
                new_move.set_tile_to("g1", King, 1)
                new_move.set_king_position(1, "g1")
                moves["O-O"] = new_move
            if self.get_white_long_castle_right() and self.check_castle_legal(WHITE_LONG_SAFE_TILES, 1):
                new_move = SmallBoard(self.state)
                new_move.set_white_short_castle_right(0)
                new_move.set_white_long_castle_right(0)
                new_move.unset_tiles(["e1", "a1"])
                new_move.set_tile_to("d1", Rook, 1)
                new_move.set_tile_to("c1", King, 1)
                new_move.set_king_position(1, "c1")
                moves["O-O-O"] = new_move
            return moves
        # Otherwise it's black's turn
        if self.get_black_short_castle_right() and self.check_castle_legal(BLACK_SHORT_SAFE_TILES, 0):
            new_move = SmallBoard(self.state)
            new_move.set_black_short_castle_right(0)
            new_move.set_black_long_castle_right(0)
            new_move.unset_tiles(["e8", "h8"])
            new_move.set_tile_to("f8", Rook, 0)
            new_move.set_tile_to("g8", King, 0)
            new_move.set_king_position(0, "g8")
            moves["O-O"] = new_move
        if self.get_black_long_castle_right() and self.check_castle_legal(BLACK_LONG_SAFE_TILES, 0):
            new_move = SmallBoard(self.state)
            new_move.set_black_short_castle_right(0)
            new_move.set_black_long_castle_right(0)
            new_move.unset_tiles(["e8", "a8"])
            new_move.set_tile_to("d8", Rook, 0)
            new_move.set_tile_to("c8", King, 0)
            new_move.set_king_position(0, "c8")
            moves["O-O-O"] = new_move
        return moves

    def find_promotion_moves(self, from_file: int, from_rank: int,
                             promotion_file: int, promotion_rank: int,
                             is_take: bool=False) ->  dict[str, Self]:
        moves = {}
        new_move_parent = SmallBoard(self.state)
        to_tile = f"{FILE_NAME[promotion_file]}{RANK_NAME[promotion_rank]}"
        from_tile = f"{FILE_NAME[from_file]}{RANK_NAME[from_rank]}"
        new_move_parent.unset_tile(f"{FILE_NAME[from_file]}{RANK_NAME[from_rank]}")
        to_tile = f"{FILE_NAME[promotion_file]}{RANK_NAME[promotion_rank]}"
        from_tile = f"{FILE_NAME[from_file]}{RANK_NAME[from_rank]}"
        move_string = f"{from_tile}x{to_tile}" if is_take else f"{from_tile}{to_tile}"
        for piece in PROMOTE_TO_PIECES:
            new_move = SmallBoard(new_move_parent.state)
            new_move.flip_turn()  # Because it flips on creation we need an odd number of flips
            new_move.set_tile_to(to_tile, piece, self.get_turn())
            moves[f"{move_string}{PIECE_NAME[piece]}"] = new_move
        return moves
    
    def get_pawn_move_from_to(self, player: int, from_file: int, to_file: int,
                              from_rank: int, to_rank: int) -> Self:
        new_move = SmallBoard(self.state)
        new_move.unset_tile(FILE_NAME[from_file] + RANK_NAME[from_rank])
        new_move.set_tile_by_file_rank(to_file, to_rank, Pawn, player)
        return new_move

    def find_pawn_forward_moves(self, file: int, rank: int, player: int) ->  dict[str, Self]:
        moves = {}
        rank_mod = 1 if player else -1
        new_rank = rank + rank_mod
        from_tile = f"{FILE_NAME[file]}{RANK_NAME[rank]}"
        if new_rank == 0 or new_rank == 7:
            moves = moves | self.find_promotion_moves(file, rank, file, new_rank)
        else:
            new_move = self.get_pawn_move_from_to(player, file, file, rank, new_rank)
            moves[f"{from_tile}{FILE_NAME[file]}{RANK_NAME[new_rank]}"] = new_move

            if (new_rank == 2 and player == 1) or (new_rank == 5 and player == 0):
                if self.get_tile_by_file_rank(file, new_rank + rank_mod)[0] is None:
                    new_move = self.get_pawn_move_from_to(player, file, file, rank, new_rank + rank_mod)
                    new_move.set_en_passant_file_idx(file)
                    moves[f"{from_tile}{FILE_NAME[file]}{RANK_NAME[new_rank + rank_mod]}"] = new_move
        return moves

    def find_pawn_moves(self, file: int, rank: int, player: int) ->  dict[str, Self]:
        moves = {}
        rank_mod = 1 if player else -1
        new_rank = rank + rank_mod

        # Forwards moves
        if self.get_tile_by_file_rank(file, new_rank)[0] is None:
            moves = moves | self.find_pawn_forward_moves(file, rank, player)
        
        # Attack right and left (swapped because files increase in value from right to left)
        from_tile = f"{FILE_NAME[file]}{RANK_NAME[rank]}"
        if file - 1 >= 0:
            piece, tile_player = self.get_tile_by_file_rank(file - 1, new_rank)
            if piece and tile_player != player:
                if new_rank == 0 or new_rank == 7:
                    moves = moves | self.find_promotion_moves(file, rank, file - 1, new_rank, True)
                else:
                    new_move = self.get_pawn_move_from_to(player, file, file - 1, rank, new_rank)
                    moves[f"{from_tile}x{FILE_NAME[file - 1]}{RANK_NAME[new_rank]}"] = new_move

        if file + 1 <= 7:
            piece, tile_player = self.get_tile_by_file_rank(file + 1, new_rank)
            if piece and tile_player != player:
                if new_rank == 0 or new_rank == 7:
                    moves = moves | self.find_promotion_moves(file, rank, file + 1, new_rank, True)
                else:
                    new_move = self.get_pawn_move_from_to(player, file, file + 1, rank, new_rank)
                    moves[f"{from_tile}x{FILE_NAME[file + 1]}{RANK_NAME[new_rank]}"] = new_move

        # En passant
        if (new_rank == 5 and player == 1) or (new_rank == 2 and player == 0):
            if self.en_passant_file() == file - 1:
                new_move = self.get_pawn_move_from_to(player, file, file - 1, rank, new_rank)
                new_move.unset_tile(FILE_NAME[file - 1] + RANK_NAME[rank])
                moves[f"{from_tile}x{FILE_NAME[file - 1]}{RANK_NAME[new_rank]}"] = new_move
            elif self.en_passant_file() == file + 1:
                new_move = self.get_pawn_move_from_to(player, file, file + 1, rank, new_rank)
                new_move.unset_tile(FILE_NAME[file + 1] + RANK_NAME[rank])
                moves[f"{from_tile}x{FILE_NAME[file + 1]}{RANK_NAME[new_rank]}"] = new_move
        
        return moves

    def remove_castle_right(self, player:int, move_string: str) -> None:
        if player == 1:
            if "K" == move_string[0]:  # Doing the castle move already removes rights
                self.set_white_short_castle_right(0)
                self.set_white_long_castle_right(0)
            elif self.get_white_long_castle_right() and move_string == "Ra1":
                self.set_white_long_castle_right(0)
            elif self.get_white_short_castle_right() and move_string == "Rh1":
                self.set_white_short_castle_right(0)
        else:
            if "K" == move_string[0]: # Doing the castle move already removes rights
                self.set_black_short_castle_right(0)
                self.set_black_long_castle_right(0)
            elif self.get_black_long_castle_right() and move_string == "Ra8":
                self.set_black_long_castle_right(0)
            elif self.get_black_short_castle_right() and move_string == "Rh8":
                self.set_black_short_castle_right(0)

    def regular_piece_moves(self, file, rank, piece, player) ->  dict[str, Self]:
        moves = {}
        for horizontal, vertical in piece.ATTACK_VECTORS:
            for i in range(1, piece.ATTACK_RANGE + 1):
                # Get the new files and ranks and end the loop if they're off the board
                new_file = file + i * vertical
                if new_file > 7 or new_file < 0:
                    break
                new_rank = rank + i * horizontal
                if new_rank > 7 or new_rank < 0:
                    break

                new_piece, controlled_by = self.get_tile_by_file_rank(new_file, new_rank)
                move_string = f"{PIECE_NAME[piece]}{FILE_NAME[file]}{RANK_NAME[rank]}"
                new_move = SmallBoard(self.state)

                # Remove Approriate Castling rights
                if piece is Rook or piece is King:
                    new_move.remove_castle_right(player, move_string)

                # If there is a piece in the way
                if new_piece:
                    if controlled_by != player:
                        move_string += "x"
                        move_string += f"{FILE_NAME[new_file]}{RANK_NAME[new_rank]}"
                        new_move.unset_tile(FILE_NAME[file] + RANK_NAME[rank])
                        new_move.set_tile_by_file_rank(new_file, new_rank, piece, player)
                        moves[move_string] = new_move
                    break

                move_string += f"{FILE_NAME[new_file]}{RANK_NAME[new_rank]}"
                new_move.unset_tile(FILE_NAME[file] + RANK_NAME[rank])
                new_move.set_tile_by_file_rank(new_file, new_rank, piece, player)
                moves[move_string] = new_move
        return moves

    def sufficient_material(self) -> bool:
        material = {1: defaultdict(int), 0: defaultdict(int)}
        for file, rank, piece, player in self:
            if piece in SUFFICIENT_MATERIAL:
                return True
            material[player][piece] += 1
            if material[player][Bishop] == 2:
                return True
            if material[player][Bishop] >= 1 and material[player][Knight] >= 1:
                return True
        return False
            
    def get_all_moves(self) -> dict[str, Self]:
        moves = {}
        active_player = self.get_turn()
        moves = moves | self.get_castle_moves(active_player)
        for file, rank, piece, player in self:
            # Skip pieces not controlled by player
            if piece is None or player != active_player:
                continue
            if piece is Pawn:
                moves = moves | self.find_pawn_moves(file, rank, player)
            else:
                moves = moves | self.regular_piece_moves(file, rank, piece, player)

        # Filter out moves that cause check
        return {move: board for move, board in moves.items() if not board.in_check(active_player, move)}
