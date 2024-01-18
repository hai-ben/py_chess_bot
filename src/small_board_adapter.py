import random
from collections import Counter
from src.small_board import SmallBoard

class SmallBoardAdapter:
    def __init__(self) -> None:
        self.current_state = SmallBoard()
        self.current_state.reset()
        self.current_moves = self.current_state.get_all_moves()
        self.draw_counter = 100
        self.visited_state = Counter()
    
    def play_random_move(self):
        # _ = input()
        # print(f"Gamestate {bin(self.current_state.state)}")
        # print(f"White's Turn: {self.current_state.get_turn()}")
        # print(f"White in check: {self.current_state.in_check(1)}")
        # print(f"Black in check: {self.current_state.in_check(0)}")
        # print("THE MOVES IS " + move)
        # print(self.current_state.state)

        move, state = random.choice(list(self.current_moves.items()))
        
        # Repeated state check
        if self.visited_state[state] == 2:
            return 0
        self.visited_state[state] += 1

        # No moves state:
        if not state.sufficient_material():
            return 0

        self.current_state = state
        self.update_moves()
        return len(self.current_moves)
    
    def update_moves(self):
        self.current_moves = self.current_state.get_all_moves()