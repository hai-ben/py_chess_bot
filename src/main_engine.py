"""Chess engine uses a list for a state and a graph to track relations"""
from collections import deque, defaultdict
from src.resources.move_dict import KING_MOVES, KNIGHT_MOVES, BISHOP_MOVES, ROOK_MOVES,\
    QUEEN_MOVES, PAWN_SINGLE_MOVES_WHITE, PAWN_SINGLE_MOVES_BLACK, PAWN_DOUBLE_MOVES_WHITE,\
    PAWN_DOUBLE_MOVES_BLACK, BLOCKABLE_ATTACK_DICT_WHITE, BLOCKABLE_ATTACK_DICT_BLACK,\
    UNBLOCKABLE_ATTACKS_AT, MOVES_TO_BLOCK_ATTACK_ON_FROM, VECTOR_TO_SQUARE_FROM,\
    WHITE_THREATS_IN_DIRECTION, BLACK_THREATS_IN_DIRECTION, MOVES_FROM_SQUARE_ALONG_VECTOR
from src.resources.zobrist_hashes import ZOBRIST_TABLE

ASCII_LOOKUP = {1: "♙",  2: "♘", 3: "♗", 4: "♖", 5: "♕", 6: "♔",
                7: "♟︎", 8: "♞", 9: "♝", 10: "♜", 11: "♛", 12: "♚"}
LIGHT_TILE, DARK_TILE = "□", "■"
STARTING_STATE =\
    [10, 8, 9, 11, 12, 9, 8, 10] + [7] * 8\
    + [0] * 8 + [0] * 8 + [0] * 8 + [0] * 8\
    + [1] * 8 + [4, 2, 3, 5, 6, 3, 2, 4]\
    + [4] + [60] + [0b1111] + [-1] + [True]
