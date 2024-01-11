import pytest
from copy import deepcopy
from src.chess_pieces import Pawn, Bishop, Knight, Rook, Queen, King
from src.board import ChessBoard
from resources import BASE_STATE, OPENING_MOVES_WHITE, OPENING_MOVES_BLACK, ITER_BASE_STATE, START_STATE

@pytest.fixture
def base_board():
    return ChessBoard()


@pytest.fixture
def blank_state(base_board):
    base_board.empty_board()
    return base_board


def test_starting_state(base_board):
    assert base_board.board == BASE_STATE


def test_iter(base_board):
    for a, b in zip(ITER_BASE_STATE, base_board):
        assert a == b


def test_blank_state(blank_state):
    for rank in blank_state.board:
        for tile in rank:
            assert not any(tile)


def test_add_piece(blank_state):
    blank_state.add_piece("b2", Pawn, -1)
    for rank, row in enumerate(blank_state.board):
        for file, tile in enumerate(row):
            if rank == 6 and file == 1:
                assert tile == [-1, 0, 0, 0, 0, 0]
            else:
                assert not any(tile)


def test_opening_moves(base_board):
    legal_moves_white = base_board.legal_moves(1).keys()
    for move in OPENING_MOVES_WHITE:
        assert move in legal_moves_white
    
    legal_moves_black = base_board.legal_moves(-1).keys()
    for move in OPENING_MOVES_BLACK:
        assert move in legal_moves_black


def test_print(base_board):
    assert str(base_board) == START_STATE

class TestRook:
    EXPECTED_MOVES = set([
        'Rc4a4', 'Rc4b4', 'Rc4d4', 'Rc4e4','Rc4f4', 'Rc4g4', 'Rc4h4',
        'Rc4c1', 'Rc4c2', 'Rc4c3', 'Rc4c5', 'Rc4c6', 'Rc4c7', 'Rc4c8'
    ])
    
    @pytest.fixture(autouse=True)
    def _make_rook(self, blank_state):
        self.c4_rook = blank_state
        self.c4_rook.board[4][2][3] = 1

    def test_empty_moves(self):
        legal_moves = self.c4_rook.legal_moves(1).keys()
        for move in self.EXPECTED_MOVES:
            assert move in legal_moves
    
    def test_blocked_moves_friendly(self):
        self.c4_rook.add_piece("d4", Pawn, 1)
        legal_moves = self.c4_rook.legal_moves(1).keys()
        lost_moves = set(['Rc4d4', 'Rc4e4','Rc4f4', 'Rc4g4', 'Rc4h4'])
        for move in self.EXPECTED_MOVES.difference(lost_moves):
            assert move in legal_moves
        for move in lost_moves:
            assert move not in legal_moves

    def test_blocked_moves_enemy(self):
        self.c4_rook.add_piece("d4", Pawn, -1)
        legal_moves = self.c4_rook.legal_moves(1).keys()
        lost_moves = set(['Rc4d4', 'Rc4e4','Rc4f4', 'Rc4g4', 'Rc4h4'])
        for move in self.EXPECTED_MOVES.difference(lost_moves):
            assert move in legal_moves
        for move in lost_moves:
            assert move not in legal_moves

    def test_checks(self):
        self.c4_rook.add_piece("d4", King, -1)
        assert self.c4_rook.in_check(-1)
        assert not self.c4_rook.in_check(1)

    def test_pin_and_capture(self):
        self.c4_rook.add_piece("d4", King, 1)
        self.c4_rook.add_piece("b4", Rook, -1)
        legal_moves = self.c4_rook.legal_moves(1).keys()
        for move in legal_moves:
            if "R" in move:
                assert move == "Rc4xb4"