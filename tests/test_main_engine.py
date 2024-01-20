"""Unit Tests for the MainEngine class"""
from collections import deque
import pytest
from tests.prototyping.pytest_resources import BASE_STATE_ASCII, START_STATE_ASCII
from src.main_engine import MainEngine
from src.resources.data_translators import SQUARE_IDX, B_KING_IDX, W_KING_IDX, CASTLE_IDX, EP_IDX,\
    TURN_IDX, SQUARE_STATES, CASTLE_STATES, EP_FILE , PLAYER_TURN


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


@pytest.fixture(name="engine")
def fixture_blank_engine():
    """Returns a blank MainEngine class"""
    return MainEngine()


@pytest.fixture(name="empty_board")
def fixture_empty_board():
    """Returns a board with no pieces and both king_idx set to a8"""
    return MainEngine([0] * 66 + [0b1111] + [-1] + [True])


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


MOVE_TEST_DICT = {
    "WHITE_KING_EMPTY": (
        [("e3", "w_king"), (W_KING_IDX, "e3"), (EP_IDX, "b")],
        [["e3"] * 8,
         ["w_king"] * 8,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2", "f4"],
         ["empty"] * 8,
         [0b1111] * 8,
         [0b1100] * 8,
         [EP_FILE["b"]] * 8,
         [-1] * 8],
        ("get_king_moves", [])
    ),
    "WHITE_KING_ENEMY_TAKE": (
        [("e3", "w_king"), (W_KING_IDX, "e3"), (EP_IDX, "b"), ("e2", "b_pawn")],
        [["e3"] * 8,
         ["w_king"] * 8,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2", "f4"],
         ["b_pawn"] + ["empty"] * 7,
         [0b1111] * 8,
         [0b1100] * 8,
         [EP_FILE["b"]] * 8,
         [-1] * 8],
        ("get_king_moves", [])
    ),
    "WHITE_KING_FRIENDLY_TAKE": (
        [("e3", "w_king"), (W_KING_IDX, "e3"), (EP_IDX, "b"), ("f4", "w_pawn")],
        [["e3"] * 7,
         ["w_king"] * 7,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2"],
         ["empty"] * 7,
         [0b1111] * 7,
         [0b1100] * 7,
         [EP_FILE["b"]] * 7,
         [-1] * 7],
        ("get_king_moves", [])
    ),
    "BLACK_KING_EMPTY": (
        [(TURN_IDX, False), ("e3", "b_king"), (B_KING_IDX, "e3"), (EP_IDX, "c")],
        [["e3"] * 8,
         ["b_king"] * 8,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2", "f4"],
         ["empty"] * 8,
         [0b1111] * 8,
         [0b0011] * 8,
         [EP_FILE["c"]] * 8,
         [-1] * 8],
        ("get_king_moves", [])
    ),
    "BLACK_KING_ENEMY_TAKE": (
        [(TURN_IDX, False), ("e3", "b_king"), (B_KING_IDX, "e3"), (EP_IDX, "d"), ("e2", "w_pawn")],
        [["e3"] * 8,
         ["b_king"] * 8,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2", "f4"],
         ["w_pawn"] + ["empty"] * 7,
         [0b1111] * 8,
         [0b0011] * 8,
         [EP_FILE["d"]] * 8,
         [-1] * 8],
        ("get_king_moves", [])
    ),
    "BLACK_KING_ALLY_TAKE": (
        [(TURN_IDX, False), ("e3", "b_king"), (B_KING_IDX, "e3"), (EP_IDX, "e"), ("f4", "b_pawn")],
        [["e3"] * 7,
         ["b_king"] * 7,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2"],
         ["empty"] * 7,
         [0b1111] * 7,
         [0b0011] * 7,
         [EP_FILE["e"]] * 7,
         [-1] * 7],
        ("get_king_moves", [])
    ),
    "WHITE_KNIGHT_EMPTY": (
        [("c5", "w_knight")],
        [["c5"] * 8,
         ["w_knight"] * 8,
         ["b7", "d7", "b3", "d3", "a4", "e4", "e6", "a6"],
         ["empty"] * 8],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "WHITE_KNIGHT_ENEMY_TAKE": (
        [("c5", "w_knight"), ("a6", "b_queen")],
        [["c5"] * 8,
         ["w_knight"] * 8,
         ["b7", "d7", "b3", "d3", "a4", "e4", "e6", "a6"],
         ["empty"] * 7 + ["b_queen"]],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "WHITE_KNIGHT_ALLY_TAKE": (
        [("c5", "w_knight"), ("d3", "w_rook")],
        [["c5"] * 7,
         ["w_knight"] * 7,
         ["b7", "d7", "b3", "a4", "e4", "e6", "a6"],
         ["empty"] * 7],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "WHITE_KNIGHT_UNSET_EP": (
        [("c5", "w_knight"), (EP_IDX, EP_FILE["e"])],
        [["c5"] * 8,
         ["w_knight"] * 8,
         ["b7", "d7", "b3", "d3", "a4", "e4", "e6", "a6"],
         ["empty"] * 8,
         [0b1111] * 8,
         [0b1111] * 8,
         [EP_FILE["e"]] * 8,
         [-1] * 8],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "BLACK_KNIGHT_EMPTY": (
        [("c5", "b_knight"), (TURN_IDX, False)],
        [["c5"] * 8,
         ["b_knight"] * 8,
         ["b7", "d7", "b3", "d3", "a4", "e4", "e6", "a6"],
         ["empty"] * 8],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "BLACK_KNIGHT_ENEMY_TAKE": (
        [("c5", "b_knight"), ("a6", "w_queen"), (TURN_IDX, False)],
        [["c5"] * 8,
         ["b_knight"] * 8,
         ["b7", "d7", "b3", "d3", "a4", "e4", "e6", "a6"],
         ["empty"] * 7 + ["w_queen"]],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "BLACK_KNIGHT_ALLY_TAKE": (
        [("c5", "b_knight"), ("d3", "b_rook"), (TURN_IDX, False)],
        [["c5"] * 7,
         ["b_knight"] * 7,
         ["b7", "d7", "b3", "a4", "e4", "e6", "a6"],
         ["empty"] * 7],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "BLACK_KNIGHT_UNSET_EP": (
        [("c5", "b_knight"), (EP_IDX, EP_FILE["f"]), (TURN_IDX, False)],
        [["c5"] * 8,
         ["b_knight"] * 8,
         ["b7", "d7", "b3", "d3", "a4", "e4", "e6", "a6"],
         ["empty"] * 8,
         [0b1111] * 8,
         [0b1111] * 8,
         [EP_FILE["f"]] * 8,
         [-1] * 8],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "WHITE_BISHOP_EMPTY": (
        [("f5", "w_bishop")],
        [["f5"] * 11,
         ["w_bishop"] * 11,
         ["g6", "h7", "e4", "d3", "c2", "b1", "g4", "h3", "e6", "d7", "c8"],
         ["empty"] * 11],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "WHITE_BISHOP_ENEMY_TAKE": (
        [("f5", "w_bishop"), ("d7", "b_queen")],
        [["f5"] * 10,
         ["w_bishop"] * 10,
         ["g6", "h7", "e4", "d3", "c2", "b1", "g4", "h3", "e6", "d7"],
         ["empty"] * 9 + ["b_queen"]],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "WHITE_BISHOP_ALLY_TAKE": (
        [("f5", "w_bishop"), ("e4", "w_rook")],
        [["f5"] * 7,
         ["w_bishop"] * 7,
         ["g6", "h7", "g4", "h3", "e6", "d7", "c8"],
         ["empty"] * 7],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "WHITE_BISHOP_UNSET_EP": (
        [("f5", "w_bishop"), (EP_IDX, EP_FILE["a"])],
        [["f5"] * 11,
         ["w_bishop"] * 11,
         ["g6", "h7", "e4", "d3", "c2", "b1", "g4", "h3", "e6", "d7", "c8"],
         ["empty"] * 11,
         [0b1111] * 11,
         [0b1111] * 11,
         [EP_FILE["a"]] * 11,
         [-1] * 11],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "BLACK_BISHOP_EMPTY": (
        [("f5", "b_bishop"), (TURN_IDX, False)],
        [["f5"] * 11,
         ["b_bishop"] * 11,
         ["g6", "h7", "e4", "d3", "c2", "b1", "g4", "h3", "e6", "d7", "c8"],
         ["empty"] * 11],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "BLACK_BISHOP_ENEMY_TAKE": (
        [("f5", "b_bishop"), ("d7", "w_queen"), (TURN_IDX, False)],
        [["f5"] * 10,
         ["b_bishop"] * 10,
         ["g6", "h7", "e4", "d3", "c2", "b1", "g4", "h3", "e6", "d7"],
         ["empty"] * 9 + ["w_queen"]],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "BLACK_BISHOP_ALLY_TAKE": (
        [("f5", "b_bishop"), ("e4", "b_rook"), (TURN_IDX, False)],
        [["f5"] * 7,
         ["b_bishop"] * 7,
         ["g6", "h7", "g4", "h3", "e6", "d7", "c8"],
         ["empty"] * 7],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "BLACK_BISHOP_UNSET_EP": (
        [("f5", "b_bishop"), (EP_IDX, EP_FILE["a"]), (TURN_IDX, False)],
        [["f5"] * 11,
         ["b_bishop"] * 11,
         ["g6", "h7", "e4", "d3", "c2", "b1", "g4", "h3", "e6", "d7", "c8"],
         ["empty"] * 11,
         [0b1111] * 11,
         [0b1111] * 11,
         [EP_FILE["a"]] * 11,
         [-1] * 11],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
}


# Using the move test dict keys as test parameters for easier debugging
@pytest.mark.parametrize("test_key", MOVE_TEST_DICT.keys())
def test_get_moves(empty_board: MainEngine, test_key):
    """After making modifications to empty board, this calls func_name of empty board with args
    and asserts the set of that return value is the same as the set of the expected_instructions"""
    # Unpack the test information
    mods, instruction_gen_args, (func, args) = MOVE_TEST_DICT[test_key]

    # Unpack the modifications to the state and apply them
    for idx, val in mods:
        if not isinstance(idx, int):
            idx = SQUARE_IDX[idx]
        if not isinstance(val, (int, bool)):
            val = SQUARE_STATES.get(
                val, EP_FILE.get(val, PLAYER_TURN.get(val, SQUARE_IDX.get(val, None))))
        empty_board.state[idx] = val

    # Generate the instruction set
    if len(instruction_gen_args) == 4:
        expected_instructions = set(
            (SQUARE_IDX[from_tile], SQUARE_STATES[from_state],
             SQUARE_IDX[to_tile], SQUARE_STATES[to_state])
            for from_tile, from_state, to_tile, to_state in zip(*instruction_gen_args))
    elif len(instruction_gen_args) == 8:
        expected_instructions = set(
            (SQUARE_IDX[from_tile], SQUARE_STATES[from_state],
             SQUARE_IDX[to_tile], SQUARE_STATES[to_state],
             castle_from, castle_to, ep_from, ep_to)
            for from_tile, from_state, to_tile, to_state,
                castle_from, castle_to, ep_from, ep_to in zip(*instruction_gen_args))
    else:  # This means len(instruction_gen_args) == 12
        expected_instructions = set(
            (SQUARE_IDX[from_tile], SQUARE_STATES[from_state],
             SQUARE_IDX[to_tile], SQUARE_STATES[to_state],
             castle_from, castle_to, ep_from, ep_to,
             SQUARE_IDX[from2_tile], SQUARE_STATES[from2_state],
             SQUARE_IDX[to2_tile], SQUARE_STATES[to2_state],)
            for from_tile, from_state, to_tile, to_state,
                castle_from, castle_to, ep_from, ep_to,
                from2_tile, from2_state, to2_tile, to2_state, in zip(*instruction_gen_args))

    # Check it against what the engine returns
    actual_instructions = set(getattr(empty_board, func)(*args))
    print(f"{actual_instructions=}")
    print(f"{expected_instructions=}")

    # Redundant checking for easy debugging
    assert len(actual_instructions) == len(expected_instructions)
    for move in actual_instructions:
        assert move in expected_instructions
    for move in expected_instructions:
        assert move in actual_instructions
    assert actual_instructions == expected_instructions


def test_rook_move():
    # TODO:
    pass


def test_queen_move():
    # TODO:
    pass


def test_pawn_single_move():
    # TODO:
    pass


def test_pawn_double_move():
    # TODO:
    pass


def test_pawn_promote_no_take():
    # TODO:
    pass


def test_pawn_promote_take():
    # TODO:
    pass


def test_enpassant_take():
    # TODO:
    pass


def test_enpassant_no_take():
    # TODO:
    pass


def test_short_castle():
    # TODO:
    pass


def test_long_castle():
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
