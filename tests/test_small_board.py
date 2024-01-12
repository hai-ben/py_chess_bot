import pytest
from src.small_board import SmallBoard
from src.chess_pieces import Pawn, Bishop, Knight, Rook, Queen, King

@pytest.fixture
def board():
    return SmallBoard()


def test_zero_strip_from(board):
    board.state = 2**10-1  # 10 digits of  '1'
    board.zero_strip_from(3, 4)  # should be 0b1110000111
    assert board.state == int("1110000111", 2)


def test_set_get_to_play(board):
    board.set_turn(1)
    assert board.get_turn() == 1
    board.set_turn(0)
    assert board.get_turn() == 0


def test_castle_rights(board):
    board.set_white_long_castle_right(1)
    board.set_white_short_castle_right(1)
    board.set_black_long_castle_right(1)
    board.set_black_short_castle_right(1)
    assert board.get_white_long_castle_right()
    assert board.get_white_short_castle_right()
    assert board.get_black_long_castle_right()
    assert board.get_black_short_castle_right()

    board.set_white_long_castle_right(0)
    board.set_white_short_castle_right(0)
    board.set_black_long_castle_right(0)
    board.set_black_short_castle_right(0)
    assert not board.get_white_long_castle_right()
    assert not board.get_white_short_castle_right()
    assert not board.get_black_long_castle_right()
    assert not board.get_black_short_castle_right()
    

def test_en_passant_tile_get_set(board):
    board.set_en_passant_file_idx(2)
    assert board.en_passant_file() == 2
    board.unset_en_passant()
    assert board.en_passant_file() < 0


def test_set_unset_tile(board):
    board.set_tile_to("c4", King, 1)
    board.set_tile_to("a2", Queen, 1)
    board.set_tile_to("g6", Knight, 0)
    board.set_tile_to("e7", Bishop, 0)
    board.set_tile_to("e2", Pawn, 0)
    board.set_tile_to("b4", Rook, 1)
    assert board.get_tile("c4") == (King, 1)
    assert board.get_tile("a2") == (Queen, 1)
    assert board.get_tile("g6") == (Knight, 0)
    assert board.get_tile("e7") == (Bishop, 0)
    assert board.get_tile("e2") == (Pawn, 0)
    assert board.get_tile("b4") == (Rook, 1)
    assert board.get_tile("a1")[0] is None

    board.unset_tile("a2")
    assert board.get_tile("a2")[0] is None

