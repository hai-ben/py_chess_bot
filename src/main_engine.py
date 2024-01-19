"""Chess engine uses a list for a state and a graph to track relations"""
from collections import deque
from src.resources.zobrist_hashes import ZOBRIST_TABLE

ASCII_LOOKUP = {1: "♙",  2: "♘", 3: "♗", 4: "♖", 5: "♕", 6: "♔",
                7: "♟︎", 8: "♞", 9: "♝", 10: "♜", 11: "♛", 12: "♚"}
LIGHT_TILE, DARK_TILE = "□", "■"
STARTING_STATE =\
    [10, 8, 9, 11, 12, 9, 8, 10] + [7] * 8\
    + [0] * 8 + [0] * 8 + [0] * 8 + [0] * 8\
    + [1] * 8 + [4, 2, 3, 5, 6, 3, 2, 4]\
    + [4] + [60] + [0b1111] + [-1] + [True]


class MainEngine:
    """See data_structures.md for detailed data structure information"""
    def __init__(self, state: list=None) -> None:
        self.state = state or STARTING_STATE
        self.game_graph = {}
        self.state_stack = deque()
        self.iter_counter = 0
        self.hash = None

    def __iter__(self):
        self.iter_counter = 0
        return self

    def __next__(self):
        self.iter_counter += 1
        if self.iter_counter < 65:
            return self.state[self.iter_counter - 1]
        raise StopIteration

    def __str__(self) -> str:
        out_str = ""
        for idx, state in enumerate(self):
            if state == 0:
                if (idx // 8  + idx) % 2 == 0:
                    out_str += LIGHT_TILE
                else:
                    out_str += DARK_TILE
            else:
                out_str += ASCII_LOOKUP[state]
            out_str += " "
            if idx > 0 and (idx + 1) % 8 == 0:
                out_str += "\n"
        return out_str[:-1]

    def __hash__(self):
        if self.hash is None:
            self.hash = ZOBRIST_TABLE[68][self.state[-1]]
            self.hash ^= ZOBRIST_TABLE[67][self.state[67]]
            self.hash ^= ZOBRIST_TABLE[66][self.state[66]]
            for idx, val in enumerate(self):
                self.hash ^= ZOBRIST_TABLE[idx][val]
        return self.hash
