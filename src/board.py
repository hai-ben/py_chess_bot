from copy import deepcopy
from src.chess_pieces import Pawn, Bishop, Knight, Rook, Queen, King

FILE_IDX = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
}
FILE_NAME = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
}
RANK_IDX = {
    "1": 7,
    "2": 6,
    "3": 5,
    "4": 4,
    "5": 3,
    "6": 2,
    "7": 1,
    "8": 0,
}
RANK_NAME = {
    0: "8",
    1: "7",
    2: "6",
    3: "5",
    4: "4",
    5: "3",
    6: "2",
    7: "1",
}
PIECE_NOTATION = {
    Pawn: "",
    Bishop: "B",
    Knight: "N",
    Rook: "R",
    Queen: "Q",
    King: "K"
}
PIECE_NAME = {
    "B": Bishop,
    "N": Knight,
    "R": Rook,
    "Q": Queen,
    "K": King,
}
PIECE_IDX = {
    Pawn: 0,
    Bishop: 1,
    Knight: 2,
    Rook: 3,
    Queen: 4,
    King: 5
}
PIECE_TYPE = {
    0: Pawn,
    1: Bishop,
    2: Knight,
    3: Rook,
    4: Queen,
    5: King,
}
ASCII_LOOKUP_WHITE = {
    0: "♙",
    1: "♗",
    2: "♘",
    3: "♖",
    4: "♕",
    5: "♔"
}
ASCII_LOOKUP_BLACK = {
    0: "♟︎",
    1: "♝",
    2: "♞",
    3: "♜",
    4: "♛",
    5: "♚"
}
LIGHT_TILE = "□"
DARK_TILE = "■"


class GameState:
    def __init__(self, notation: str="", wrcs: bool=True, wrcl: bool=True, brcs: bool=True, brcl: bool=True) -> None:
        self.current_state = ChessBoard()
        self.last_state = None
        self.player_turn = 1
        self.legal_moves = {}
        self.update_legal_moves()
        self.turn_number = 1
        self.notation_string = notation
        if notation:
            self.run_game()
        else:
            self.notation_string = f"{self.turn_number}. "
        self.wrcs = wrcs  # White right to castle short
        self.wrcl = wrcl  # White right to castle long
        self.brcs = brcs  # Black right to castle short
        self.brcl = brcl  # Black right to castle long
        self.en_passant_tile = []
    
    def run_game(self, notation_string):
        pass
    
    def update_legal_moves(self):
        pass

    def make_move(self, move) -> None:
        # Update the turn and notation
        self.player_turn = -self.player_turn
        if self.player_turn == 1:
            self.turn_number += 1
            self.notation_string += f"{self.turn_number}. "
        self.notation_string += f"{move} "

        # Update the state of the boards and legal moves
        self.last_turn = self.board
        self.board = self.legal_moves[move]
        self.legal_moves = {}
        self.update_legal_moves()

        # TODO: Add castle rights and en passant logic
    
    def re_ambiguate_moves(self, moveset: dict) -> dict:
        # TODO
        ambiguated_move_set_dict = {}

        temp_dict = {}
        for move in moveset.keys():
            if move[0].isupper():
               temp_dict[move[0]] = move

        return ambiguated_move_set_dict