SUFFICIENT_MATERIAL = {1, 4, 5, 7, 10, 11}
WHITE_PIECES = {1, 2, 3, 4, 5, 6}
BLACK_PIECES = {7, 8, 9, 10, 11, 12}
CASTLE_RIGHT_REMOVAL = {0: 0b0111, 7: 0b1011, 56: 0b1101, 63: 0b1110}


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
        for idx, state in enumerate(self.state[:64]):
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
            for idx, val in enumerate(self.state[:64]):
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
        instruction_set = self.state_stack.pop()

        # Update the king position if it changed
        if self.state[64 + (not self.state[-1])] == instruction_set[2]:
            self.state[64 + (not self.state[-1])] = instruction_set[0]

        # Put the piece back on the start_idx
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

    def _get_black_king_moves(self, king_idx: int) -> list[tuple]:
        """Gets all the possible king move instructions (not castling) for black"""
        # If black has any castling rights or there is an enpassant
        if self.state[66] & 0b1100 or self.state[67] >= 0:
            castle_to_state = self.state[66] & 0b0011
            return [
                (king_idx, self.state[king_idx],
                target_idx, self.state[target_idx],
                self.state[66], castle_to_state, self.state[67], -1)
                for target_idx in KING_MOVES[king_idx]
                if self.state[target_idx] < 7
            ]
        # Otherwise don't include them in the return statement
        return [
            (king_idx, self.state[king_idx], target_idx, self.state[target_idx],)
            for target_idx in KING_MOVES[king_idx] if self.state[target_idx] < 7
        ]

    def _get_white_king_moves(self, king_idx: int) -> list[tuple]:
        """Gets all the possible king move instructions (not castling) for white"""
        # If white has any castling rights remove them
        if self.state[66] & 0b0011 or self.state[67] >= 0:
            castle_to_state = self.state[66] & 0b1100
            return [
                (king_idx, self.state[king_idx],
                    target_idx, self.state[target_idx],
                    self.state[66], castle_to_state, self.state[67], -1)
                for target_idx in KING_MOVES[king_idx]
                if self.state[target_idx] == 0 or self.state[target_idx] > 6
            ]
        # Otherwise don't include them in the return statement
        return [
            (king_idx, self.state[king_idx], target_idx, self.state[target_idx])
                for target_idx in KING_MOVES[king_idx]
                    if self.state[target_idx] == 0 or self.state[target_idx] > 6
        ]

    def _get_knight_moves_black(self, knight_idx: int) -> list[tuple]:
        """Gets all the possible knight move instructions for the black player
        for the knight on knight_idx"""
        if self.state[67] >= 0:
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

    def _get_knight_moves_white(self, knight_idx: int) -> list[tuple]:
        """Gets all the possible knight move instructions for the white player
        for the knight on knight_idx"""
        if self.state[67] >= 0:
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

    def _get_blockable_moves_black(self, start_idx:int, move_dict: dict,
                                   additional_state_info: tuple) -> list[tuple]:
        """Goes through each move direction in move_dict for the square at
        start_idx. Adds moves to move list until it runs into a piece or out
        of moves. Performs a capture if the piece is not controlled by the
        black"""
        move_list = []
        for direction in move_dict[start_idx]:
            for square_idx in direction:
                # If the square is empty, append a move and go to the next
                if self.state[square_idx] == 0:
                    move_list.append((start_idx, self.state[start_idx],
                                      square_idx, self.state[square_idx])\
                                      + additional_state_info)
                    continue
                # If the piece is controlled by white
                if self.state[square_idx] < 7:
                    move_list.append((start_idx, self.state[start_idx],
                                      square_idx, self.state[square_idx])\
                                     + additional_state_info)
                # Don't continue in this direction as there is a piece here
                break
        return move_list

    def _get_blockable_moves_white(self, start_idx:int, move_dict: dict,
                                   additional_state_info: tuple) -> list[tuple]:
        """Goes through each move direction in move_dict for the square at
        start_idx. Adds moves to move list until it runs into a piece or out
        of moves. Performs a capture if the piece is not controlled by the
        white"""
        move_list = []
        for direction in move_dict[start_idx]:
            for square_idx in direction:
                # If the square is empty, append a move and go to the next
                if self.state[square_idx] == 0:
                    move_list.append((start_idx, self.state[start_idx],
                                      square_idx, self.state[square_idx])\
                                     + additional_state_info)
                    continue
                # If the piece is controlled by black
                if self.state[square_idx] > 6:
                    move_list.append((start_idx, self.state[start_idx],
                                      square_idx, self.state[square_idx])\
                                      + additional_state_info)
                # Don't continue in this direction as there is a piece here
                break
        return move_list

    def _get_bishop_moves_black(self, bishop_idx: int) -> list[tuple]:
        """Gets all the possible bishop move instructions for
        the active player for the bishop on bishop_idx"""
        if self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)
        else:
            additional_state_info = ()

        return self._get_blockable_moves_black(bishop_idx, BISHOP_MOVES, additional_state_info)

    def _get_bishop_moves_white(self, bishop_idx: int) -> list[tuple]:
        """Gets all the possible bishop move instructions for
        the active player for the bishop on bishop_idx"""
        if self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)
        else:
            additional_state_info = ()

        return self._get_blockable_moves_white(bishop_idx, BISHOP_MOVES, additional_state_info)

    def _get_rook_moves_black(self, rook_idx: int) -> list[tuple]:
        """Gets all the possible rook move instructions for
        the black for the rook on rook_idx"""
        additional_state_info = ()
        if rook_idx == 0:  # Black long castle
            additional_state_info += (self.state[66], self.state[66] & 0b0111)
        elif rook_idx == 7:  # Black short castle
            additional_state_info += (self.state[66], self.state[66] & 0b1011)

        # Update en_passant information
        if additional_state_info:
            additional_state_info += (self.state[67], -1)
        elif self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)

        return self._get_blockable_moves_black(rook_idx, ROOK_MOVES, additional_state_info)

    def _get_rook_moves_white(self, rook_idx: int) -> list[tuple]:
        """Gets all the possible rook move instructions for
        the white for the rook on rook_idx"""
        additional_state_info = ()
        if rook_idx == 63:  # White short castle
            additional_state_info += (self.state[66], self.state[66] & 0b1110)
        elif rook_idx == 56:  # White long castle
            additional_state_info += (self.state[66], self.state[66] & 0b1101)

        # Update en_passant information
        if additional_state_info:
            additional_state_info += (self.state[67], -1)
        elif self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)

        return self._get_blockable_moves_white(rook_idx, ROOK_MOVES, additional_state_info)

    def _get_queen_moves_black(self, queen_idx: int) -> list[tuple]:
        """Gets all the possible bishop move instructions for
        black for the queen on queen_idx"""
        if self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)
        else:
            additional_state_info = ()

        return self._get_blockable_moves_black(queen_idx, QUEEN_MOVES, additional_state_info)

    def _get_queen_moves_white(self, queen_idx: int) -> list[tuple]:
        """Gets all the possible queen move instructions for
        white for the queen on queen_idx"""
        if self.state[67] >= 0:
            additional_state_info = (self.state[66], self.state[66], self.state[67], -1)
        else:
            additional_state_info = ()

        return self._get_blockable_moves_white(queen_idx, QUEEN_MOVES, additional_state_info)

    def _get_white_promotion_moves(self, pawn_idx: int) -> list[tuple]:
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

    def _get_white_pawn_moves(self, pawn_idx: int) -> list[tuple]:
        """Gets all the possible moves for the white pawn at pawn_idx"""
        # If the pawn will promote on it's move
        if pawn_idx // 8 == 1:
            return self._get_white_promotion_moves(pawn_idx)

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

    def _get_black_promotion_moves(self, pawn_idx: int) -> list[tuple]:
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

    def _get_black_pawn_moves(self, pawn_idx: int) -> list[tuple]:
        """Gets all the possible moves for the black pawn at pawn_idx"""
        # If the pawn will promote
        if pawn_idx // 8 == 6:
            return self._get_black_promotion_moves(pawn_idx)

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
            return self._get_white_pawn_moves(pawn_idx)
        return self._get_black_pawn_moves(pawn_idx)

    def _get_castle_moves_black(self) -> list[tuple]:
        """Gets castling moves for black"""
        moves = []

        # If black is in check
        if self._square_attacked_by_white(self.state[64]):
            return moves

        if self.state[66] & 0b0100 and self._squares_empty_and_safe_from_white((5, 6)):
            moves.append((4, 12, 6, 0,
                          self.state[66], self.state[66] & 0b0011, self.state[67], -1,
                          7, 10, 5, 0))
        if self.state[66] & 0b1000 and self._squares_empty_and_safe_from_white((3, 2, 1)):
            moves.append((4, 12, 2, 0,
                          self.state[66], self.state[66] & 0b0011, self.state[67], -1,
                          0, 10, 3, 0))

        return moves

    def _get_castle_moves_white(self) -> list[tuple]:
        """Gets castling moves for white"""
        moves = []

        # If white is in check
        if self._square_attacked_by_black(self.state[65]):
            return moves

        # If white has short castling rights and the tiles are clear and safe
        if self.state[66] & 0b0001 and self._squares_empty_and_safe_from_black((61, 62)):
            moves.append((60, 6, 62, 0,
                            self.state[66], self.state[66] & 0b1100, self.state[67], -1,
                            63, 4, 61, 0))

        # If white has long castling rights and the tiles are clear and safe
        if self.state[66] & 0b0010 and self._squares_empty_and_safe_from_black((57, 58, 59)):
            moves.append((60, 6, 58, 0,
                            self.state[66], self.state[66] & 0b1100, self.state[67], -1,
                            56, 4, 59, 0))
        return moves

    def _attacks_on_square_by_black(self, square: int) -> list[int]:
        """Gets all of the attacks on square by a black piece"""
        # Check if the square is being attacked by a black knight
        attacking_indicies = []
        for attacking_idx in KNIGHT_MOVES[square]:
            if self.state[attacking_idx] == 8:
                attacking_indicies.append(attacking_idx)

        for attacking_direciton in BLOCKABLE_ATTACK_DICT_BLACK[square]:
            for attacking_idx, threats in attacking_direciton:
                if self.state[attacking_idx] in threats:
                    attacking_indicies.append(attacking_idx)
                if self.state[attacking_idx] > 0:
                    break
        return attacking_indicies

    def _attacks_on_square_by_white(self, square: int) -> list[int]:
        """Gets all of the attacks on square by a white piece"""
        # Check if the square is being attacked by a black knight
        attacking_indicies = []
        for attacking_idx in KNIGHT_MOVES[square]:
            if self.state[attacking_idx] == 2:
                attacking_indicies.append(attacking_idx)

        for attacking_direciton in BLOCKABLE_ATTACK_DICT_WHITE[square]:
            for attacking_idx, threats in attacking_direciton:
                if self.state[attacking_idx] in threats:
                    attacking_indicies.append(attacking_idx)
                if self.state[attacking_idx] > 0:
                    break
        return attacking_indicies

    def _square_attacked_by_black(self, square: int) -> bool:
        """Checks whether the square is being attacked by a black piece"""
        # Check if the square is being attacked by a black knight
        for attacking_idx in KNIGHT_MOVES[square]:
            if self.state[attacking_idx] == 8:
                return True

        for attacking_direciton in BLOCKABLE_ATTACK_DICT_BLACK[square]:
            for attacking_idx, threats in attacking_direciton:
                if self.state[attacking_idx] in threats:
                    return True
                if self.state[attacking_idx] > 0:
                    break
        return False

    def _square_attacked_by_white(self, square: int) -> bool:
        """Checks whether the square is being attacked by a white piece"""
        # Check if the square is being attacked by a white knight
        for attacking_idx in KNIGHT_MOVES[square]:
            if self.state[attacking_idx] == 2:
                return True

        for attacking_direciton in BLOCKABLE_ATTACK_DICT_WHITE[square]:
            for attacking_idx, threats in attacking_direciton:
                if self.state[attacking_idx] in threats:
                    return True
                if self.state[attacking_idx] > 0:
                    break
        return False

    def _square_attacked_by_player(self, square: int, player_is_white: bool) -> bool:
        """Returns all the squares where a piece controlled by the given player
         is attacking the given square."""
        if player_is_white:
            return self._square_attacked_by_white(square)
        return self._square_attacked_by_black(square)

    def _squares_empty_and_safe_from_black(self, squares: tuple[int]) -> bool:
        """Returns True if the given squares are empty and are safe from attacks from black"""
        for square in squares:
            if self.state[square] > 0:
                return False
            if self._square_attacked_by_black(square):
                return False
        return True

    def _squares_empty_and_safe_from_white(self, squares: tuple[int]) -> bool:
        """Returns True if the given squares are empty and are safe from attacks from white"""
        for square in squares:
            if self.state[square] > 0:
                return False
            if self._square_attacked_by_white(square):
                return False
        return True

    def squares_attacking_king(self, player_is_white: bool=None) -> list[int]:
        "Checks the tile the player's king is on is threatened by a piece of the enemy"
        player_is_white = self.state[-1] if player_is_white is None else player_is_white
        if player_is_white:
            return self._attacks_on_square_by_black(self.state[65])
        return self._attacks_on_square_by_white(self.state[64])

    def get_white_moves(self) -> list[tuple]:
        """Gets all the moves for white in the current position"""
        moves = []
        moves.extend(self._get_castle_moves_white())
        for idx, state in enumerate(self.state[:64]):
            if state == 0 or state > 6:
                continue
            if state == 1:
                moves.extend(self._get_white_pawn_moves(idx))
            elif state == 2:
                moves.extend(self._get_knight_moves_white(idx))
            elif state == 3:
                moves.extend(self._get_bishop_moves_white(idx))
            elif state == 4:
                moves.extend(self._get_rook_moves_white(idx))
            elif state == 5:
                moves.extend(self._get_queen_moves_white(idx))
            else:
                moves.extend(self._get_white_king_moves(idx))
        return moves

    def get_black_moves(self) -> list[tuple]:
        """Gets all the moves for black in the current position"""
        moves = []
        moves.extend(self._get_castle_moves_black())
        for idx, state in enumerate(self.state[:64]):
            if state < 7:
                continue
            if state == 7:
                moves.extend(self._get_black_pawn_moves(idx))
            elif state == 8:
                moves.extend(self._get_knight_moves_black(idx))
            elif state == 9:
                moves.extend(self._get_bishop_moves_black(idx))
            elif state == 10:
                moves.extend(self._get_rook_moves_black(idx))
            elif state == 11:
                moves.extend(self._get_queen_moves_black(idx))
            else:
                moves.extend(self._get_black_king_moves(idx))
        return moves

    def _filter_moves_double_check(self, moves: list[tuple], king_idx: int,
                                        threatening_player: bool) -> list[tuple]:
        """Removes all the illegal moves in moves for when active player is in double check"""
        legal_moves = []
        for move in moves:
            # King moves to an unthreatened square
            if move[0] == king_idx and\
                    not self._square_attacked_by_player(move[2], threatening_player):
                legal_moves.append(move)
        return legal_moves

    def _filter_moves_unblockable_check(self, moves: list[tuple], idx_attacking_king: list[int],
                                        king_idx: int, threatening_player: bool) -> list[tuple]:
        """Removes all the moves from moves that don't resolve an unblockable check"""
        # Legal moves only move the king to a non-threatened square or capture the piece
        legal_moves =[]
        for move in moves:
            # King moves to an unthreatened square
            if move[0] == king_idx:
                if self._square_attacked_by_player(move[2], threatening_player):
                    continue
                legal_moves.append(move)
            # Moves that capture the attacking piece
            elif move[2] == idx_attacking_king[0]:
                legal_moves.append(move)
        return legal_moves

    def _filter_moves_blockable_check(self, moves: list[tuple], idx_attacking_king: list[int],
                                      king_idx: int, threatening_player: bool) -> list[tuple]:
        """Removes all the moves from moves that don't resolve a blockable check"""
        legal_moves = []
        for move in moves:
            # King moves to an unthreatened square
            if move[0] == king_idx:
                if self._square_attacked_by_player(move[2], threatening_player):
                    continue
                legal_moves.append(move)

            # Moves that capture the attacking piece
            elif move[2] == idx_attacking_king[0]:
                legal_moves.append(move)

            # Moves that block the attacking piece
            elif move[2] in MOVES_TO_BLOCK_ATTACK_ON_FROM[king_idx][idx_attacking_king[0]]:
                legal_moves.append(move)
        return legal_moves

    def _filter_moves_in_check(self, moves: list[tuple], idx_attacking_king: list[int],
                               king_idx: int, threatening_player: bool) -> list[tuple]:
        """Removes all the illegal moves in moves for when the active player is in check"""
        # If the player is in double check
        if len(idx_attacking_king) >= 2:
            return self._filter_moves_double_check(moves, king_idx, threatening_player)

        # If the check is caused by an unblockable attack
        if idx_attacking_king[0] in UNBLOCKABLE_ATTACKS_AT[king_idx]:
            return self._filter_moves_unblockable_check(moves, idx_attacking_king,
                                                        king_idx, threatening_player)

        # Otherwise the check must be caused by a blockable attack
        return self._filter_moves_blockable_check(moves, idx_attacking_king,
                                                  king_idx, threatening_player)

    def _move_reveals_check(self, move: tuple, king_idx: int,
                            threats_in_direciton: dict, friendly_pieces: set) -> bool:
        """Determines if a move reveals a check"""
        unit_line_from_king_to_piece = VECTOR_TO_SQUARE_FROM[king_idx].get(move[0], None)

        # If there is no straight line from the move to the king no pin can exist
        if unit_line_from_king_to_piece is None:
            return False

        for square_idx in MOVES_FROM_SQUARE_ALONG_VECTOR[king_idx][unit_line_from_king_to_piece]:
            # Skip the square the origin piece is on
            if square_idx == move[0]:
                continue

            # If the piece is moving along that vector, it won't reveal a check
            if square_idx == move[2]:
                return False

            # If there is friendly piece on this vector, it won't reveal a check
            if self.state[square_idx] in friendly_pieces:
                return False

            # If there is an enemy that could cause a check on this vector
            if self.state[square_idx] in threats_in_direciton[unit_line_from_king_to_piece]:
                return True
        return False

    def _filter_illegal_moves(self, moves: list[tuple]) -> list[tuple]:
        """Returns a copy of moves but removing any move that causes check"""

        # There is a faster filter if the player is already in check
        king_idx = self.state[64 + self.state[-1]]
        idx_attacking_king = self.squares_attacking_king()
        if idx_attacking_king:
            return self._filter_moves_in_check(
                moves, idx_attacking_king, king_idx, not self.state[-1])

        legal_moves = []
        if self.state[-1]:
            threats_in_direciton = BLACK_THREATS_IN_DIRECTION
            friendly_pieces = WHITE_PIECES
        else:
            threats_in_direciton = WHITE_THREATS_IN_DIRECTION
            friendly_pieces = BLACK_PIECES

        for move in moves:
            # The king cannot step onto a threatened tile
            if move[0] == king_idx and\
                    self._square_attacked_by_player(move[2], not self.state[-1]):
                continue

            # A piece cannot reveal a check
            if self._move_reveals_check(move, king_idx, threats_in_direciton, friendly_pieces):
                continue

            legal_moves.append(move)
        return legal_moves

    def _udpate_moves_to_remove_castle(self, moves: list[tuple]):
        """Looks for moves that perform rook captures, removing appropriate castling rights"""
        if self.state[66] == 0:
            return moves

        new_moves = []
        for move in moves:
            if len(move) > 8 and move[10] in CASTLE_RIGHT_REMOVAL:
                new_moves.append(move[:5] + (move[5] & CASTLE_RIGHT_REMOVAL[move[10]],) + move[6:])
            elif len(move) > 4 and move[2] in CASTLE_RIGHT_REMOVAL:
                new_moves.append(move[:5] + (move[5] & CASTLE_RIGHT_REMOVAL[move[2]],) + move[6:])
            elif move[2] in CASTLE_RIGHT_REMOVAL:
                new_moves.append(move + (self.state[66],
                                         self.state[66] & CASTLE_RIGHT_REMOVAL[move[2]],
                                         self.state[67], -1))
            else:
                new_moves.append(move)
        return new_moves

    def get_all_moves(self) -> list[tuple]:
        """Gets all the moves for the given state of the board"""
        if self.state[-1]:
            moves = self.get_white_moves()
        else:
            moves = self.get_black_moves()
        return self._filter_illegal_moves(self._udpate_moves_to_remove_castle(moves))

    def sufficient_material(self) -> bool:
        """Checks if there is sufficient mating material"""
        # pylint: disable=too-many-return-statements
        material = defaultdict(int)
        for state in self.state[:64]:
            # If the piece on this tile by itself is sufficient material
            if state in SUFFICIENT_MATERIAL:
                return True
            material[state] += 1

            # If a player has two bishops
            if material[3] == 2 or material[9] == 2:
                return True

            # If a player has at least one bishop and at least one knight
            if (material[3] >= 1 and material[2] >= 1) or (material[9] >= 1 and material[8] >= 1):
                return True

            # If white has two knights and black has at least one knight or bishop
            if material[2] >= 2 and (material[8] >= 1 or material[9] >= 1):
                return True

            # If black has two knights and white has at least one knight or bishop
            if material[8] >= 2 and (material[2] >= 1 or material[3] >= 1):
                return True

            # If a player has more than two knights (strange promotion choices)
            if material[2] >= 3 or material[8] >= 3:
                return True

        return False
