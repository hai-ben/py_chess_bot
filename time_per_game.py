"""A simple performance tester that takes a random walk down the chess board"""
import time
import tracemalloc
from src.protoyping.board import GameState
from src.protoyping.small_board_adapter import SmallBoardAdapter

def run_games(n_games=10, max_turns=100, adapter=GameState):
    """Takes random moves for n_games with up to max_turns each (combined for both players)
    Using the adapter"""
    total_moves_considered = 0
    for _i in range(n_games):
        state = adapter()
        for _j in range(max_turns):
            new_moves_count = state.play_random_move()
            total_moves_considered += new_moves_count
            if new_moves_count == 0:
                break
    print(f"Ran {n_games} with maximum {max_turns} considering {total_moves_considered} moves")


def perf_tracking(func, args=None, kwargs=None):
    """Tracks the run time and memory usage of func(*args, **kwargs)"""
    tracemalloc.start()
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    mem_usage = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end_time - start_time, mem_usage


total_time, mem = perf_tracking(run_games, kwargs={"adapter": SmallBoardAdapter})
print(f"Ran in {total_time:9.4f}s with peak memory usage " +\
      f"{(mem[1] / (1024 ** 2)):6.1f}MB of memory at peak.")
print(f"The program failed to release {(mem[0] / (1024 ** 2)):6.1f}MB after execution.")
