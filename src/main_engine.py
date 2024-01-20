"""Chess engine uses a list for a state and a graph to track relations"""
from collections import deque
from src.resources.move_dict import KING_MOVES, KNIGHT_MOVES, BISHOP_MOVES, ROOK_MOVES,\
    QUEEN_MOVES, PAWN_SINGLE_MOVES_WHITE, PAWN_SINGLE_MOVES_BLACK, PAWN_DOUBLE_MOVES_WHITE,\
    PAWN_DOUBLE_MOVES_BLACK
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

    def get_king_moves(self) -> list[tuple]:
        """Gets all the possible king move instructions (not castling) for the active player"""
        # These statements can be merged but it requires additional variable assignment
        # If it's white's turn
        if self.state[-1]:
            king_idx = self.state[65]
            castle_to_state = self.state[66] & 0b1100
            return [
                (king_idx, self.state[king_idx],
                 target_idx, self.state[target_idx],
                 self.state[66], castle_to_state, self.state[67], -1)
                for target_idx in KING_MOVES[king_idx]
                if self.state[target_idx] == 0 or self.state[target_idx] > 6
            ]

        # Otherwise get the moves for black's king
        king_idx = self.state[64]
        castle_to_state = self.state[66] & 0b0011
        return [
            (king_idx, self.state[king_idx],
             target_idx, self.state[target_idx],
             self.state[66], castle_to_state, self.state[67], -1)
            for target_idx in KING_MOVES[king_idx]
            if self.state[target_idx] < 7
        ]

    def get_knight_moves(self, knight_idx: int) -> list[tuple]:
        """Gets all the possible knight move instructions for the active player
        for the knight on knight_idx"""
        if self.state[-1]:
            if self.state[67] > 0:
                return [
                    (knight_idx, self.state[knight_idx],
                        target_idx, self.state[target_idx],
                        self.state[66], self.state[66], self.state[67], -1)
                    for target_idx in KNIGHT_MOVES[knight_idx]
                        if self.state[target_idx] == 0 or self.state[target_idx] > 6
                ]
            return [
                (knight_idx, self.state[knight_idx],
                    target_idx, self.state[target_idx])
                for target_idx in KNIGHT_MOVES[knight_idx]
                    if self.state[target_idx] == 0 or self.state[target_idx] > 6
            ]
        if self.state[67] > 0:
            return [
                (knight_idx, self.state[knight_idx],
                    target_idx, self.state[target_idx],
                    self.state[66], self.state[66], self.state[67], -1)
                for target_idx in KNIGHT_MOVES[knight_idx]
                    if self.state[target_idx] < 7
            ]
        return [
            (knight_idx, self.state[knight_idx],
                target_idx, self.state[target_idx])
            for target_idx in KNIGHT_MOVES[knight_idx]
                if self.state[target_idx] < 7
        ]

    def get_blockable_moves(self, start_idx:int, move_dict: dict,
                            additional_state_info: tuple) -> list[tuple]:
        """Goes through each move direction in move_dict for the square at
        start_idx. Adds moves to move list until it runs into a piece or out
        of moves. Performs a capture if the piece is not controlled by the
        current player"""

        move_list = []
        for direction in move_dict[start_idx]:
            for square_idx in direction:
                # If the square is empty, append a move and go to the next
                if self.state[square_idx] == 0:
                    move_list.append((start_idx, self.state[start_idx],
                                      square_idx, self.state[square_idx])\
                                     + additional_state_info)
                    continue
                # If it's white's turn and the piece is controlled by black
                if self.state[-1] and self.state[square_idx] > 6:
                    move_list.append((start_idx, self.state[start_idx],
                                        square_idx, self.state[square_idx])\
                                        + additional_state_info)
                # If it's black's turn and the piece is controlled by white
                elif not self.state[-1] and self.state[square_idx] < 7:
                    move_list.append((start_idx, self.state[start_idx],
                                      square_idx, self.state[square_idx])\
                                     + additional_state_info)
                # Don't continue in this direction as there is a piece here
                break
        return move_list

    def get_bishop_moves(self, bishop_idx: int) -> list[tuple]:
        """Gets all the possible bishop move instructions for
        the active player for the bishop on bishop_idx"""
        if self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)
        else:
            additional_state_info = ()

        return self.get_blockable_moves(bishop_idx, BISHOP_MOVES, additional_state_info)

    def get_rook_moves(self, rook_idx: int) -> list[tuple]:
        """Gets all the possible rook move instructions for
        the active player for the rook on rook_idx"""
        additional_state_info = ()

        # Do castling information
        if self.state[-1]:
            if rook_idx == 63:  # White short castle
                additional_state_info += (self.state[66], self.state[66] & 0b1110)
            elif rook_idx == 56:  # White long castle
                additional_state_info += (self.state[66], self.state[66] & 0b1101)
        else:
            print("Blacks turn", rook_idx)
            if rook_idx == 0:  # Black long castle
                additional_state_info += (self.state[66], self.state[66] & 0b0111)
            elif rook_idx == 7:  # Black short castle
                additional_state_info += (self.state[66], self.state[66] & 0b1011)

        # Update en_passant information
        if additional_state_info:
            additional_state_info += (self.state[67], -1)
        elif self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)

        # Go through each direciton the rook can move
        return self.get_blockable_moves(rook_idx, ROOK_MOVES, additional_state_info)

    def get_queen_moves(self, queen_idx: int) -> list[tuple]:
        """Gets all the possible bishop move instructions for
        the active player for the bishop on bishop_idx"""
        if self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)
        else:
            additional_state_info = ()

        return self.get_blockable_moves(queen_idx, QUEEN_MOVES, additional_state_info)

    def get_white_promotion_moves(self, pawn_idx: int) -> list[tuple]:
        """Gets all the promotion moves for the white pawn on pawn_idx"""
        moves = []
        additional_state_info = (self.state[66], self.state[66], self.state[67], -1)

        # If the pawn can move forward
        if self.state[pawn_idx - 8] == 0:
            # There are some pre-generated tuples to use
            for move_a, move_b in PAWN_SINGLE_MOVES_WHITE[pawn_idx]:
                moves.append(move_a + additional_state_info + move_b)

        # If the pawn can attack left and promote
        if pawn_idx % 8 > 0 and self.state[pawn_idx - 9] > 6:
            for promotion_piece in range(2, 6):
                moves.append((pawn_idx, 1, pawn_idx, promotion_piece) + additional_state_info\
                                + (pawn_idx, promotion_piece,
                                pawn_idx - 9, self.state[pawn_idx - 9]))

        # If the pawn can attack right and promote
        if pawn_idx % 8 < 7 and self.state[pawn_idx - 7] > 6:
            for promotion_piece in range(2, 6):
                moves.append((pawn_idx, 1, pawn_idx, promotion_piece) + additional_state_info\
                                + (pawn_idx, promotion_piece,
                                pawn_idx - 7, self.state[pawn_idx - 7]))

        return moves

    def get_white_pawn_moves(self, pawn_idx: int) -> list[tuple]:
        """Gets all the possible moves for the white pawn at pawn_idx"""
        # If the pawn will promote on it's move
        if pawn_idx // 8 == 1:
            return self.get_white_promotion_moves(pawn_idx)

        moves = []

        # Only need the additional state_info if this move turns off en_passant
        if self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)
        else:
            additional_state_info = ()

        # If the pawn is not blocked
        if self.state[pawn_idx - 8] == 0:
            # Add the single move
            moves.append(PAWN_SINGLE_MOVES_WHITE[pawn_idx] + additional_state_info)

            # If the pawn is on the starting rank, and it's not blocked from double move
            if pawn_idx // 8 == 6 and self.state[pawn_idx - 16] == 0:
                moves.append(PAWN_DOUBLE_MOVES_WHITE[pawn_idx]\
                            + (self.state[66], self.state[66], self.state[67], pawn_idx % 8))

        # If the pawn can atack left
        if pawn_idx % 8 > 0:
            # If there's a piece to attack
            if self.state[pawn_idx - 9] > 6:
                moves.append((pawn_idx, 1, pawn_idx - 9, self.state[pawn_idx - 9])\
                                + additional_state_info)
            # If the pawn can is on the right rank and file to take via en passant
            elif pawn_idx // 8 == 3 and (pawn_idx - 1) % 8 == self.state[67]:
                moves.append((pawn_idx, 1, pawn_idx - 9, 0) + additional_state_info\
                             + (pawn_idx - 1, 0, pawn_idx - 1, 7))

        # Attack right
        if pawn_idx % 8 < 7:
            if self.state[pawn_idx - 7] > 6:
                moves.append((pawn_idx, 1, pawn_idx - 7, self.state[pawn_idx - 7])\
                                + additional_state_info)
            elif pawn_idx // 8 == 3 and (pawn_idx + 1) % 8 == self.state[67]:
                moves.append((pawn_idx, 1, pawn_idx - 7, 0) + additional_state_info\
                             + (pawn_idx + 1, 0, pawn_idx + 1, 7))
        return moves

    def get_black_promotion_moves(self, pawn_idx: int) -> list[tuple]:
        """Gets all the promotion moves for the black pawn on pawn_idx"""
        moves = []
        additional_state_info = (self.state[66], self.state[66], self.state[67], -1)

        # If the pawn can move forward
        if self.state[pawn_idx + 8] == 0:
            # There are some pre-generated tuples to use
            for move_a, move_b in PAWN_SINGLE_MOVES_BLACK[pawn_idx]:
                moves.append(move_a + additional_state_info + move_b)

        # If the pawn can attack left and promote
        if pawn_idx % 8 > 0 and 0 < self.state[pawn_idx + 7] < 7:
            for promotion_piece in range(8, 12):
                moves.append((pawn_idx, 7, pawn_idx, promotion_piece) + additional_state_info\
                                + (pawn_idx, promotion_piece,
                                pawn_idx + 7, self.state[pawn_idx + 7]))

        # If the pawn can attack right and promote
        if pawn_idx % 8 < 7 and 0 < self.state[pawn_idx + 9] < 7:
            for promotion_piece in range(8, 12):
                moves.append((pawn_idx, 7, pawn_idx, promotion_piece) + additional_state_info\
                                + (pawn_idx, promotion_piece,
                                pawn_idx + 9, self.state[pawn_idx + 9]))

        return moves

    def get_black_pawn_moves(self, pawn_idx: int) -> list[tuple]:
        """Gets all the possible moves for the black pawn at pawn_idx"""
        # If the pawn will promote
        if pawn_idx // 8 == 6:
            return self.get_black_promotion_moves(pawn_idx)

        moves = []
        if self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)
        else:
            additional_state_info = ()

        if self.state[pawn_idx + 8] == 0:
            moves.append(PAWN_SINGLE_MOVES_BLACK[pawn_idx] + additional_state_info)
            # Check for double move ahead
            if pawn_idx // 8 == 1 and self.state[pawn_idx + 16] == 0:
                moves.append(PAWN_DOUBLE_MOVES_BLACK[pawn_idx]\
                            + (self.state[66], self.state[66], self.state[67], pawn_idx % 8))

        # Attack left:
        if pawn_idx % 8 > 0:
            # If there is a piece to take
            if 0 < self.state[pawn_idx + 7] < 7:
                moves.append((pawn_idx, 7, pawn_idx + 7, self.state[pawn_idx + 7])\
                                + additional_state_info)
            # If the pawn can is on the right rank and file to take via en passant
            elif pawn_idx // 8 == 4 and (pawn_idx - 1) % 8 == self.state[67]:
                moves.append((pawn_idx, 7, pawn_idx + 7, 0) + additional_state_info\
                             + (pawn_idx - 1, 0, pawn_idx - 1, 1))

        # Attack right
        if pawn_idx % 8 < 7:
            # If there is a piece to take
            if 0 < self.state[pawn_idx + 9] < 7:
                moves.append((pawn_idx, 7, pawn_idx + 9, self.state[pawn_idx + 9])\
                                + additional_state_info)
            # If the pawn can is on the right rank and file to take via en passant
            elif pawn_idx // 8 == 4 and (pawn_idx + 1) % 8 == self.state[67]:
                moves.append((pawn_idx, 7, pawn_idx + 9, 0) + additional_state_info\
                             + (pawn_idx + 1, 0, pawn_idx + 1, 1))
        return moves

    def get_pawn_moves(self, pawn_idx: int) -> list[tuple]:
        """Gets all the possible pawn moves for the pawn on pawn_idx"""
        # If it's white's turn
        if self.state[-1]:
            return self.get_white_pawn_moves(pawn_idx)
        return self.get_black_pawn_moves(pawn_idx)

    def get_castle_moves(self) -> list[tuple]:
        """Gets all possible castling moves"""
        moves = []
        if self.state[66] == 0:
            return moves

        # Moving the king and or rook unsets the appropriate castle rights
        # This means only, check, and tween tiles need to be checked
        # If it's white's turn
        if self.state[-1]:
            if self.state[66] & 0b0001 and self.state[61] == 0 and self.state[62] == 0:
                moves.append((60, 6, 62, 0,
                              self.state[66], self.state[66] & 0b1100, self.state[67], -1,
                              63, 4, 61, 0))
            if self.state[66] & 0b0010 and self.state[57] == 0\
                    and self.state[58] == 0 and self.state[59] == 0:
                moves.append((60, 6, 58, 0,
                              self.state[66], self.state[66] & 0b1100, self.state[67], -1,
                              56, 4, 59, 0))
            return moves

        # Otherwise it's black's turn
        if self.state[66] & 0b0100 and self.state[5] == 0 and self.state[6] == 0:
            moves.append((4, 12, 6, 0,
                          self.state[66], self.state[66] & 0b0011, self.state[67], -1,
                          7, 10, 5, 0))
        if self.state[66] & 0b1000 and self.state[3] == 0\
                and self.state[2] == 0 and self.state[1] == 0:
            moves.append((4, 12, 2, 0,
                          self.state[66], self.state[66] & 0b0011, self.state[67], -1,
                          0, 10, 3, 0))
        return moves
