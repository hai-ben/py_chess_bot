- v00.00.01:
    - The engine seems to hit a memory leak or recursion issue around 4k-7k turns eating up vast amounts of memory.
- v00.01.00:
    - Fixed memory leak and got the following performance report:
        Ran 10 games with maximum 100 considering 31270 moves
        Ran in 54.3274s with peak memory usage 0.6MB of memory at peak.
- v00.02.00:
    - Added small_board, a highly memory effecient engine that had the performance:
        Ran 10 with maximum 100 considering 32083 moves
        Ran in 5.5599s with peak memory usage 0.0MB of memory at peak.
        The program failed to release 0.0MB after execution.
    - Fixed some bugs and made small performance tweaks
- v00.02.02:
    - Tracked king positions to improve performance:
        Ran 10 with maximum 100 considering 30563 moves
        Ran in 3.4484s with peak memory usage 0.0MB of memory at peak.
        The program failed to release 0.0MB after execution.
- v00.02.03:
    - Attemped to preform a move_revealed_check to exit threat detection early but performance testing was worse, reverting in future releases
        Ran 10 with maximum 100 considering 31040 moves
        Ran in 3.6150s with peak memory usage 0.0MB of memory at peak.
        The program failed to release 0.0MB after execution.
- v00.02.04:
    - Dictionarized the move computation resulting in very large time savings:
        Ran 10 with maximum 100 considering 19331 moves
        Ran in 1.3716s with peak memory usage 0.0MB of memory at peak.
        The program failed to release 0.0MB after execution.
    - The moves considered is significantly lower, I wonder if this is a bug fix or a bug introduction
- v00.02.05:
    - Fixed a bug causing pieces to dissapear
        Ran 10 with maximum 100 considering 30652 moves
        Ran in 2.0223s with peak memory usage 0.1MB of memory at peak.
        The program failed to release 0.0MB after execution.
- v00.02.06:
    - Improved performance of get_tile:
        Ran 10 with maximum 100 considering 32056 moves
        Ran in 1.3503s with peak memory usage 0.1MB of memory at peak.
        The program failed to release 0.0MB after execution.
- v00.03.01:
    - Switched over to a graph-based engine for faster read/writes
    - Added seeds for the random library to make comparisons consistent
    - New Performance:
        Ran 10 games considering 28915 moves
        Graph engine ran in 0.7498s with peak memory usage 44320 bytes of memory at peak.
- v00.03.02:
    - Switched to checking for illegal positions before moves are made instead of after
        Ran 10 games considering 30591 moves
        Graph engine ran in 0.1647s with peak memory usage 43736 bytes of memory at peak.
        The program failed to release 15344 bytes after execution.
    - Difference is likely due to bugs found in some of the move_dict_generator functions
- v00.03.03:
    - Dictionarized the _move_reveals_check function to get a ~10% speedup
        Considering ~43M states is ran at 459s in main engine vs 500s for the last commit.  
- v00.03.05:
    - Stopped using my custom __iter__ function for another 10% speedup.
        Considering ~43M states ran in 423s with profiler
- v00.03.07:
    - Improved some logic branching for ~7% speedup.
        Considering ~43M states ran in 394s with profiler
- v00.03.08:
    - Found a bug where a capturing a rook did not remove castling rights. Now running at 410s with profiler for 43M states
