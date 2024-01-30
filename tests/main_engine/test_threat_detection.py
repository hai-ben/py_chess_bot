"""A suite of tests that makes sure different board states are registered as checks"""
import pytest
from src.resources.data_translators import B_KING_IDX, W_KING_IDX, TURN_IDX, SQUARE_IDX


CHECK_TEST_CASES = {
    "WHITE_CHECKED_BY_B_ROOK_H": (
        [("d2", "w_king"), (W_KING_IDX, "d2"), ("f2", "b_rook")],
        ("squares_attacking_king", [True]),
        ["f2"]
    ),
    "WHITE_NOT_CHECKED_BY_W_ROOK_H": (
        [("d2", "w_king"), (W_KING_IDX, "d2"), ("f2", "w_rook")],
        ("squares_attacking_king", [True]),
        []
    ),
    "BLACK_CHECKED_BY_W_ROOK_H": (
        [("e3", "b_king"), (B_KING_IDX, "e3"), ("a3", "w_rook")],
        ("squares_attacking_king", [False]),
        ["a3"]
    ),
    "BLACK_NOT_CHECKED_BY_B_ROOK_H": (
        [("e3", "b_king"), (B_KING_IDX, "e3"), ("a3", "b_rook")],
        ("squares_attacking_king", [False]),
        []
    ),
    "WHITE_CHECKED_BY_B_ROOK_V": (
        [("a2", "w_king"), (W_KING_IDX, "a2"), ("a8", "b_rook")],
        ("squares_attacking_king", [True]),
        ["a8"]
    ),
    "WHITE_NOT_CHECKED_BY_W_ROOK_V": (
        [("a2", "w_king"), (W_KING_IDX, "a2"), ("a8", "w_rook")],
        ("squares_attacking_king", [True]),
        []
    ),
    "BLACK_CHECKED_BY_W_ROOK_V": (
        [("h8", "b_king"), (B_KING_IDX, "h8"), ("h1", "w_rook")],
        ("squares_attacking_king", [False]),
        ["h1"]
    ),
    "BLACK_NOT_CHECKED_BY_B_ROOK_V": (
        [("h8", "b_king"), (B_KING_IDX, "h8"), ("h1", "b_rook")],
        ("squares_attacking_king", [False]),
        []
    ),
    "WHITE_CHECKED_BY_B_BISHOP": (
        [("d2", "w_king"), (W_KING_IDX, "d2"), ("f4", "b_bishop")],
        ("squares_attacking_king", [True]),
        ["f4"]
    ),
    "WHITE_NOT_CHECKED_BY_W_BISHOP": (
        [("d2", "w_king"), (W_KING_IDX, "d2"), ("f4", "w_bishop")],
        ("squares_attacking_king", [True]),
        []
    ),
    "BLACK_CHECKED_BY_W_BISHOP": (
        [("e3", "b_king"), (B_KING_IDX, "e3"), ("a7", "w_bishop")],
        ("squares_attacking_king", [False]),
        ["a7"]
    ),
    "BLACK_NOT_CHECKED_BY_B_BISHOP": (
        [("e3", "b_king"), (B_KING_IDX, "e3"), ("a7", "b_bishop")],
        ("squares_attacking_king", [False]),
        []
    ),
    "WHITE_CHECKED_BY_B_KNIGHT": (
        [("h1", "w_king"), (W_KING_IDX, "h1"), ("g3", "b_knight")],
        ("squares_attacking_king", [True]),
        ["g3"]
    ),
    "WHITE_NOT_CHECKED_BY_W_KNIGHT": (
        [("h1", "w_king"), (W_KING_IDX, "h1"), ("f2", "w_knight")],
        ("squares_attacking_king", [True]),
        []
    ),
    "BLACK_CHECKED_BY_W_KNIGHT": (
        [("c7", "b_king"), (B_KING_IDX, "c7"), ("a8", "w_knight")],
        ("squares_attacking_king", [False]),
        ["a8"]
    ),
    "BLACK_NOT_CHECKED_BY_B_KNIGHT": (
        [("e3", "b_king"), (B_KING_IDX, "e3"), ("a6", "b_knight")],
        ("squares_attacking_king", [False]),
        []
    ),
    "WHITE_CHECKED_BY_B_QUEEN": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("e4", "b_queen")],
        ("squares_attacking_king", [True]),
        ["e4"]
    ),
    "WHITE_NOT_CHECKED_BY_W_QUEEN": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("e4", "w_queen")],
        ("squares_attacking_king", [True]),
        []
    ),
    "BLACK_CHECKED_BY_W_QUEEN": (
        [("b4", "b_king"), (B_KING_IDX, "b4"), ("b1", "w_queen")],
        ("squares_attacking_king", [False]),
        ["b1"]
    ),
    "BLACK_NOT_CHECKED_BY_B_QUEEN": (
        [("b4", "b_king"), (B_KING_IDX, "b4"), ("b1", "b_queen")],
        ("squares_attacking_king", [False]),
        []
    ),
    "WHITE_CHECKED_BY_B_PAWN": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("b7", "b_pawn")],
        ("squares_attacking_king", [True]),
        ["b7"]
    ),
    "WHITE_NOT_CHECKED_BY_W_PAWN": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("d5", "w_pawn")],
        ("squares_attacking_king", [True]),
        []
    ),
    "BLACK_CHECKED_BY_W_PAWN": (
        [("b4", "b_king"), (B_KING_IDX, "b4"), ("c3", "w_pawn")],
        ("squares_attacking_king", [False]),
        ["c3"]
    ),
    "BLACK_NOT_CHECKED_BY_B_PAWN": (
        [("b4", "b_king"), (B_KING_IDX, "b4"), ("a5", "b_pawn")],
        ("squares_attacking_king", [False]),
        []
    ),
    "WHITE_CHECKED_BY_B_KING": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("d7", "b_king"), (B_KING_IDX, "d7")],
        ("squares_attacking_king", [True]),
        ["d7"]
    ),
    "BLACK_CHECKED_BY_W_KING": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("d7", "b_king"), (B_KING_IDX, "d7")],
        ("squares_attacking_king", [False]),
        ["c6"]
    ),
    "IN_CHECK_OFF_TURN_W": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("d6", "b_rook"), (TURN_IDX, False)],
        ("squares_attacking_king", [True]),
        ["d6"]
    ),
    "IN_CHECK_OFF_TURN_B": (
        [("c6", "b_king"), (B_KING_IDX, "c6"), ("d7", "w_bishop"), (TURN_IDX, True)],
        ("squares_attacking_king", [False]),
        ["d7"]
    ),
    "DOUBLE_CHECK_W": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("d6", "b_rook"), ("d7", "b_bishop")],
        ("squares_attacking_king", [True]),
        ["d6", "d7"]
    ),
    "DOUBLE_CHECK_B": (
        [("c6", "b_king"), (B_KING_IDX, "c6"), ("d6", "w_rook"), ("d7", "w_bishop")],
        ("squares_attacking_king", [False]),
        ["d6", "d7"]
    ),
}


# Using the board_state dict keys as test parameters for easier debugging
@pytest.mark.parametrize("test_key", CHECK_TEST_CASES.keys())
def test_squares_attacking_king(board_state_generator, test_key: str):
    """Modifies the state of an empty board to according to mods and then
    calls the given function with the arguments and checks it against the
    specified expected state"""
    mods, (func, args), expected_state = CHECK_TEST_CASES[test_key]
    board = board_state_generator(mods)
    print(board)
    assert set(getattr(board, func)(*args)) == {SQUARE_IDX[state] for state in expected_state}
