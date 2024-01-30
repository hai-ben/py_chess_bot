"""A simple way to perform a random walk down a board state using the instruction-set based board"""
import random
from collections import Counter
from src.main_engine import MainEngine


class MainEngineAdapter:
    """A way to perform a random walk down a board state using SmallBoard"""
    def __init__(self, rand_seed:int = 21221) -> None:
        self.engine = MainEngine()
        self.current_moves = self.engine.get_all_moves()
        self.draw_counter = 100
        self.visited_state = Counter()
        random.seed(rand_seed)

    def play_random_move(self) -> int:
        """ Plays random moves on a board itself until there are no more
        moves or a draw state is reached. It's expected that some other context repeadetly
        calls this function until it returns 0 or some other condition"""
        # If threre are no moves
        self.update_moves()
        if len(self.current_moves) == 0:
            return 0

        # Otherwise pick a move at random and execute it
        move = random.choice(self.current_moves)
        self.engine.execute_instructions(move)
        # try:
        #     self.engine.execute_instructions(move)
        # except KeyError as e:
        #     print(f"ENCOUNTERED ERROR: {e}")
        #     print(f"MOVES TO GET HERE: {self.engine.state_stack}")
        #     print(f"MOVE: {move}")
        #     print(f"BOARD CURRENT STATE: {self.engine.state}")
        #     print(f"VISUALIZED:\n{self.engine}")

        # If it repeats a state for a third time, it's a draw and try to exit
        if self.visited_state[hash(self.engine)] == 2:
            return 0
        self.visited_state[hash(self.engine)] += 1

        # If there's insufficient mating material try to exit
        if not self.engine.sufficient_material():
            return 0

        return len(self.current_moves)

    def update_moves(self):
        """Updates the possible moves for the current state"""
        self.current_moves = self.engine.get_all_moves()
