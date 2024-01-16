import pytest
from src.small_board import SmallBoard
from src.chess_pieces import Pawn, Bishop, Knight, Rook, Queen, King
from resources import START_STATE, BASE_STATE_ASCII, OPENING_MOVES_WHITE

@pytest.fixture
def board() -> SmallBoard:
    return SmallBoard()


@pytest.fixture
def start_board(board: SmallBoard) -> SmallBoard:
    board.reset()
    return board


@pytest.fixture
def castle_board(start_board: SmallBoard) -> SmallBoard:
    start_board.unset_tiles(["b1", "c1", "d1", "f1", "g1",
                             "b8", "c8", "d8", "f8", "g8"])
    return start_board


def test_zero_strip_from(board: SmallBoard):
    board.state = 2**10-1  # 10 digits of  '1'
    board.zero_strip_from(3, 4)  # should be 0b1110000111
    assert board.state == int("1110000111", 2)


def test_set_get_to_play(board: SmallBoard):
    board.set_turn(1)
    assert board.get_turn() == 1
    board.set_turn(0)
    assert board.get_turn() == 0


def test_castle_rights(board: SmallBoard):
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
    

def test_en_passant_tile_get_set(board: SmallBoard):
    board.set_en_passant_file_idx(2)
    assert board.en_passant_file() == 2
    board.unset_en_passant()
    assert board.en_passant_file() < 0


def test_set_unset_tile(board: SmallBoard):
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


def test_iter(board: SmallBoard):
    for idx, (file_idx, rank_idx, piece_type, _player) in enumerate(board):
        assert piece_type is None
        assert idx % 8 == file_idx
        assert idx // 8 == rank_idx


def test_str(board: SmallBoard):
    assert str(board) == BASE_STATE_ASCII


def test_start_state(start_board: SmallBoard):
    assert start_board.get_turn() == 1
    assert start_board.get_white_long_castle_right()
    assert start_board.get_white_short_castle_right()
    assert start_board.get_black_long_castle_right()
    assert start_board.get_black_short_castle_right()
    assert start_board.en_passant_file() < 0
    assert str(start_board) == START_STATE


def test_in_check_rook(board: SmallBoard):
    board.set_turn(0)
    board.set_tile_to("a1", King, 0)
    board.set_tile_to("a2", Rook, 1)
    board.set_tile_to("a3", King, 1)
    assert board.in_check()
    assert board.in_check(0)
    assert not board.in_check(1)

def test_rook_check_adv(board: SmallBoard):
    board.set_turn(0)
    board.set_tile_to("b8", King, 0)
    board.set_tile_to("b5", Rook, 1)
    assert board.in_check()
    assert board.in_check(0)
    assert not board.in_check(1)

def test_in_check_king(board: SmallBoard):
    board.set_turn(0)
    board.set_tile_to("a1", King, 0)
    board.set_tile_to("b2", King, 1)
    assert board.in_check()
    assert board.in_check(0)
    assert board.in_check(1)

def test_in_check_queen(board: SmallBoard):
    board.set_turn(1)
    board.set_tile_to("a1", King, 0)
    board.set_tile_to("c3", Queen, 1)
    print(board)
    assert not board.in_check()
    assert board.in_check(0)
    assert not board.in_check(1)

def test_in_check_pawn(board: SmallBoard):
    board.set_turn(1)
    board.set_tile_to("c5", King, 1)
    board.set_tile_to("d6", Pawn, 0)
    board.set_tile_to("h8", King, 0)
    assert board.in_check()
    assert not board.in_check(0)
    assert board.in_check(1)

def test_in_check_knight(board: SmallBoard):
    board.set_turn(1)
    board.set_tile_to("c5", King, 1)
    board.set_tile_to("d7", Knight, 0)
    assert board.in_check()
    assert not board.in_check(0)
    assert board.in_check(1)

def test_opening_moves(start_board: SmallBoard):
    expected_moves = set(OPENING_MOVES_WHITE)
    actual_moves = set(start_board.get_all_moves().keys())
    assert not expected_moves.difference(actual_moves)
    assert not actual_moves.difference(expected_moves)


def test_multiple_get_doesnt_change(start_board: SmallBoard):
    expected_moves = set(OPENING_MOVES_WHITE)
    for i in range(5):
        actual_moves = set(start_board.get_all_moves().keys())
    assert not expected_moves.difference(actual_moves)
    assert not actual_moves.difference(expected_moves)


def test_threatened_in_directions(board: SmallBoard):
    board.set_tile_to("b3", Bishop, 0)
    assert board.threatened_in_directions(5, 3, Bishop.ATTACK_VECTORS, 8, 0, set([Bishop]))
    assert not board.threatened_in_directions(5, 3, Bishop.ATTACK_VECTORS, 8, 1, set([Bishop]))

