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
