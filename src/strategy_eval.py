"""Class used play two evaluation strategies against eachother"""
import random
from typing import Callable
from src.main_engine import MainEngine


class StrategyEvaluator:
    """Plays two evaluation strategies against eachother"""
    def __init__(self, strategy1: Callable, strategy2: Callable, rand_seed: int = 21221) -> None:
        self.strat1 = strategy1
        self.strat2 = strategy2
        self.engine = MainEngine()
        self.strat1_evals = {}
        self.strat2_evals = {}
        self.strat1_is_white = True
        random.seed(rand_seed)

    def explore_children_of_current(self) -> None:
        """Explores all the children of the current node and caches their evaluations"""
        new_moves = self.engine.get_all_moves()
        for move in new_moves:
            self.engine.execute_instructions(move)
            self.strat1_evals[hash(self.engine)] = self.strat1(self.engine.state)
            self.strat2_evals[hash(self.engine)] = self.strat2(self.engine.state)
            self.engine.reverse_last_instruction()

    def play_best_move(self) -> None:
        """Plays the best move for the strategies given the turn"""
        # If the moves of the children have not been evaluated, evaluate them
        if hash(self.engine) not in self.engine.game_graph:
            self.explore_children_of_current()
        print(self.engine.game_graph)
        instructions, states = zip(*self.engine.game_graph[hash(self.engine)])

        # Get the proper evaluations
        if (self.strat1_is_white and self.engine.state[-1])\
                or (not self.strat1_is_white and not self.engine.state[-1]):
            evaluations = [self.strat1_evals[state] for state in states]
        else:
            evaluations = [self.strat2_evals[state] for state in states]

        # Find out what the best score is
        if self.engine.state[-1]:
            value_to_match = max(evaluations)
        else:
            value_to_match = min(evaluations)

        # Play a move that's tied for "best"
        print(evaluations)
        candidates = [idx for idx, score in enumerate(evaluations) if score == value_to_match]
        print(candidates)
        self.engine.execute_instructions(instructions[random.choice(candidates)])
        