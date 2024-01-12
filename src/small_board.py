from src.chess_pieces import Pawn, Bishop, Knight, Rook, Queen, King

FILE_IDX = {"a": 7, "b": 6, "c": 5, "d": 4, "e": 3, "f": 2, "g": 1, "h": 0}
RANK_IDX = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7}
FILE_NAME = {7: "a", 6: "b", 5: "c", 4: "d", 3: "e", 2: "f", 1: "g", 0: "h"}
RANK_NAME = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6", 6: "7", 7: "8"}
PIECE_TYPE = {0: None, 1: Pawn, 2: Bishop, 3: Knight, 4: Rook, 5: Queen, 6: King}
PIECE_ID = {None: 0, Pawn: 1, Bishop: 2, Knight: 3, Rook: 4, Queen: 5, King: 6}
TO_PLAY_OFFSET = 0
BLACK_LONG_OFFSET = 1
BLACK_SHORT_OFFSET = 2
WHITE_LONG_OFFSET = 3
WHITE_SHORT_OFFSET = 4
EN_PASSANT_FILE_OFFSET = 5
EN_PASSANT_POSSIBLE_OFFSET = 8
BOARD_START_OFFSET = 9
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


class SmallBoard:
    def __init__(self, board_state: int=0) -> None:
        """
        The state a binary representation of a chess board laid out in the following hunks:
        [board_position][en_passant_info][castling_info][player_turn]
        player_turn (1 bit): 1 is White, 0 is Black
        castling_info (4 bits): [white_short, white_long, black_short, black_long]
        en_passant_info (4 bits): [en_passant_allowed (1 bit), en_passant_file (3 bits)]
        board_position (4 bits x 64 long sequence): [a8, b8, ....., g1, h1]
        each tile is broken up in the following way:
        [controlled_by_player (1 bit), piece_id (3 bits)]
        piece_id can be looked up in the dict, controlled_by_player 1 is White, 0 is Black
        """
        self.state = board_state
    
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

    def reset(self):
        self.set_turn(1)
        self.set_white_short_castle_right(1)
        self.set_black_short_castle_right(1)
        self.set_white_long_castle_right(1)
        self.set_black_long_castle_right(1)
        self.unset_en_passant()
        for tile, (piece, player) in STANDARD_START.items():
            self.set_tile_to(tile, piece, player)

    def set_turn(self, player: int) -> None:
        self.state &= ~1
        self.state += player

    def get_turn(self) -> int:
        return self.state & 1 == 1
    
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
    
    def set_tile_to(self, tile: str, piece: type, player: int):
        self.unset_tile(tile)
        self.state += ((player << 3) + PIECE_ID[piece]) << TILE_OFFSETS[tile]
    
    def unset_tile(self, tile):
        self.zero_strip_from(TILE_OFFSETS[tile], 4)

    def get_tile_by_offset(self, offset: int):
        return (PIECE_TYPE[(self.state >> offset) & 7], (self.state >> (offset + 3)) & 1)

    def get_tile_by_file_rank(self, file: int, rank: int):
        return self.get_tile_by_offset(4 * (file + 8 * rank) + BOARD_START_OFFSET)

    def get_tile(self, tile: str):
        return (PIECE_TYPE[self.state >> (TILE_OFFSETS[tile]) & 7],
                ((self.state >> (TILE_OFFSETS[tile] + 3)) & 1))
    
    def zero_strip_from(self, idx_from_right: int, digits_to_left: int) -> None:
        self.state &= ~(((1 << digits_to_left) - 1) << idx_from_right)

    def find_king(self, kings_player) -> str:
        for file, rank, piece, player in self:
            if piece is King and player == kings_player:
                return FILE_NAME[file] + RANK_NAME[rank]
        return ""
    
    def threatened_in_directions(self, file: int, rank: int,
                                 directions: list, distance: int,
                                 by_player: int, by_pieces: set):
    
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

    def tile_threatened(self, tile: str) -> bool:
        threatening_player = int(not self.get_turn())
        file = FILE_IDX[tile[0]]
        rank = RANK_IDX[tile[1]]

        if self.threatened_in_directions(file, rank, Bishop.ATTACK_VECTORS, 8, threatening_player, set([Queen, Bishop])):
            return True
        if self.threatened_in_directions(file, rank, Rook.ATTACK_VECTORS, 8, threatening_player, set([Queen, Rook])):
            return True
        if self.threatened_in_directions(file, rank, Knight.ATTACK_VECTORS, 1, threatening_player, set([Knight])):
            return True
        if self.threatened_in_directions(file, rank, Queen.ATTACK_VECTORS, 1, threatening_player, set([King])):
            return True

        # Find pawn threats
        new_rank = rank + (-1)**threatening_player
        if new_rank > 7 or new_rank < 0:  # Can't threaten from off the baord
            return False
        
        # Check pawn left and right
        if file - 1 > 0 and (Pawn, threatening_player) == self.get_tile_by_file_rank(new_rank, file - 1):
            return True
        if file + 1 < 7 and (Pawn, threatening_player) == self.get_tile_by_file_rank(new_rank, file + 1):
            return True
        
        # Exhausted all possible threats
        return False

    def in_check(self) -> bool:
        return self.tile_threatened(self.find_king(self.get_turn()))
