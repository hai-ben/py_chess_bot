"""Unit Tests for the MainEngine class"""
from collections import deque
import pytest
from tests.prototyping.pytest_resources import BASE_STATE_ASCII, START_STATE_ASCII
from src.main_engine import MainEngine


STARTING_LIST_STATE =\
    [10, 8, 9, 11, 12, 9, 8, 10] + [7] * 8\
    + [0] * 8 + [0] * 8 + [0] * 8 + [0] * 8\
    + [1] * 8 + [4, 2, 3, 5, 6, 3, 2, 4]\
    + [4] + [60] + [0b1111] + [-1] + [True]
SHORT_INSTRUCTION = (3, STARTING_LIST_STATE[3], 9, STARTING_LIST_STATE[9])
SINGLE_INSTRUCTION = (3, STARTING_LIST_STATE[3], 9, STARTING_LIST_STATE[9],
                      0b1111, 0b1010, -1, 5)
DOUBLE_INSTRUCTION = (3, STARTING_LIST_STATE[3], 9, STARTING_LIST_STATE[9],
                       0b1111, 0b0000, -1, 2,
                       15, STARTING_LIST_STATE[15], 20, STARTING_LIST_STATE[20])


def test_data_structs_init(engine: MainEngine):
    """Tests to make sure the data structures match documentation"""
    assert len(engine.state) == 69
    assert isinstance(engine.game_graph, dict)
    assert isinstance(engine.state_stack, deque)
    assert isinstance(engine.hash_stack, deque)


def test_default_start_state(engine: MainEngine):
    """Makes sure the default starting state is a game of chess"""
    assert engine.state == STARTING_LIST_STATE


def test_init_with_data():
    """Makes sure one can initiate a custom state"""
    in_state = list([0] * 68 + [True])
    engine = MainEngine(in_state)
    assert engine.state == in_state


def test_iter():
    """Makes sure the iteration goes over nothing but the squares on the board"""
    in_state = list([2] * 68 + [True])
    engine = MainEngine(in_state)
    idx = 0
    for idx, x in enumerate(engine):
        assert x == 2
    assert idx == 63


def test_str(engine: MainEngine):
    """Makes sure the printout for the game_state is correct"""
    print(engine)
    assert str(engine) == START_STATE_ASCII
    engine.state = [0] * 68 + [True]
    assert str(engine) == BASE_STATE_ASCII


def test_hash_basic(engine: MainEngine):
    """Checks the hash of two fresh instances are the same"""
    engine2 = MainEngine()
    assert hash(engine) == hash(engine2)


def test_hash_different_init(engine: MainEngine):
    """Checks the hash of two identical custom instances are the same
    and different from the starting hash"""
    new_state = [0] * 68 + [True]
    engine2 = MainEngine(new_state)
    engine3 = MainEngine(new_state)
    assert hash(engine2) != hash(engine)
    assert hash(engine3) != hash(engine)
    assert hash(engine2) == hash(engine3)


def test_execture_short_instruction(engine: MainEngine):
    """Tests that the engine propertly executes a short instruction set"""
    start_hash = hash(engine)
    engine.execute_instructions(SHORT_INSTRUCTION)
    assert engine.state_stack[-1] == SHORT_INSTRUCTION  # Correctly stored the instruction set
    assert engine.state[SHORT_INSTRUCTION[0]] == 0  # Correctly moved piece away
    assert engine.state[SHORT_INSTRUCTION[2]] == SHORT_INSTRUCTION[1]  # Set new piece location
    assert engine.state[66] == STARTING_LIST_STATE[66]  # Castling Rights
    assert engine.state[67] == STARTING_LIST_STATE[67]  # En Passant File
    assert engine.state[68] is False   # Player turn
    assert start_hash != hash(engine)  # The hash has udpated
    assert engine.game_graph[start_hash] == (SHORT_INSTRUCTION, hash(engine))


def test_execute_instructions(engine: MainEngine):
    """Tests that the engine properly executes long instruction set"""
    start_hash = hash(engine)
    engine.execute_instructions(SINGLE_INSTRUCTION)
    assert engine.state_stack[-1] == SINGLE_INSTRUCTION  # Correctly stored the instruction set
    assert engine.state[3] == 0  # Correctly moved piece away
    assert engine.state[9] == SINGLE_INSTRUCTION[1]  # Correctly set new piece location
    assert engine.state[66] == 0b1010  # Castling Rights
    assert engine.state[67] == 5       # En Passant File
    assert engine.state[68] is False   # Player turn
    assert start_hash != hash(engine)  # The hash has udpated
    assert engine.game_graph[start_hash] == (SINGLE_INSTRUCTION, hash(engine))


def test_execute_double_instructions(engine: MainEngine):
    """Tests that the engine properly executes a double (castling) instruction set"""
    start_hash = hash(engine)
    engine.execute_instructions(DOUBLE_INSTRUCTION)
    assert engine.state_stack[-1] == DOUBLE_INSTRUCTION  # Correctly stored the instruction set
    assert engine.state[3] == 0  # Correctly moved piece away
    assert engine.state[9] == DOUBLE_INSTRUCTION[1]  # Correctly set new piece location
    assert engine.state[15] == 0  # Correctly moved piece away
    assert engine.state[20] == DOUBLE_INSTRUCTION[9]  # Correctly set new piece location
    assert engine.state[66] == 0b0000  # Castling Rights
    assert engine.state[67] == 2       # En Passant File
    assert engine.state[68] is False   # Player turn
    assert start_hash != hash(engine)  # The hash has udpated
    assert engine.game_graph[start_hash] == (DOUBLE_INSTRUCTION, hash(engine))


