from copy import deepcopy
from chess_pieces import Pawn, Bishop, Knight, Rook, Queen, King

# TODO: Algebriac notation in/out

class ChessBoard:
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

    def __init__(self, player_turn=1, last_turn=None, board=None, wrcs=True, wrcl=True, brcs=True, brcl=True) -> None:
        # 6 piece types, on an 8x8 board from white's perspective (black on top)
        # pawn, bishop, knight, rook, queen, king
        # 1 represents a white piece, -1 is black
        self.player_turn = player_turn
        self.board = board or [[[0] * 6 for _i in range(8)] for _j in range(8)]
        self.last_turn = last_turn or deepcopy(self.board)
        self.wrcs = wrcs  # White right to castle short
        self.wrcl = wrcl  # White right to castle long
        self.brcs = brcs  # Black right to castle short
        self.brcl = brcl  # Black right to castle long
        self.iter_counter = 0
    
    def standard_setup(self) -> None:
        # Pawns, black is at the top
        self.board = [[[0] * 6 for _i in range(8)] for _j in range(8)]

        for i in range(8):
            self.board[1][i][self.PIECE_IDX[Pawn]] = -1
            self.board[-2][i][self.PIECE_IDX[Pawn]] = 1

        # Bishops
        self.board[0][2][self.PIECE_IDX[Bishop]] = -1
        self.board[0][-3][self.PIECE_IDX[Bishop]] = -1
        self.board[-1][2][self.PIECE_IDX[Bishop]] = 1
        self.board[-1][-3][self.PIECE_IDX[Bishop]] = 1

        # Knights
        self.board[0][1][self.PIECE_IDX[Knight]] = -1
        self.board[0][-2][self.PIECE_IDX[Knight]] = -1
        self.board[-1][1][self.PIECE_IDX[Knight]] = 1
        self.board[-1][-2][self.PIECE_IDX[Knight]] = 1

        # Rooks
        self.board[0][0][self.PIECE_IDX[Rook]] = -1
        self.board[0][-1][self.PIECE_IDX[Rook]] = -1
        self.board[-1][0][self.PIECE_IDX[Rook]] = 1
        self.board[-1][-1][self.PIECE_IDX[Rook]] = 1

        # Queens
        self.board[0][3][self.PIECE_IDX[Queen]] = -1
        self.board[-1][3][self.PIECE_IDX[Queen]] = 1

        # Kings
        self.board[0][4][self.PIECE_IDX[King]] = -1
        self.board[-1][4][self.PIECE_IDX[King]] = 1
    
    def __str__(self):
        out_str = ""
        for rank, row in enumerate(self.board):
            for file, tile in enumerate(row):
                new_tile = self.LIGHT_TILE if (rank + file) % 2 == 0 else self.DARK_TILE
                for piece_type, val in enumerate(tile):
                    if val != 0:
                        new_tile = self.ASCII_LOOKUP_BLACK[piece_type] if val == -1 else self.ASCII_LOOKUP_WHITE[piece_type]
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

    def __getitem__(self, item):
        return self.board[item]

    def next_turn_with(self, new_board, previous_board=None):
        return ChessBoard(-self.player_turn,
                          previous_board or deepcopy(self.board),
                          deepcopy(new_board),
                          self.wrcs,
                          self.wrcl,
                          self.brcs,
                          self.brcl)

    def in_check(self, player: int) -> bool:
        if player != 1 and player != -1:
            raise ValueError("please specify a player!")

        # Check all pieces not controlled by the given player
        for rank, file, piece_id, controlled_by in self:
            # If this piece is not controlled by the opposite player (always continues when no player controls the tile)
            if controlled_by != -player:
                continue
            
            # Go through all of the attack vectors for that piece up to the piece's maximum range
            for vector in self.PIECE_TYPE[piece_id].ATTACK_VECTORS:
                for distance in range(1, self.PIECE_TYPE[piece_id].ATTACK_RANGE + 1):
                    row = rank + distance * (-controlled_by) * vector[1]  # Flip file movement based on player
                    col = file + distance * vector[0]
                    
                    # If the attack is off the board try the next vector
                    if row >= 8 or row < 0 or col >= 8 or col < 0:
                        break
                    
                    # If the attack targets a players king return True
                    if self.board[row][col][self.PIECE_IDX[King]] == player:
                        return True
                    
                    # If the attack runs into a piece try the next vector
                    if any(self.board[row][col]):
                        break
        
        return False

    def pawn_promotions(self, previous_board, rank, file, player):
        # Assumes the promotion square is either attackable or move-to-able on the file
        promotions = []
        for i in range(4):
            promotions.append(self.next_turn_with(self.board, previous_board))
            promotions[-1][rank - player][file] = [0] * 6  # Remove the defending piece from the future move
            promotions[-1][rank - player][file][i + 1] = player  # [i+1] determines promotion type
        return promotions

    def advance_pawn(self, previous_board, rank, file, player):
        board = self.next_turn_with(self.board, previous_board)
        board[rank - player][file] = [0] * 6  # Remove the defending piece from the future move
        board[rank - player][file][self.PIECE_IDX[Pawn]] = player
        return board

    def check_castle_legal(self, player, mode="short") -> bool:
        rank = 0 if player == -1 else 7
        empty_files = [1, 2, 3] if mode == "long" else [5, 6]

        # Check the rook exists
        if self.board[rank][0 if mode == "long" else 7][self.PIECE_IDX[Rook]] != player:
            return False

        # If there's a piece in the way the player can't castle
        if any([sum(self.board[rank][col]) != 0 for col in empty_files]):
            return False
        
        # If the player would be in check if they move their king along those spaces
        old_board = deepcopy(self.board)

        # Add kings to the empty files, if any are in check then the castle is illegal
        for file in empty_files:
            self.board[rank][file][self.PIECE_IDX[King]] = player
        would_cause_check = self.in_check(player)

        # Put the board back
        self.board = old_board
        return not would_cause_check

    def legal_moves(self, player: int):
        if player != 1 and player != -1:
            raise ValueError("please specify a turn!")
        
        future_moves = []

        # For all pieces controlled by the given player
        for rank, file, piece_id, controlled_by in self:
            # TODO: Change castling rights if king or rook moved

            if controlled_by != player:
                continue
            
            piece_type = self.PIECE_TYPE[piece_id]
    
            # Special rules for pawns: en passant, promotion, double moves
            if piece_type == Pawn:
                on_home_rank = (rank == 1) if (player == -1) else (rank == 6)
                promotes_on_next_rank = (rank - player == 0) or (rank - player == 7)

                # Make a copy of this board and then remove the pawn from it for ease
                this_turn = deepcopy(self.board)
                self.board[rank][file][self.PIECE_IDX[Pawn]] = 0

                # Check left attack
                if file > 0:
                    # If the left attack square is controlled by the opposite player
                    if sum(self.board[rank - player][file - 1]) == -player:
                        if promotes_on_next_rank:
                            future_moves.extend(self.pawn_promotions(this_turn, rank, file - 1, player))
                        else:
                            future_moves.append(self.advance_pawn(this_turn, rank, file - 1, player))
                
                # Check right attack
                if file < 7:
                    # If the right attack square is controlled by the opposite player
                    if sum(self.board[rank - player][file + 1]) == -player:
                        if promotes_on_next_rank:
                            future_moves.extend(self.pawn_promotions(this_turn, rank, file + 1, player))
                        else:
                            future_moves.append(self.advance_pawn(this_turn, rank, file + 1, player))

                # Check forward moves, if the square in front is empty
                if sum(self.board[rank - player][file]) == 0:
                    if promotes_on_next_rank:
                        future_moves.extend(self.pawn_promotions(this_turn, rank, file, player))
                    else:
                        future_moves.append(self.advance_pawn(this_turn, rank, file, player))
                        # Check for double Moves
                        if on_home_rank and sum(self.board[rank - (2 * player)][file]) == 0:
                            future_moves.append(self.advance_pawn(this_turn, rank - player, file, player))

                on_en_passant_rank = (rank == 4) if (player == -1) else (rank == 3)
                if on_en_passant_rank:
                    # Check left that there is a pawn beside
                    if file > 0 and self.board[rank][file - 1][self.PIECE_IDX[Pawn]] == -player:
                        piece_behind_pawn = sum(self.board[rank][file - 1]) == 0
                        was_on_home_rank = self.last_turn[rank + 2 * player][file - 1][self.PIECE_IDX[Pawn]] == -player
                        home_rank_empty = sum(self.board[rank + 2 * player][file - 1]) == 0
                        if not piece_behind_pawn and was_on_home_rank and home_rank_empty:
                            future_moves.append(self.advance_pawn(this_turn, rank, file - 1, player))
                            future_moves[-1][rank][file - 1] = [0] * 6
                    # Check right that there is a pawn beside
                    if file < 7 and self.board[rank][file + 1][self.PIECE_IDX[Pawn]] == -player:
                        piece_behind_pawn = sum(self.board[rank][file + 1]) == 0
                        was_on_home_rank = self.last_turn[rank + 2 * player][file + 1][self.PIECE_IDX[Pawn]] == -player
                        home_rank_empty = sum(self.board[rank + 2 * player][file + 1]) == 0
                        if not piece_behind_pawn and was_on_home_rank and home_rank_empty:
                            future_moves.append(self.advance_pawn(this_turn, rank, file + 1, player))
                            future_moves[-1][rank][file + 1] = [0] * 6

                # Put the pawn back after removing it
                self.board[rank][file][self.PIECE_IDX[Pawn]] = player
                continue  # Don't execute the general attack logic for pawns
            
            # Do castling
            if piece_type == King:
                # White short castling
                if player == 1:
                    if self.wrcs and self.check_castle_legal(player, "short"):
                        future_moves.append(self.next_turn_with(self.board))
                        future_moves[-1][7][4][self.PIECE_IDX[King]] = 0
                        future_moves[-1][7][6][self.PIECE_IDX[King]] = 1
                        future_moves[-1][7][5][self.PIECE_IDX[Rook]] = 1
                        future_moves[-1][7][7][self.PIECE_IDX[Rook]] = 0
                        future_moves[-1].wrcs = False
                        future_moves[-1].wrcl = False
                    # White long castling
                    if self.wrcl and self.check_castle_legal(player, "long"):
                        future_moves.append(self.next_turn_with(self.board))
                        future_moves[-1][7][4][self.PIECE_IDX[King]] = 0
                        future_moves[-1][7][2][self.PIECE_IDX[King]] = 1
                        future_moves[-1][7][3][self.PIECE_IDX[Rook]] = 1
                        future_moves[-1][7][0][self.PIECE_IDX[Rook]] = 0
                        future_moves[-1].wrcs = False
                        future_moves[-1].wrcl = False
                
                else:
                    # Black short castling
                    if self.brcs and self.check_castle_legal(player, "short"):
                        future_moves.append(self.next_turn_with(self.board))
                        future_moves[-1][0][4][self.PIECE_IDX[King]] = 0
                        future_moves[-1][0][6][self.PIECE_IDX[King]] = -1
                        future_moves[-1][0][5][self.PIECE_IDX[Rook]] = -1
                        future_moves[-1][0][7][self.PIECE_IDX[Rook]] = 0
                        future_moves[-1].brcs = False
                        future_moves[-1].brcl = False
                    # Black long castling
                    if self.brcl and self.check_castle_legal(player, "long"):
                        future_moves.append(self.next_turn_with(self.board))
                        future_moves[-1][0][4][self.PIECE_IDX[King]] = 0
                        future_moves[-1][0][2][self.PIECE_IDX[King]] = -1
                        future_moves[-1][0][3][self.PIECE_IDX[Rook]] = -1
                        future_moves[-1][0][0][self.PIECE_IDX[Rook]] = 0
                        future_moves[-1].brcs = False
                        future_moves[-1].brcl = False

            # Check the attack vectors of the given piece
            for vector in piece_type.ATTACK_VECTORS:
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
                    new_board = self.next_turn_with(self.board)
                    new_board[rank][file][piece_id] = 0  # Remove the piece from the old position
                    new_board[row][col] = [0] * 6  # Remove all pieces from the landed position
                    new_board[row][col][piece_id] = player

                    # Update the castling rights, any king move revokes all
                    if piece_type is King:
                        if player == 1:
                            new_board.wrcs = False
                            new_board.wrcl = False
                        else:
                            new_board.brcs = False
                            new_board.brcl = False
                    # Otherwise a rook move will revoke on that side
                    elif piece_type is Rook and (self.wrcs or self.wrcl) if player == 1 else (self.brcs or self.brcl):
                        if player == 1:
                            if file == 7:
                                new_board.wrcs = False
                            if file == 0:
                                new_board.wrcl = False
                        else:
                            if file == 7:
                                new_board.brcs = False
                            if file == 0:
                                new_board.brcl = False
                    future_moves.append(new_board)
        # Remove all moves that would put the player in check
        return [move for move in future_moves if not move.in_check(player)]
    