def test_tile_threatened(board: SmallBoard):
    board.set_tile_to("c2", Pawn, 1)
    assert not board.tile_threatened("c3", 0)
    assert not board.tile_threatened("c3", 1)
    assert board.tile_threatened("b3", 1)
    assert board.tile_threatened("d3", 1)
    assert not board.tile_threatened("b3", 0)
    assert not board.tile_threatened("d3", 0)

def test_promotion_basic(board: SmallBoard):
    board.set_tile_to("c7", Pawn, 1)
    expected_moves = set(["c7c8Q", "c7c8N", "c7c8R", "c7c8B"])
    actual_moves = set(board.get_all_moves().keys())
    print(actual_moves)
    assert not expected_moves.difference(actual_moves)
    assert not actual_moves.difference(expected_moves)

def test_promotion_take(board: SmallBoard):
    board.set_tile_to("d2", Pawn, 0)
    board.set_tile_to("d1", Rook, 1)
    board.set_tile_to("c1", Rook, 1)
    board.set_tile_to("e1", Rook, 1)

    # Required because the default king position is h1 meaning there's a pin
    board.set_king_position(1, "a8")
    board.set_king_position(0, "a8")
    board.set_turn(0)
    expected_moves = set(["d2xc1B", "d2xc1Q", "d2xc1R", "d2xc1N",
                          "d2xe1B", "d2xe1Q", "d2xe1R", "d2xe1N"])
    actual_moves = set(board.get_all_moves().keys())
    assert not expected_moves.difference(actual_moves)
    assert not actual_moves.difference(expected_moves)

def test_pin(board: SmallBoard):
    board.set_tile_to("a2", King, 0)
    board.set_tile_to("b2", Pawn, 0)
    board.set_tile_to("c2", Queen, 1)
    board.set_turn(0)
    expected_moves = set(["Ka2a1", "Ka2a3"])
    actual_moves = set(board.get_all_moves().keys())
    print(actual_moves)
    assert not expected_moves.difference(actual_moves)
    assert not actual_moves.difference(expected_moves)

def test_en_passant(board: SmallBoard):
    # Check enpassant triggers
    board.set_tile_to("d5", Pawn, 1)
    board.set_tile_to("e7", Pawn, 0)
    board.set_turn(0)
    moves = board.get_all_moves()
    print(board, "\n")
    new_board = moves["e7e5"]
    print(new_board, "\n")
    assert new_board.en_passant_file() == 3

    # Check that the move registers
    expected_moves = set(["d5xe6", "d5d6"])
    ep_moves = new_board.get_all_moves()
    actual_moves = set(ep_moves.keys())
    assert not expected_moves.difference(actual_moves)
    assert not actual_moves.difference(expected_moves)
    
    # Check that the state after is correct
    post_ep = ep_moves["d5xe6"]
    print(post_ep, "\n")
    empty_tiles = ["e5", "d5", "d6", "d7", "e7", "d4"]
    for tile in empty_tiles:
        assert post_ep.get_tile(tile)[0] is None
    assert post_ep.get_tile("e6") == (Pawn, 1)

def test_pawn_take_white(board: SmallBoard):
    # Check that the right moves exist
    board.set_tile_to("d4", Pawn, 1)
    board.set_tile_to("e5", Pawn, 0)
    board.set_turn(1)
    expected_moves = set(["d4xe5", "d4d5"])
    moves = board.get_all_moves()
    actual_moves = set(moves.keys())
    assert not expected_moves.difference(actual_moves)
    assert not actual_moves.difference(expected_moves)
    # TODO: Test that the move works

