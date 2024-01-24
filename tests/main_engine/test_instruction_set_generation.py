"""Tests that the instruction sets for each piece are generated correctly"""
import pytest
from instruction_set_cases.basic_cases import BASIC_MOVE_TESTS
from instruction_set_cases.advanced_cases import ADVANCED_MOVE_TESTS
from src.resources.data_translators import SQUARE_IDX, SQUARE_STATES
from src.main_engine import MainEngine

MOVE_TEST_DICT = BASIC_MOVE_TESTS | ADVANCED_MOVE_TESTS

# Using the move test dict keys as test parameters for easier debugging
@pytest.mark.parametrize("test_key", MOVE_TEST_DICT.keys())
def test_get_moves(board_state_generator, test_key: str):
    """After making modifications to empty board, this calls func_name of empty board with args
    and asserts the set of that return value is the same as the set of the expected_instructions"""
    # Unpack the test information
    mods, instruction_gen_args, (func, args) = MOVE_TEST_DICT[test_key]

    # Unpack the modifications to the state and apply them
    if mods:
        board = board_state_generator(mods)
    else:
        board = MainEngine()

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
             SQUARE_IDX.get(from2_tile, None), SQUARE_STATES.get(from2_state, None),
             SQUARE_IDX.get(to2_tile, None), SQUARE_STATES.get(to2_state, None),)
            for from_tile, from_state, to_tile, to_state,
                castle_from, castle_to, ep_from, ep_to,
                from2_tile, from2_state, to2_tile, to2_state, in zip(*instruction_gen_args))

    # Remove None instructions to allow for short instructions:
    new_set = set()
    for item in expected_instructions:
        if None in item:
            new_set.add(item[:item.index(None)])
        else:
            new_set.add(item)
    expected_instructions = new_set

    # Check it against what the engine returns
    actual_instructions = set(getattr(board, func)(*args))
    print(f"{actual_instructions=}")
    print(f"{expected_instructions=}")
    print(f"Board:\n{board}\n")

    # Redundant checking for easy debugging
    assert len(actual_instructions) == len(expected_instructions)
    for move in actual_instructions:
        assert move in expected_instructions
    for move in expected_instructions:
        assert move in actual_instructions
    assert actual_instructions == expected_instructions
