"""Generate an importable zobrist hashtable"""
import random

RAND_RANGE = (2**64) - 1
random.seed(21221)  # Should make the table the same for each import

# For each square on the chessboard, make a random 64-bit number for each state to use as a hash
ZOBRIST_TABLE = {idx: {s: random.randrange(RAND_RANGE) for s in range(13)} for idx in range(64)}

# Do the same with castle states, en passant states, and the player turn
ZOBRIST_TABLE[66] = {s: random.randrange(RAND_RANGE) for s in range(0b1111 + 1)}
ZOBRIST_TABLE[67] = {s: random.randrange(RAND_RANGE) for s in range(-1, 8)}
ZOBRIST_TABLE[68] = {True: random.randrange(RAND_RANGE), False: random.randrange(RAND_RANGE)}