def test_castle(castle_board: SmallBoard):
    white_moves = castle_board.get_all_moves()
    castle_board.set_turn(0)
    black_moves = castle_board.get_all_moves()

    # Check the moves are there
    assert "O-O" in white_moves
    assert "O-O-O" in white_moves
    assert "O-O" in black_moves
    assert "O-O-O" in black_moves

    #Check the moves work and remove castle rights
    white_short = white_moves["O-O"]
    white_long = white_moves["O-O-O"]
    black_short = black_moves["O-O"]
    black_long = black_moves["O-O-O"]

    # White Short
    assert not white_short.get_white_short_castle_right()
    assert not white_short.get_white_long_castle_right()
    assert white_short.get_black_short_castle_right()
    assert white_short.get_black_long_castle_right()
    assert white_short.get_tile("d1")[0] is None
    assert white_short.get_tile("h1")[0] is None
    assert white_short.get_tile("g1") == (King, 1)
    assert white_short.get_tile("f1") == (Rook, 1)

    # White long
    assert not white_long.get_white_short_castle_right()
    assert not white_long.get_white_long_castle_right()
    assert white_long.get_black_short_castle_right()
    assert white_long.get_black_long_castle_right()
    assert white_long.get_tile("a1")[0] is None
    assert white_long.get_tile("b1")[0] is None
    assert white_long.get_tile("c1") == (King, 1)
    assert white_long.get_tile("d1") == (Rook, 1)

    # Black Short
    assert not black_short.get_black_short_castle_right()
    assert not black_short.get_black_long_castle_right()
    assert black_short.get_white_short_castle_right()
    assert black_short.get_white_long_castle_right()
    assert black_short.get_tile("d8")[0] is None
    assert black_short.get_tile("h8")[0] is None
    assert black_short.get_tile("g8") == (King, 0)
    assert black_short.get_tile("f8") == (Rook, 0)

    # Black long
    assert not black_long.get_black_short_castle_right()
    assert not black_long.get_black_long_castle_right()
    assert black_long.get_white_short_castle_right()
    assert black_long.get_white_long_castle_right()
    assert black_long.get_tile("a8")[0] is None
    assert black_long.get_tile("b8")[0] is None
    assert black_long.get_tile("c8") == (King, 0)
    assert black_long.get_tile("d8") == (Rook, 0)


def test_cant_castle_after_rooks_move(castle_board: SmallBoard):
    white_right_rook = castle_board.get_all_moves()["Rh1g1"]
    white_left_rook = castle_board.get_all_moves()["Ra1b1"]
    castle_board.set_turn(0)
    black_right_rook = castle_board.get_all_moves()["Rh8g8"]
    black_left_rook = castle_board.get_all_moves()["Ra8b8"]

    assert not white_right_rook.get_white_short_castle_right()
    assert white_right_rook.get_white_long_castle_right()
    assert white_right_rook.get_black_short_castle_right()
    assert white_right_rook.get_black_long_castle_right()

    assert white_left_rook.get_white_short_castle_right()
    assert not white_left_rook.get_white_long_castle_right()
    assert white_left_rook.get_black_short_castle_right()
    assert white_left_rook.get_black_long_castle_right()

    assert black_right_rook.get_white_short_castle_right()
    assert black_right_rook.get_white_long_castle_right()
    assert not black_right_rook.get_black_short_castle_right()
    assert black_right_rook.get_black_long_castle_right()

    assert black_left_rook.get_white_short_castle_right()
    assert black_left_rook.get_white_long_castle_right()
    assert black_left_rook.get_black_short_castle_right()
    assert not black_left_rook.get_black_long_castle_right()


def test_cant_castle_after_king_move(castle_board: SmallBoard):
    white_post_move_board = castle_board.get_all_moves()["Ke1d1"]
    castle_board.set_turn(0)
    black_post_move_board = castle_board.get_all_moves()["Ke8f8"]
    
    assert not white_post_move_board.get_white_short_castle_right()
    assert not white_post_move_board.get_white_long_castle_right()
    assert white_post_move_board.get_black_short_castle_right()
    assert white_post_move_board.get_black_long_castle_right()

    assert not black_post_move_board.get_black_short_castle_right()
    assert not black_post_move_board.get_black_long_castle_right()
    assert black_post_move_board.get_white_short_castle_right()
    assert black_post_move_board.get_white_long_castle_right()


def test_teleport_through_friendly(board: SmallBoard):
    board.set_tile_to("a1", Bishop, 1)
    board.set_tile_to("b2", Pawn, 0)
    board.set_turn(1)
    expected_moves = set(["Ba1xb2"])
    actual_moves = set(board.get_all_moves().keys())
    assert not expected_moves.difference(actual_moves)
    assert not actual_moves.difference(expected_moves)


def test_teleport_through_enemy():
    board = SmallBoard(
        int("1000000000000000110000001001100000000000000001101010000000000000000000000001010000100"
            + "00000100000000000100001001000000010000000010011001000000000000000011010000000000000"
            + "00000000000000010010001101100000000000010011001000000000000000000000000110010100000"
            + "0000101000001", 2), False)
    assert "Qg4c8" not in board.get_all_moves()


def test_sufficient_material_pawn(board: SmallBoard):
    board.set_tile_to("a1", Pawn, 1)
    assert board.sufficient_material()


def test_sufficient_material_two_knights(board: SmallBoard):
    board.set_tile_to("a1", Knight, 0)
    board.set_tile_to("a2", Knight, 0)
    assert not board.sufficient_material()


