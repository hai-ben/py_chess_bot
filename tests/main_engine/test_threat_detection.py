import pytest
from src.resources.data_translators import SQUARE_IDX, B_KING_IDX, W_KING_IDX, CASTLE_IDX, EP_IDX,\
    TURN_IDX, SQUARE_STATES, CASTLE_STATES, EP_FILE


STATE_RETURN_DICT = {
    "WHITE_CHECKED_BY_B_ROOK_H": (
        [("d2", "w_king"), (W_KING_IDX, "d2"), ("f2", "b_rook")],
        ("in_check", [True]),
        True
    ),
    "WHITE_NOT_CHECKED_BY_W_ROOK_H": (
        [("d2", "w_king"), (W_KING_IDX, "d2"), ("f2", "w_rook")],
        ("in_check", [True]),
        False
    ),
    "BLACK_CHECKED_BY_W_ROOK_H": (
        [("e3", "b_king"), (B_KING_IDX, "e3"), ("a3", "w_rook")],
        ("in_check", [False]),
        True
    ),
    "BLACK_NOT_CHECKED_BY_B_ROOK_H": (
        [("e3", "b_king"), (B_KING_IDX, "e3"), ("a3", "b_rook")],
        ("in_check", [False]),
        False
    ),
    "WHITE_CHECKED_BY_B_ROOK_V": (
        [("a2", "w_king"), (W_KING_IDX, "a2"), ("a8", "b_rook")],
        ("in_check", [True]),
        True
    ),
    "WHITE_NOT_CHECKED_BY_W_ROOK_V": (
        [("a2", "w_king"), (W_KING_IDX, "a2"), ("a8", "w_rook")],
        ("in_check", [True]),
        False
    ),
    "BLACK_CHECKED_BY_W_ROOK_V": (
        [("h8", "b_king"), (B_KING_IDX, "h8"), ("h1", "w_rook")],
        ("in_check", [False]),
        True
    ),
    "BLACK_NOT_CHECKED_BY_B_ROOK_V": (
        [("h8", "b_king"), (B_KING_IDX, "h8"), ("h1", "b_rook")],
        ("in_check", [False]),
        False
    ),
    "WHITE_CHECKED_BY_B_BISHOP": (
        [("d2", "w_king"), (W_KING_IDX, "d2"), ("f4", "b_bishop")],
        ("in_check", [True]),
        True
    ),
    "WHITE_NOT_CHECKED_BY_W_BISHOP": (
        [("d2", "w_king"), (W_KING_IDX, "d2"), ("f4", "w_bishop")],
        ("in_check", [True]),
        False
    ),
    "BLACK_CHECKED_BY_W_BISHOP": (
        [("e3", "b_king"), (B_KING_IDX, "e3"), ("a7", "w_bishop")],
        ("in_check", [False]),
        True
    ),
    "BLACK_NOT_CHECKED_BY_B_BISHOP": (
        [("e3", "b_king"), (B_KING_IDX, "e3"), ("a7", "b_bishop")],
        ("in_check", [False]),
        False
    ),
    "WHITE_CHECKED_BY_B_KNIGHT": (
        [("h1", "w_king"), (W_KING_IDX, "h1"), ("g3", "b_knight")],
        ("in_check", [True]),
        True
    ),
    "WHITE_NOT_CHECKED_BY_W_KNIGHT": (
        [("h1", "w_king"), (W_KING_IDX, "h1"), ("f2", "w_knight")],
        ("in_check", [True]),
        False
    ),
    "BLACK_CHECKED_BY_W_KNIGHT": (
        [("c7", "b_king"), (B_KING_IDX, "c7"), ("a8", "w_knight")],
        ("in_check", [False]),
        True
    ),
    "BLACK_NOT_CHECKED_BY_B_KNIGHT": (
        [("e3", "b_king"), (B_KING_IDX, "e3"), ("a6", "b_knight")],
        ("in_check", [False]),
        False
    ),
}


def test_in_check_king():
    # TODO:
    pass


def test_in_check_queen():
    # TODO:
    pass


def test_in_check_pawn():
    # TODO:
    pass


# Using the board_state dict keys as test parameters for easier debugging
@pytest.mark.parametrize("test_key", STATE_RETURN_DICT.keys())
def test_state_return(board_state_generator, test_key: str):
    """Modifies the state of an empty board to according to mods and then
    calls the given function with the arguments and checks it against the
    specified expected state"""
    mods, (func, args), expected_state = STATE_RETURN_DICT[test_key]
    board = board_state_generator(mods)
    print(board)
    assert getattr(board, func)(*args) == expected_state
