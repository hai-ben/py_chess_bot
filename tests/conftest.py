"""Unit test fixtures and helpers"""
from typing import Callable
import pytest
from src.main_engine import MainEngine
from src.resources.data_translators import SQUARE_IDX, SQUARE_STATES, EP_FILE, PLAYER_TURN

@pytest.fixture(name="engine")
def fixture_blank_engine() -> MainEngine:
    """Returns a MainEngine class with defaults"""
    return MainEngine()


@pytest.fixture(name="empty_board")
def fixture_empty_board() -> MainEngine:
    """Returns a board with no pieces and both king_idx set to a8"""
    return MainEngine([0] * 66 + [0b1111] + [-1] + [True])


@pytest.fixture(name="board_state_generator")
def fixture_board_state_generator() -> Callable:
    """Returns the board_generator used to create board states
    This nested function definition is due to pytest's strange imports"""
    def board_generator(changed_tiles: list[tuple]) -> MainEngine:
        """Updates the indicies of an empty MainEngine's state given the changed_tiles"""
        board = MainEngine([0] * 66 + [0b1111] + [-1] + [True])
        for idx, val in changed_tiles:
            if not isinstance(idx, int):
                idx = SQUARE_IDX[idx]
            if not isinstance(val, (int, bool)):
                val = SQUARE_STATES.get(
                    val, EP_FILE.get(val, PLAYER_TURN.get(val, SQUARE_IDX.get(val, None))))
            board.state[idx] = val
        return board
    return board_generator
