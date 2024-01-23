"""A suite of tests that makes sure different board states are registered as checks"""
import pytest
from src.resources.data_translators import B_KING_IDX, W_KING_IDX, TURN_IDX


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
    "WHITE_CHECKED_BY_B_QUEEN": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("e4", "b_queen")],
        ("in_check", [True]),
        True
    ),
    "WHITE_NOT_CHECKED_BY_W_QUEEN": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("e4", "w_queen")],
        ("in_check", [True]),
        False
    ),
    "BLACK_CHECKED_BY_W_QUEEN": (
        [("b4", "b_king"), (B_KING_IDX, "b4"), ("b1", "w_queen")],
        ("in_check", [False]),
        True
    ),
    "BLACK_NOT_CHECKED_BY_B_QUEEN": (
        [("b4", "b_king"), (B_KING_IDX, "b4"), ("b1", "b_queen")],
        ("in_check", [False]),
        False
    ),
    "WHITE_CHECKED_BY_B_PAWN": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("b7", "b_pawn")],
        ("in_check", [True]),
        True
    ),
    "WHITE_NOT_CHECKED_BY_W_PAWN": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("d5", "w_pawn")],
        ("in_check", [True]),
        False
    ),
    "BLACK_CHECKED_BY_W_PAWN": (
        [("b4", "b_king"), (B_KING_IDX, "b4"), ("c3", "w_pawn")],
        ("in_check", [False]),
        True
    ),
    "BLACK_NOT_CHECKED_BY_B_PAWN": (
        [("b4", "b_king"), (B_KING_IDX, "b4"), ("a5", "b_pawn")],
        ("in_check", [False]),
        False
    ),
    "WHITE_CHECKED_BY_B_KING": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("d7", "b_king"), (B_KING_IDX, "d7")],
        ("in_check", [True]),
        True
    ),
    "BLACK_CHECKED_BY_W_KING": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("d7", "b_king"), (B_KING_IDX, "d7")],
        ("in_check", [False]),
        True
    ),
    "IN_CHECK_OFF_TURN_W": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("d6", "b_rook"), (TURN_IDX, False)],
        ("in_check", [True]),
        True
    ),
    "IN_CHECK_OFF_TURN_B": (
        [("c6", "b_king"), (B_KING_IDX, "c6"), ("d7", "w_bishop"), (TURN_IDX, True)],
        ("in_check", [False]),
        True
    ),
}


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
