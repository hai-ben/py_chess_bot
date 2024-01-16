import random
from src.small_board import SmallBoard

class SmallBoardAdapter:
    def __init__(self) -> None:
        self.current_state = SmallBoard()
        self.current_state.reset()
        self.current_moves = self.current_state.get_all_moves()
    
    def play_random_move(self):
        # print(f"Gamestate {bin(self.current_state.state)}")
        # print(f"White's Turn: {self.current_state.get_turn()}")
        # print(f"White in check: {self.current_state.in_check(1)}")
        # print(f"Black in check: {self.current_state.in_check(0)}")
        move, state = random.choice(list(self.current_moves.items()))
        # print(f"The move is {move} form the following state:")
        # print(self.current_state)
        self.current_state = state
        self.update_moves()
        return len(self.current_moves)
    
    def update_moves(self):
        self.current_moves = self.current_state.get_all_moves()