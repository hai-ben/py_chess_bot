"""A simple performance tester that takes a random walk down the chess board"""
import time
import tracemalloc
from src.main_engine_adapter import MainEngineAdapter
from src.prototyping.board import GameState
from src.prototyping.small_board_adapter import SmallBoardAdapter


def run_games(n_games=10, max_turns=100, adapter=GameState):
    """Takes random moves for n_games with up to max_turns each (combined for both players)
    Using the adapter"""
    total_moves_considered = 0
    for i in range(n_games):
        # Initialize with a random seed to compare apples to apples
        state = adapter(rand_seed = ((2 ** (i+5)) - (12345 * i)))
        for _j in range(max_turns):
            new_moves_count = state.play_random_move()
            total_moves_considered += new_moves_count
            if new_moves_count == 0:
                break
        if i % 50 == 0:
            print(f"Completed {i} games out of {n_games}")
    print(f"Ran {n_games} games considering {total_moves_considered} moves")


def perf_tracking(func, args=None, kwargs=None):
    """Tracks the run time and memory usage of func(*args, **kwargs)"""
    args = [] if args is None else args
    kwargs = {} if kwargs is None else kwargs
    tracemalloc.start()
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    mem_usage = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end_time - start_time, mem_usage


# # Old small board performance
# print("Running bitstring engine")
# total_time, mem = perf_tracking(run_games, kwargs={"adapter": SmallBoardAdapter})
# print(f"Bitstring ran in {total_time:1.4f}s with peak memory usage " +\
#       f"{(mem[1]):5.0f} bytes of memory at peak.")
# print(f"The program failed to release {(mem[0]):5.0f} bytes after execution.\n")


# New main engine performance
print("Running graph engine")
total_time, mem = perf_tracking(
    run_games, kwargs={"n_games": 10_000, "max_turns": 150, "adapter": MainEngineAdapter})
print(f"Graph engine ran in {total_time:1.4f}s with peak memory usage " +\
      f"{(mem[1]):5.0f} bytes of memory at peak.")
print(f"The program failed to release {(mem[0]):5.0f} bytes after execution.")
