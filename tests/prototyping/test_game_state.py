""""Tests for src.prototyping.board GameState"""
# pylint: disable=missing-function-docstring
# pylint: disable=attribute-defined-outside-init
import pytest
from src.prototyping.board import GameState
from resources import GAME_OF_THE_CENTURY, CENTURY_END_STATE, POST_EN_PASSANT_STATE


@pytest.fixture(name="base_state")
def fixture_base_state():
    return GameState()

@pytest.fixture(name="ready_to_castle")
def fixture_ready_to_castle(base_state):
    moves = "c4 c5 Qb3 Qb6 h4 h5 a4 a5 Nf3 Nf6 Nc3 Nc6 e3 e6 d3 d6 Be2 Be7 Bd2 Bd7"
    base_state.run_game(moves)
    return base_state

def test_find_ambigous_move_basic(base_state):
    assert base_state.find_ambigous_move("Nf3") == "Ng1f3"

def test_the_game_of_the_century(base_state):
    base_state.run_game(GAME_OF_THE_CENTURY)
    assert str(base_state) == CENTURY_END_STATE
    clean_game = GAME_OF_THE_CENTURY.replace("\n", " ")
    while "  " in clean_game:
        clean_game = clean_game.replace("  ", " ")
    clean_game = clean_game.strip(" ")
    assert base_state.notation_string == clean_game

def test_cant_recastle_short(ready_to_castle):
    moves = "O-O O-O g3 g6 Kg2 Kg7 Rh1 Rh8 Kf1 Kf8 Ke1 Ke8"
    ready_to_castle.run_game(moves)
    assert "O-O" not in ready_to_castle.legal_moves
    assert "O-O-O" not in ready_to_castle.legal_moves
    ready_to_castle.make_move("Nd4")
    assert "O-O" not in ready_to_castle.legal_moves
    assert "O-O-O" not in ready_to_castle.legal_moves

def test_cant_recastle_long(ready_to_castle):
    moves = "O-O-O O-O-O Kc2 Kc7 Ra1 Ra8 Kd1 Kd8 Ke1 Ke8"
    ready_to_castle.run_game(moves)
    assert "O-O" not in ready_to_castle.legal_moves
    assert "O-O-O" not in ready_to_castle.legal_moves
    ready_to_castle.make_move("Nd4")
    assert "O-O" not in ready_to_castle.legal_moves
    assert "O-O-O" not in ready_to_castle.legal_moves

def test_cant_castle_after_rooks_move(ready_to_castle):
    moves = "Rh2 Rh7 Rh1 Rh8"
    ready_to_castle.run_game(moves)
    assert "O-O" not in ready_to_castle.legal_moves
    assert "O-O-O" in ready_to_castle.legal_moves
    ready_to_castle.make_move("Ra2")
    assert "O-O" not in ready_to_castle.legal_moves
    assert "O-O-O" in ready_to_castle.legal_moves
    ready_to_castle.run_game("Ra7 Ra1 Ra8")
    assert "O-O" not in ready_to_castle.legal_moves
    assert "O-O-O" not in ready_to_castle.legal_moves
    ready_to_castle.make_move("Nd4")
    assert "O-O" not in ready_to_castle.legal_moves
    assert "O-O-O" not in ready_to_castle.legal_moves

def test_cant_castle_after_king_move(ready_to_castle):
    moves = "Kf1 Kf8 Ke1 Ke8"
    ready_to_castle.run_game(moves)
    assert "O-O" not in ready_to_castle.legal_moves
    assert "O-O-O" not in ready_to_castle.legal_moves
    ready_to_castle.make_move("Nd4")
    assert "O-O" not in ready_to_castle.legal_moves
    assert "O-O-O" not in ready_to_castle.legal_moves

def test_en_passant(base_state):
    moves = "1. d4 h6 2. d5 e5 dxe6"
    base_state.run_game(moves)
    assert str(base_state) == POST_EN_PASSANT_STATE