class ChessBoard:
    def __init__(self, board=None) -> None:
        # 6 piece types, on an 8x8 board from white's perspective (black on top)
        # pawn, bishop, knight, rook, queen, king
        # 1 represents a white piece, -1 is black
        self.board = board or self.standard_setup()
        self.iter_counter = 0  # Used for iterating over every tile
    
    def __str__(self):
        out_str = ""
        for rank, row in enumerate(self.board):
            for file, tile in enumerate(row):
                new_tile = LIGHT_TILE if (rank + file) % 2 == 0 else DARK_TILE
                for piece_type, val in enumerate(tile):
                    if val != 0:
                        new_tile = ASCII_LOOKUP_BLACK[piece_type] if val == -1 else ASCII_LOOKUP_WHITE[piece_type]
                        break
                out_str += new_tile + " "
            out_str += "\n"
        return out_str[:-1]

    def __iter__(self):
        self.iter_counter = 0
        return self

    def __next__(self):
        if self.iter_counter < 8 * 8:
            rank = self.iter_counter // 8
            file = self.iter_counter % 8
            piece_id = next((index for index, value in enumerate(self.board[rank][file]) if value != 0), -1)
            self.iter_counter += 1
            return rank, file, piece_id, self.board[rank][file][piece_id]
        else:
            raise StopIteration
    
    def standard_setup(self) -> list:
        # Black is at the top
        standard_board = [[[0] * 6 for _i in range(8)] for _j in range(8)]
        
        # Pawns
        for i in range(8):
            standard_board[1][i][PIECE_IDX[Pawn]] = -1
            standard_board[-2][i][PIECE_IDX[Pawn]] = 1

        # Bishops
        standard_board[0][2][PIECE_IDX[Bishop]] = -1
        standard_board[0][-3][PIECE_IDX[Bishop]] = -1
        standard_board[-1][2][PIECE_IDX[Bishop]] = 1
        standard_board[-1][-3][PIECE_IDX[Bishop]] = 1

        # Knights
        standard_board[0][1][PIECE_IDX[Knight]] = -1
        standard_board[0][-2][PIECE_IDX[Knight]] = -1
        standard_board[-1][1][PIECE_IDX[Knight]] = 1
        standard_board[-1][-2][PIECE_IDX[Knight]] = 1

        # Rooks
        standard_board[0][0][PIECE_IDX[Rook]] = -1
        standard_board[0][-1][PIECE_IDX[Rook]] = -1
        standard_board[-1][0][PIECE_IDX[Rook]] = 1
        standard_board[-1][-1][PIECE_IDX[Rook]] = 1

        # Queens
        standard_board[0][3][PIECE_IDX[Queen]] = -1
        standard_board[-1][3][PIECE_IDX[Queen]] = 1

        # Kings
        standard_board[0][4][PIECE_IDX[King]] = -1
        standard_board[-1][4][PIECE_IDX[King]] = 1
        return standard_board

    def empty_board(self) -> None:
        self.board = [[[0] * 6 for _i in range(8)] for _j in range(8)]

    def add_piece(self, notation: str, piece: type, player: int):
        self.board[RANK_IDX[notation[1]]][FILE_IDX[notation[0]]][PIECE_IDX[piece]] = player

    def piece_on(self, board, rank, file) -> type:
        piece_id = next((index for index, value in enumerate(board[rank][file]) if value != 0), -1)
        return PIECE_TYPE.get(piece_id, None)

    def in_check(self, player: int) -> bool:
        # Check all pieces not controlled by the given player
        for rank, file, piece_id, controlled_by in self:
            # If this piece is not controlled by the opposite player (always continues when no player controls the tile)
            if controlled_by != -player:
                continue
            
            # Go through all of the attack vectors for that piece up to the piece's maximum range
            for vector in PIECE_TYPE[piece_id].ATTACK_VECTORS:
                for distance in range(1, PIECE_TYPE[piece_id].ATTACK_RANGE + 1):
                    row = rank + distance * (-controlled_by) * vector[1]  # Flip file movement based on player
                    col = file + distance * vector[0]
                    
                    # If the attack is off the board try the next vector
                    if row >= 8 or row < 0 or col >= 8 or col < 0:
                        break
                    
                    # If the attack targets a players king return True
                    if self.board[row][col][PIECE_IDX[King]] == player:
                        return True
                    
                    # If the attack runs into a piece try the next vector
                    if any(self.board[row][col]):
                        break
        return False

    def get_pawn_promotions(self, base_notation, current_board, rank, file, player):
        # Assumes the movement to the promotion square is legal and the pawn is already removed from current_board
        new_rank = rank - player
        promotion_moves = {}
        for i in range(4):
            new_state = deepcopy(current_board)
            new_state[new_rank][file] = [0] * 6  # Remove the defending piece from the future move if there is one
            new_state[new_rank][file][i + 1] = player  # [i+1] determines promotion type
            promotion_moves[base_notation + PIECE_NOTATION[PIECE_TYPE[i + 1]]] = ChessBoard(new_state)
        return promotion_moves

    def castle_legal(self, player: int, mode:str="short") -> bool:
        rank = 0 if player == -1 else 7
        empty_files = [1, 2, 3] if mode == "long" else [5, 6]

        # Check the rook exists
        if self.board[rank][0 if mode == "long" else 7][PIECE_IDX[Rook]] != player:
            return False

        # If there's a piece in the way the player can't castle
        if any([sum(self.board[rank][col]) != 0 for col in empty_files]):
            return False
        
        # Add kings to the empty files, if any are in check then the castle is illegal
        castle_check_board = ChessBoard(deepcopy(self.board))
        for file in empty_files:
            castle_check_board.board[rank][file][PIECE_IDX[King]] = player
        would_cause_check = castle_check_board.in_check(player)

        return not would_cause_check           
            
    def legal_moves(self, player: int, en_passant_tile: list=[], castle_rights: list=[]) -> dict:
        # For all pieces controlled by the given player
        all_moves = {}

        for rank, file, piece_id, controlled_by in self:
            if controlled_by != player:
                continue

            piece_type = PIECE_TYPE[piece_id]
            move_string = ""
    
            # Special rules for pawns: en passant, promotion, double moves
            if piece_type == Pawn:
                move_string += f"{FILE_NAME[file]}"
                new_rank = rank - player
                on_home_rank = (rank == 1) if (player == -1) else (rank == 6)
                promotes_on_next_rank = (new_rank == 0) or (new_rank == 7)
                
                # Make a copy of this board and then remove the pawn from it for ease in the future
                state_without_pawn = deepcopy(self.board)
                state_without_pawn[rank][file][PIECE_IDX[Pawn]] = 0

                # Check the pawn can attack something on the left
                if file > 0 and sum(self.board[new_rank][file - 1]) == -player:
                    take_string = f"{move_string}x{FILE_NAME[file - 1]}{RANK_NAME[new_rank]}"
                    if promotes_on_next_rank:
                        all_moves = all_moves | self.get_pawn_promotions(take_string, state_without_pawn, rank, file - 1)
                    else:
                        new_state = deepcopy(state_without_pawn)
                        new_state[new_rank][file - 1] = [1, 0, 0, 0, 0]
                        all_moves[take_string] = ChessBoard(new_state)
                
                # Check the pawn can attack something on the right
                if file < 7 and sum(self.board[new_rank][file + 1]) == -player:
                    take_string = f"{move_string}x{FILE_NAME[file + 1]}{RANK_NAME[new_rank]}"
                    if promotes_on_next_rank:
                        all_moves = all_moves | self.get_pawn_promotions(take_string, state_without_pawn, rank, file + 1)
                    else:
                        new_state = deepcopy(state_without_pawn)
                        new_state[new_rank][file + 1] = [player, 0, 0, 0, 0, 0]
                        all_moves[take_string] = ChessBoard(new_state)

                # If the square in front is empty
                if sum(self.board[new_rank][file]) == 0:
                    if promotes_on_next_rank:
                        all_moves = all_moves | self.get_pawn_promotions(move_string + RANK_NAME[new_rank], state_without_pawn, rank, file)
                    else:
                        new_state = deepcopy(state_without_pawn)
                        new_state[new_rank][file] = [1, 0, 0, 0, 0, 0]
                        all_moves[move_string + RANK_NAME[new_rank]] = ChessBoard(new_state)

                        # Check for double Moves
                        if on_home_rank and sum(self.board[new_rank - player][file]) == 0:
                            new_state = deepcopy(state_without_pawn)
                            new_state[new_rank - player][file] = [1, 0, 0, 0, 0, 0]
                            all_moves[move_string + RANK_NAME[new_rank - player]] = ChessBoard(new_state)

                # If en_passant is an option
                if en_passant_tile and rank == en_passant_tile[0]:
                    if file == en_passant_tile[1] + 1:
                        take_string = f"{move_string}x{FILE_NAME[file + 1]}{RANK_NAME[new_rank]}"
                        new_state = deepcopy(state_without_pawn)
                        new_state[new_rank][file + 1] = [1, 0, 0, 0, 0, 0]
                        all_moves[take_string] = ChessBoard(new_state)
                    elif file == en_passant_tile[1] - 1:
                        take_string = f"{move_string}x{FILE_NAME[file - 1]}{RANK_NAME[new_rank]}"
                        new_state = deepcopy(state_without_pawn)
                        new_state[new_rank][file - 1] = [1, 0, 0, 0, 0, 0]
                        all_moves[take_string] = ChessBoard(new_state)
                continue  # Don't execute the general attack logic for pawns
            
            # Castling
            if castle_rights and piece_type == King:
                castle_rank = 7 if player == 1 else 0
                if "short" in castle_rights and self.check_castle_legal(player, "short"):
                    new_state = deepcopy(self.board)
                    new_state[castle_rank][4][PIECE_IDX[King]] = 0
                    new_state[castle_rank][6][PIECE_IDX[King]] = player
                    new_state[castle_rank][5][PIECE_IDX[Rook]] = player
                    new_state[castle_rank][7][PIECE_IDX[Rook]] = 0
                    all_moves["O-O"] = ChessBoard(new_state)
                if "long" in castle_rights and self.check_castle_legal(player, "long"):
                    new_state = deepcopy(self.board)
                    new_state[castle_rank][4][PIECE_IDX[King]] = 0
                    new_state[castle_rank][2][PIECE_IDX[King]] = player
                    new_state[castle_rank][3][PIECE_IDX[Rook]] = player
                    new_state[castle_rank][0][PIECE_IDX[Rook]] = 0
                    all_moves["O-O-O"] = ChessBoard(new_state)

            # Check the attack vectors of the given piece
            for vector in piece_type.ATTACK_VECTORS:
                new_state_wo_piece = deepcopy(self.board)
                new_state_wo_piece[rank][file][piece_id] = 0
                move_from = f"{PIECE_NOTATION[piece_type]}{FILE_NAME[file]}{RANK_NAME[rank]}"
                for distance in range(1, piece_type.ATTACK_RANGE + 1):
                    row = rank + distance * vector[1]
                    col = file + distance * vector[0]

                    # If the attack is off the board try the next vector
                    if row >= 8 or row < 0 or col >= 8 or col < 0:
                        break
                    
                    # If the attack runs into a friendly piece try the next vector
                    if sum(self.board[row][col]) == player:
                        break

                    # Make the move
                    take_string = move_from
                    new_state = deepcopy(new_state_wo_piece)

                    # If it's a capture break
                    if sum(new_state[row][col]) == -player:
                        new_state[row][col] = [0] * 6  # Remove all pieces from the landed position
                        new_state[row][col][piece_id] = player
                        all_moves[take_string + "x" + FILE_NAME[col] + RANK_NAME[row]] = ChessBoard(new_state)
                        break

                    new_state[row][col][piece_id] = player
                    all_moves[take_string + FILE_NAME[col] + RANK_NAME[row]] = ChessBoard(new_state)
        
        legal_moves = [move for move, board in all_moves.items() if not board.in_check(player)]
        return {move: all_moves[move] for move in legal_moves}
