"""
Uses bitstrings to create a chessboard in the following segments
[board_information (4bits x 64positions)][en_passant_info (4 bits)][castling_rights (4 bits)][player_turn (1 bit)]
player_turn: 1 is white and 0 is black
castling_rights: [white_short, white_long, black_short, black_long] 1 is true, 0 is false
en_passant_info: [available (1 is true, 0 is false), file (0 is a, 7 is h)]
board_information: [a8_piece_id, b8_piece_id, ..., g1 piece_id, h1 piece_id]
piece_id: [player_color (1 bit), piece_type (3 bits)]
piece_type:
{
    0: empty,
    1: pawn,
    2: bishop,
    3: knight,
    4: rook,
    5: queen,
    6: king,
}
"""

from src.chess_pieces import Pawn, Bishop, Knight, Rook, Queen, King

FILE_IDX = {"a": 7, "b": 6, "c": 5, "d": 4, "e": 3, "f": 2, "g": 1, "h": 0}
RANK_IDX = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7}
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


class SmallBoard:
    def __init__(self, board_state: int=0) -> None:
        self.state = board_state
    
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

    def get_tile(self, tile: str):
        return (PIECE_TYPE[self.state >> (TILE_OFFSETS[tile]) & 7],
                ((self.state >> (TILE_OFFSETS[tile] + 3)) & 1))
    
    def zero_strip_from(self, idx_from_right: int, digits_to_left: int) -> None:
        self.state &= ~(((1 << digits_to_left) - 1) << idx_from_right)
