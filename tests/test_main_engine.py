"""Unit Tests for the MainEngine class"""
from collections import deque
import pytest
from prototyping.resources import BASE_STATE_ASCII, START_STATE
from src.main_engine import MainEngine


STARTING_LIST_STATE =\
    [10, 8, 9, 11, 12, 9, 8, 10] + [7] * 8\
    + [0] * 8 + [0] * 8 + [0] * 8 + [0] * 8\
    + [1] * 8 + [4, 2, 3, 5, 6, 3, 2, 4]\
    + [4] + [60] + [0b1111] + [-1]


@pytest.fixture(name="engine")
def fixture_blank_engine():
    """Returns a blank MainEngine class"""
    return MainEngine()


def test_data_structs_init(engine: MainEngine):
    """Tests to make sure the data structures match documentation"""
    assert len(engine.state) == 68
    assert isinstance(engine.game_graph, dict)
    assert isinstance(engine.state_stack, deque)


def test_default_start_state(engine: MainEngine):
    """Makes sure the default starting state is a game of chess"""
    assert engine.state == STARTING_LIST_STATE


def test_init_with_data():
    """Makes sure one can initiate a custom state"""
    in_state = list(range(68))
    engine = MainEngine(in_state)
    assert engine.state == in_state


def test_iter():
    """Makes sure the iteration goes over nothing but the squares on the board"""
    in_state = list(range(68, 136))
    engine = MainEngine(in_state)
    idx = 0
    for idx, x in enumerate(engine):
        assert x == idx + 68
    assert idx == 63


def test_str(engine: MainEngine):
    """Makes sure the printout for the game_state is correct"""
    print(engine)
    assert str(engine) == START_STATE
    engine.state = [0] * 68
    assert str(engine) == BASE_STATE_ASCII


def test_hash_basic():
    # TODO:
    pass


def test_set_get_tile():
    # TODO:
    pass


def test_get_king():
    # TODO:
    pass


def test_set_get_turn():
    # TODO:
    pass


def test_set_get_castle():
    # TODO:
    pass


def test_set_get_en_passant():
    # TODO:
    pass


def test_in_check_rook():
    # TODO:
    pass


def test_in_check_bishop():
    # TODO:
    pass


def test_in_check_knight():
    # TODO:
    pass


def test_in_check_king():
    # TODO:
    pass


def test_in_check_queen():
    # TODO:
    pass


def test_in_check_pawn():
    # TODO:
    pass


def test_enpassant_take():
    # TODO:
    pass


def test_enpassant_no_take():
    # TODO:
    pass


def test_pawn_double_move():
    # TODO:
    pass


def test_pawn_single_move():
    # TODO:
    pass


def test_pawn_promote_take():
    # TODO:
    pass


def test_pawn_promote_no_take():
    # TODO:
    pass


def test_knight_move():
    # TODO:
    pass


def test_bishop_move():
    # TODO:
    pass


def test_rook_move():
    # TODO:
    pass


def test_queen_move():
    # TODO:
    pass


def test_king_move():
    # TODO:
    pass


def test_short_castle():
    # TODO:
    pass


def test_long_castle():
    # TODO:
    pass


def test_pin():
    # TODO:
    pass


def test_hash_moves():
    # TODO:
    pass


def test_hash_take():
    # TODO:
    pass


def test_hash_circular():
    # TODO:
    pass


def test_hash_castling():
    # TODO:
    pass


def test_hash_enpassant():
    # TODO:
    pass


def test_sufficient_material():
    # TODO:
    pass


def test_get_game_notation():
    # TODO:
    pass


def test_play_game_from_notation():
    # TODO
    pass
