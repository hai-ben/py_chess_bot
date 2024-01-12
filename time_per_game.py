import time
import tracemalloc
from src.board import GameState

def run_games(n_games=10, max_turns=100):
    total_moves_considered = 0
    for i in range(n_games):
        state = GameState()
        for j in range(max_turns):
            new_moves_count = state.play_random_move()
            total_moves_considered += new_moves_count
            if new_moves_count == 0:
                break
    print(f"Ran {n_games} with maximum {max_turns} considering {total_moves_considered} moves")


def perf_tracking(func, args=[], kwargs={}):
    tracemalloc.start()
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    mem_usage = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end_time - start_time, mem_usage


total_time, mem = perf_tracking(run_games)
print(f"Ran in {total_time:9.4f}s with peak memory usage {(mem[1] / (1024 ** 2)):6.1f}MB of memory at peak.")
print(f"The program failed to release {(mem[0] / (1024 ** 2)):6.1f}MB after execution.")