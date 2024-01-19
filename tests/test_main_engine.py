"""Unit Tests for the MainEngine class"""
import pytest
from collections import deque
from src.main_engine import MainEngine


def test_data_structs_init():
    """Tests to make sure the data structures match documentation"""
    engine = MainEngine()
    assert len(engine.state) == 68
    assert engine.game_graph is dict
    assert engine.state_stack is deque


def test_default_start_state():
    # TODO:
    pass


def test_init_with_data():
    # TODO:
    pass


def test_str():
    # TODO:
    pass


def test_iter():
    # TODO:
    pass


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