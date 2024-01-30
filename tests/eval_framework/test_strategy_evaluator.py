"""Used to test the the strategy evaluator"""
import pytest
from src.main_engine import MainEngine
from src.strategy_eval import StrategyEvaluator


def test_init():
    """Tests that the the strategy evaluator takes two evaluation functions"""
    # pylint: disable=unnecessary-lambda-assignment
    func_1 = lambda: None
    func_2 = lambda x: x
    evaluator = StrategyEvaluator(strategy1 = func_1, strategy2 = func_2, rand_seed = 21221)
    assert evaluator.strat1 == func_1
    assert evaluator.strat2 == func_2
    assert isinstance(evaluator.engine, MainEngine)
    assert isinstance(evaluator.strat1_evals, dict)
    assert isinstance(evaluator.strat2_evals, dict)
    assert evaluator.strat1_is_white is True


def test_explore_children_of_current():
    """Checks that the explore children of current node visits all the children
    of the current state stores the results of the evaluation functions in a dict.
    Also checks that it returns to the start state"""
    # pylint: disable=unnecessary-lambda-assignment
    func_1 = lambda _: 10
    func_2 = lambda _: 5
    evaluator = StrategyEvaluator(strategy1 = func_1, strategy2 = func_2)
    evaluator.explore_children_of_current()

    assert len(evaluator.strat1_evals) == 20
    assert len(evaluator.strat2_evals) == 20
    for score in evaluator.strat1_evals.values():
        assert score == 10

    for score in evaluator.strat2_evals.values():
        assert score == 5

    assert evaluator.engine.state == MainEngine().state


def test_play_best_move():
    """Checks that the best move is played from the lookup dict, high for white, low for black"""
    # pylint: disable=unnecessary-lambda-assignment
    func_1 = lambda x: (1 if x[47] == 1 else 0)  # always choses h3
    func_2 = lambda x: (-1 if x[23] == 7 else 0)  # always choses h6
    evaluator = StrategyEvaluator(strategy1 = func_1, strategy2 = func_2)
    evaluator.play_best_move()
    assert evaluator.engine.state[47] == 1
    evaluator.play_best_move()
    assert evaluator.engine.state[23] == 7