def test_sufficient_material_one_knight(board: SmallBoard):
    board.set_tile_to("a1", Knight, 0)
    assert not board.sufficient_material()


def test_sufficient_material_one_bishop(board: SmallBoard):
    board.set_tile_to("a1", Bishop, 0)
    assert not board.sufficient_material()


def test_sufficient_material_two_bishop(board: SmallBoard):
    board.set_tile_to("a1", Bishop, 1)
    board.set_tile_to("a2", Bishop, 1)
    assert board.sufficient_material()


def test_sufficient_material_knight_bishop(board: SmallBoard):
    board.set_tile_to("a1", Bishop, 1)
    board.set_tile_to("a2", Knight, 1)
    assert board.sufficient_material()


def test_sufficient_material_queen(board: SmallBoard):
    board.set_tile_to("a1", Queen, 0)
    assert board.sufficient_material()


def test_sufficient_material_rook(board: SmallBoard):
    board.set_tile_to("a1", Rook, 1)
    assert board.sufficient_material()


def test_king_set_on_start(start_board: SmallBoard):
    assert start_board.find_king(1) == "e1"
    assert start_board.find_king(0) == "e8"

    board2 = start_board.get_all_moves()["e2e4"]
    assert start_board.find_king(1) == "e1"
    assert start_board.find_king(0) == "e8"
    assert board2.find_king(1) == "e1"
    assert board2.find_king(0) == "e8"


def test_get_set_king(board: SmallBoard):
    board.set_king_position(1, "h2")
    assert board.find_king(1) == "h2"

    board.set_king_position(0, "c4")
    assert board.find_king(0) == "c4"


def test_king_set_after_castle(castle_board: SmallBoard):
    white_short_castle = castle_board.get_all_moves()["O-O"]
    white_long_castle = castle_board.get_all_moves()["O-O-O"]
    castle_board.flip_turn()
    black_short_castle = castle_board.get_all_moves()["O-O"]
    black_long_castle = castle_board.get_all_moves()["O-O-O"]

    assert white_short_castle.find_king(1) == "g1"
    assert white_short_castle.find_king(0) == "e8"
    assert black_short_castle.find_king(0) == "g8"
    assert black_short_castle.find_king(1) == "e1"

    assert white_long_castle.find_king(1) == "c1"
    assert white_long_castle.find_king(0) == "e8"
    assert black_long_castle.find_king(0) == "c8"
    assert black_long_castle.find_king(1) == "e1"


def test_king_move_updates(castle_board: SmallBoard):
    white_move = castle_board.get_all_moves()["Ke1f1"]
    castle_board.flip_turn()
    black_move = castle_board.get_all_moves()["Ke8f8"]

    assert white_move.find_king(1) == "f1"
    assert white_move.find_king(0) == "e8"
    assert black_move.find_king(0) == "f8"
    assert black_move.find_king(1) == "e1"
    

def test_get_tile_vector(board: SmallBoard):
    assert board.get_tile_vector("e4", "e5") == (0, 1)
    assert board.get_tile_vector("e5", "e4") == (0, -1)
    assert board.get_tile_vector("c4", "f4") == (-3, 0)
    assert board.get_tile_vector("g4", "d4") == (3, 0)
    assert board.get_tile_vector("a1", "h8") == (-7, 7)
    assert board.get_tile_vector("h1", "a8") == (7, 7)


def test_tile_threatened_on_vector(board: SmallBoard):
    board.set_tile_to("h2", Rook, 1)
    # Correct directions
    assert board.tile_threatened_on_vector("e2", (-1, 0), set([Rook]), 1)
    assert board.tile_threatened_on_vector("g3", (-1, -1), set([Rook]), 1)

    # Wrong direction
    assert not board.tile_threatened_on_vector("e2", (-1, -1), set([Rook]), 1)

    # Wrong pieces
    assert not board.tile_threatened_on_vector("g3", (1, -1), set([Bishop, Queen]), 1)
    assert not board.tile_threatened_on_vector("e2", (-1, 0), set([Bishop, Queen]), 1)

    # Wrong player
    assert not board.tile_threatened_on_vector("e2", (-1, 0), set([Rook]), 0)
    assert not board.tile_threatened_on_vector("g3", (1, -1), set([Rook]), 0)


def test_move_revealed_check(board: SmallBoard):
    board.set_tile_to("a2", King, 1)
    board.set_tile_to("c3", Pawn, 1)
    board.set_tile_to("h2", Rook, 0)
    assert board.move_revealed_check("a2", 1, "b2b3")
    assert not board.move_revealed_check("a2", 1, "Ka1a2")