def test_reverse_last_instruction(engine: MainEngine):
    """Ensures that a simple instruction is correctly undone"""
    start_hash = hash(engine)
    engine.execute_instructions(SINGLE_INSTRUCTION)
    engine.reverse_last_instruction()
    assert engine.state == STARTING_LIST_STATE
    assert hash(engine) == start_hash
    assert len(engine.state_stack) == 0


def test_reverse_last_double_instruction(engine: MainEngine):
    """Ensures that a double instruction is correctly undone"""
    start_hash = hash(engine)
    engine.execute_instructions(DOUBLE_INSTRUCTION)
    engine.reverse_last_instruction()
    assert engine.state == STARTING_LIST_STATE
    assert hash(engine) == start_hash
    assert len(engine.state_stack) == 0


def test_king_idx_updated_with_instructions(engine: MainEngine):
    """Ensures that the king indicies are updated when king move instructions are executed"""
    # White king movement
    instruction_set_1 = (60, engine.state[60], 35, engine.state[35])
    engine.execute_instructions(instruction_set_1)
    assert engine.state[65] == 35  # White King
    assert engine.state[64] == 4   # Black King

    # Black king movement
    instruction_set_2 = (4, engine.state[4], 20, engine.state[20])
    engine.execute_instructions(instruction_set_2)
    assert engine.state[64] == 20  # Black King
    assert engine.state[65] == 35  # White King


def test_king_idx_updated_when_instructions_reversed(engine: MainEngine):
    """Ensures that the king indicies are updated when king move instructions are undone"""
    # White king movement
    instruction_set_1 = (60, engine.state[60], 35, engine.state[35])
    instruction_set_2 = (4, engine.state[4], 20, engine.state[20])
    engine.execute_instructions(instruction_set_1)
    engine.execute_instructions(instruction_set_2)
    engine.reverse_last_instruction()
    assert engine.state[64] == 4   # Black King
    engine.reverse_last_instruction()
    assert engine.state[65] == 60  # White King


SUFFICIENT_MATERIAL_CASES = {
    "LONE_KING": ([], False),
    "PAWN": ([("e4", "w_pawn")], True),
    "ROOK": ([("e4", "b_rook")], True),
    "QUEEN": ([("e4", "b_queen")], True),
    "SINGLE_KNIGHT": ([("e4", "w_knight"), ("e5", "b_knight")], False),
    "DOUBLE_KNIGHT": ([("e4", "w_knight"), ("e5", "w_knight")], False),
    "SINGLE_BISHOP": ([("e4", "w_bishop"), ("e5", "b_bishop")], False),
    "DOUBLE_BISHOP_W": ([("e4", "w_bishop"), ("e5", "w_bishop")], True),
    "DOUBLE_BISHOP_B": ([("e4", "b_bishop"), ("e5", "b_bishop")], True),
    "KNIGHT_BISHOP_W": ([("e4", "w_bishop"), ("e5", "w_knight")], True),
    "KNIGHT_BISHOP_B": ([("e4", "b_bishop"), ("e5", "b_knight")], True),
    "2_W_KNIGHT_VS_BISHOP": ([("e4", "w_knight"), ("e5", "w_knight"), ("e6", "b_knight")], True),
    "2_W_KNIGHT_VS_KNIGHT": ([("e4", "w_knight"), ("e5", "w_knight"), ("e6", "b_bishop")], True),
    "2_B_KNIGHT_VS_BISHOP": ([("e4", "b_knight"), ("e5", "b_knight"), ("e6", "w_knight")], True),
    "2_B_KNIGHT_VS_KNIGHT": ([("e4", "b_knight"), ("e5", "b_knight"), ("e6", "w_bishop")], True),
    "2_V_2_KNIGHTS": ([("e4", "b_knight"), ("e5", "b_knight"),
                       ("e6", "w_knight"), ("e7", "w_knight")], True),
    "3_KNIGHTS_W": ([("e4", "w_knight"), ("e5", "w_knight"), ("e6", "w_knight")], True),
    "3_KNIGHTS_B": ([("e4", "b_knight"), ("e5", "b_knight"), ("e6", "b_knight")], True),
}


@pytest.mark.parametrize("test_key", SUFFICIENT_MATERIAL_CASES.keys())
def test_sufficient_material(board_state_generator, test_key):
    """Given the modifications to the board given in the SUFFICIENT_MATERIAL_TESTS
    dictionary checks if the state is correct"""
    mods, expected_return = SUFFICIENT_MATERIAL_CASES[test_key]
    assert board_state_generator(mods).sufficient_material() is expected_return


def test_get_notation_from_state():
    # TODO:
    pass


def test_play_game_from_notation():
    # TODO
    pass
