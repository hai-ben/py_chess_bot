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
        self.state = state or STARTING_STATE.copy()
        self.game_graph = {}
        self.state_stack = deque()
        self.hash_stack = deque()
        self.iter_counter = 0

        # Initialize the hash
        self.hash = None
        self.hash = hash(self)

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

    def execute_instructions(self, instruction_set: tuple):
        """Executes the instruction_set tuple, altering the hash and list,
        appending the instructions to the state_stack and updating the graph
        an instruction set has the following construction:
        (from_square_idx, from_square_state, to_square_idx, to_square_state,
        from_castle_state, to_castle_state, from_ep_state, to_ep_state)
        The last 4 entries are left blank if there is no update

        If the instruction set has a castling move in it the construction is:
        (from_king_idx, from_king_state, to_king_idx, to_king_state,
        from_castle_state, to_castle_state, from_ep_state, to_ep_state,
        from_rook_idx, from_rook_state, to_rook_idx, to_rook_state)

        The hashing functionality is left in this function because it avoids
        extra checks on the length of the instructions."""
        self.state_stack.append(instruction_set)
        self.hash_stack.append(hash(self))

        # Remove the piece from the start idx
        self.state[instruction_set[0]] = 0
        self.hash ^= ZOBRIST_TABLE[instruction_set[0]][instruction_set[1]]
        self.hash ^= ZOBRIST_TABLE[instruction_set[0]][0]

        # Place the piece on the the target idx
        self.state[instruction_set[2]] = instruction_set[1]  # Put it on the second tile
        self.hash ^= ZOBRIST_TABLE[instruction_set[2]][instruction_set[3]]
        self.hash ^= ZOBRIST_TABLE[instruction_set[2]][instruction_set[1]]

        # Update the king position, this will not happen later due to the data struct definition
        if self.state[64 + self.state[-1]] == instruction_set[0]:
            self.state[64 + self.state[-1]] = instruction_set[2]

        # Update Castling rights
        if len(instruction_set) > 4:
            # Update castling information
            self.state[66] = instruction_set[5]
            self.hash ^= ZOBRIST_TABLE[66][instruction_set[4]]
            self.hash ^= ZOBRIST_TABLE[66][instruction_set[5]]

            # Update en_passant information
            self.state[67] = instruction_set[7]
            self.hash ^= ZOBRIST_TABLE[67][instruction_set[6]]
            self.hash ^= ZOBRIST_TABLE[67][instruction_set[7]]

            # Double instruction (castling) moves:
            if len(instruction_set) > 8:
                # Move away
                self.state[instruction_set[8]] = 0
                self.hash ^= ZOBRIST_TABLE[instruction_set[8]][instruction_set[9]]
                self.hash ^= ZOBRIST_TABLE[instruction_set[8]][0]

                # Move towards
                self.state[instruction_set[10]] = instruction_set[9]
                self.hash ^= ZOBRIST_TABLE[instruction_set[10]][instruction_set[11]]
                self.hash ^= ZOBRIST_TABLE[instruction_set[10]][instruction_set[9]]

        # Update the player's turn
        self.hash ^= ZOBRIST_TABLE[68][self.state[-1]]
        self.state[-1] = not self.state[-1]
        self.hash ^= ZOBRIST_TABLE[68][self.state[-1]]

        # Update the game graph
        self.game_graph[self.hash_stack[-1]] = (instruction_set, hash(self))

    def reverse_last_instruction(self):
        """Reverses the last instruction on the stack"""
        # Put the piece back on the start_idx
        instruction_set = self.state_stack.pop()
        self.state[instruction_set[0]] = instruction_set[1]

        # Restore the to_idx square
        self.state[instruction_set[2]] = instruction_set[3]

        # Castling and en_passant updates
        if len(instruction_set) > 4:
            self.state[66] = instruction_set[4]
            self.state[67] = instruction_set[6]

            # Double instruction moves
            if len(instruction_set) > 8:
                self.state[instruction_set[8]] = instruction_set[9]
                self.state[instruction_set[10]] = instruction_set[11]

        # Update the player's turn
        self.state[-1] = not self.state[-1]

        # Update the hash
        self.hash = self.hash_stack.pop()
