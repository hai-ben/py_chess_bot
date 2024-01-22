"""Tests that the instruction sets for each piece are generated correctly"""
import pytest
from src.resources.data_translators import SQUARE_IDX, B_KING_IDX, W_KING_IDX, CASTLE_IDX, EP_IDX,\
    TURN_IDX, SQUARE_STATES, CASTLE_STATES, EP_FILE

MOVE_TEST_DICT = {
    "WHITE_KING_EMPTY": (
        [("e3", "w_king"), (W_KING_IDX, "e3"), (EP_IDX, "b")],
        [["e3"] * 8,
         ["w_king"] * 8,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2", "f4"],
         ["empty"] * 8,
         [0b1111] * 8,
         [0b1100] * 8,
         [EP_FILE["b"]] * 8,
         [-1] * 8],
        ("get_king_moves", [])
    ),
    "WHITE_KING_ENEMY_TAKE": (
        [("e3", "w_king"), (W_KING_IDX, "e3"), (EP_IDX, "b"), ("e2", "b_pawn")],
        [["e3"] * 8,
         ["w_king"] * 8,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2", "f4"],
         ["b_pawn"] + ["empty"] * 7,
         [0b1111] * 8,
         [0b1100] * 8,
         [EP_FILE["b"]] * 8,
         [-1] * 8],
        ("get_king_moves", [])
    ),
    "WHITE_KING_FRIENDLY_TAKE": (
        [("e3", "w_king"), (W_KING_IDX, "e3"), (EP_IDX, "b"), ("f4", "w_pawn")],
        [["e3"] * 7,
         ["w_king"] * 7,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2"],
         ["empty"] * 7,
         [0b1111] * 7,
         [0b1100] * 7,
         [EP_FILE["b"]] * 7,
         [-1] * 7],
        ("get_king_moves", [])
    ),
    "BLACK_KING_EMPTY": (
        [(TURN_IDX, False), ("e3", "b_king"), (B_KING_IDX, "e3"), (EP_IDX, "c")],
        [["e3"] * 8,
         ["b_king"] * 8,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2", "f4"],
         ["empty"] * 8,
         [0b1111] * 8,
         [0b0011] * 8,
         [EP_FILE["c"]] * 8,
         [-1] * 8],
        ("get_king_moves", [])
    ),
    "BLACK_KING_ENEMY_TAKE": (
        [(TURN_IDX, False), ("e3", "b_king"), (B_KING_IDX, "e3"), (EP_IDX, "d"), ("e2", "w_pawn")],
        [["e3"] * 8,
         ["b_king"] * 8,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2", "f4"],
         ["w_pawn"] + ["empty"] * 7,
         [0b1111] * 8,
         [0b0011] * 8,
         [EP_FILE["d"]] * 8,
         [-1] * 8],
        ("get_king_moves", [])
    ),
    "BLACK_KING_ALLY_TAKE": (
        [(TURN_IDX, False), ("e3", "b_king"), (B_KING_IDX, "e3"), (EP_IDX, "e"), ("f4", "b_pawn")],
        [["e3"] * 7,
         ["b_king"] * 7,
         ["e2", "e4", "d3", "d2", "d4", "f3", "f2"],
         ["empty"] * 7,
         [0b1111] * 7,
         [0b0011] * 7,
         [EP_FILE["e"]] * 7,
         [-1] * 7],
        ("get_king_moves", [])
    ),
    "WHITE_KNIGHT_EMPTY": (
        [("c5", "w_knight")],
        [["c5"] * 8,
         ["w_knight"] * 8,
         ["b7", "d7", "b3", "d3", "a4", "e4", "e6", "a6"],
         ["empty"] * 8],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "WHITE_KNIGHT_ENEMY_TAKE": (
        [("c5", "w_knight"), ("a6", "b_queen")],
        [["c5"] * 8,
         ["w_knight"] * 8,
         ["b7", "d7", "b3", "d3", "a4", "e4", "e6", "a6"],
         ["empty"] * 7 + ["b_queen"]],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "WHITE_KNIGHT_ALLY_TAKE": (
        [("c5", "w_knight"), ("d3", "w_rook")],
        [["c5"] * 7,
         ["w_knight"] * 7,
         ["b7", "d7", "b3", "a4", "e4", "e6", "a6"],
         ["empty"] * 7],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "WHITE_KNIGHT_UNSET_EP": (
        [("c5", "w_knight"), (EP_IDX, EP_FILE["e"]), ("d3", "w_rook"), ("a6", "b_queen")],
        [["c5"] * 7,
         ["w_knight"] * 7,
         ["b7", "d7", "b3", "a4", "e4", "e6", "a6"],
         ["empty"] * 6 + ["b_queen"],
         [0b1111] * 7,
         [0b1111] * 7,
         [EP_FILE["e"]] * 7,
         [-1] * 7],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "BLACK_KNIGHT_EMPTY": (
        [("c5", "b_knight"), (TURN_IDX, False)],
        [["c5"] * 8,
         ["b_knight"] * 8,
         ["b7", "d7", "b3", "d3", "a4", "e4", "e6", "a6"],
         ["empty"] * 8],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "BLACK_KNIGHT_ENEMY_TAKE": (
        [("c5", "b_knight"), ("a6", "w_queen"), (TURN_IDX, False)],
        [["c5"] * 8,
         ["b_knight"] * 8,
         ["b7", "d7", "b3", "d3", "a4", "e4", "e6", "a6"],
         ["empty"] * 7 + ["w_queen"]],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "BLACK_KNIGHT_ALLY_TAKE": (
        [("c5", "b_knight"), ("d3", "b_rook"), (TURN_IDX, False)],
        [["c5"] * 7,
         ["b_knight"] * 7,
         ["b7", "d7", "b3", "a4", "e4", "e6", "a6"],
         ["empty"] * 7],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "BLACK_KNIGHT_UNSET_EP": (
        [("c5", "b_knight"), (EP_IDX, EP_FILE["f"]), (TURN_IDX, False),
         ("a6", "w_queen"), ("d3", "b_rook")],
        [["c5"] * 7,
         ["b_knight"] * 7,
         ["b7", "d7", "b3", "a4", "e4", "e6", "a6"],
         ["empty"] * 6 + ["w_queen"],
         [0b1111] * 7,
         [0b1111] * 7,
         [EP_FILE["f"]] * 7,
         [-1] * 7],
        ("get_knight_moves", [SQUARE_IDX["c5"]])
    ),
    "WHITE_BISHOP_EMPTY": (
        [("f5", "w_bishop")],
        [["f5"] * 11,
         ["w_bishop"] * 11,
         ["g6", "h7", "e4", "d3", "c2", "b1", "g4", "h3", "e6", "d7", "c8"],
         ["empty"] * 11],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "WHITE_BISHOP_ENEMY_TAKE": (
        [("f5", "w_bishop"), ("d7", "b_queen")],
        [["f5"] * 10,
         ["w_bishop"] * 10,
         ["g6", "h7", "e4", "d3", "c2", "b1", "g4", "h3", "e6", "d7"],
         ["empty"] * 9 + ["b_queen"]],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "WHITE_BISHOP_ALLY_TAKE": (
        [("f5", "w_bishop"), ("e4", "w_rook")],
        [["f5"] * 7,
         ["w_bishop"] * 7,
         ["g6", "h7", "g4", "h3", "e6", "d7", "c8"],
         ["empty"] * 7],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "WHITE_BISHOP_UNSET_EP": (
        [("f5", "w_bishop"), (EP_IDX, EP_FILE["a"]), ("e4", "w_rook"), ("d7", "b_queen")],
        [["f5"] * 6,
         ["w_bishop"] * 6,
         ["g6", "h7", "g4", "h3", "e6", "d7"],
         ["empty"] * 5 + ["b_queen"],
         [0b1111] * 6,
         [0b1111] * 6,
         [EP_FILE["a"]] * 6,
         [-1] * 6],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "BLACK_BISHOP_EMPTY": (
        [("f5", "b_bishop"), (TURN_IDX, False)],
        [["f5"] * 11,
         ["b_bishop"] * 11,
         ["g6", "h7", "e4", "d3", "c2", "b1", "g4", "h3", "e6", "d7", "c8"],
         ["empty"] * 11],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "BLACK_BISHOP_ENEMY_TAKE": (
        [("f5", "b_bishop"), ("d7", "w_queen"), (TURN_IDX, False)],
        [["f5"] * 10,
         ["b_bishop"] * 10,
         ["g6", "h7", "e4", "d3", "c2", "b1", "g4", "h3", "e6", "d7"],
         ["empty"] * 9 + ["w_queen"]],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "BLACK_BISHOP_ALLY_TAKE": (
        [("f5", "b_bishop"), ("e4", "b_rook"), (TURN_IDX, False)],
        [["f5"] * 7,
         ["b_bishop"] * 7,
         ["g6", "h7", "g4", "h3", "e6", "d7", "c8"],
         ["empty"] * 7],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "BLACK_BISHOP_UNSET_EP": (
        [("f5", "b_bishop"), (EP_IDX, EP_FILE["a"]), (TURN_IDX, False),
         ("e4", "b_rook"), ("d7", "w_queen")],
        [["f5"] * 6,
         ["b_bishop"] * 6,
         ["g6", "h7", "g4", "h3", "e6", "d7"],
         ["empty"] * 5 + ["w_queen"],
         [0b1111] * 6,
         [0b1111] * 6,
         [EP_FILE["a"]] * 6,
         [-1] * 6],
        ("get_bishop_moves", [SQUARE_IDX["f5"]])
    ),
    "WHITE_ROOK_BASICS": (
        [("e4", "w_rook"), ("e6", "b_knight"), ("b4", "w_pawn")],
        [["e4"] * 10,
         ["w_rook"] * 10,
         ["e6", "e5", "e3", "e2", "e1", "d4", "c4", "f4", "g4", "h4"],
         ["b_knight"] + ["empty"] * 9],
        ("get_rook_moves", [SQUARE_IDX["e4"]])
    ),
    "WHITE_ROOK_EP": (
        [("e4", "w_rook"), ("e6", "b_knight"), ("b4", "w_pawn"), (EP_IDX, EP_FILE["b"])],
        [["e4"] * 10,
         ["w_rook"] * 10,
         ["e6", "e5", "e3", "e2", "e1", "d4", "c4", "f4", "g4", "h4"],
         ["b_knight"] + ["empty"] * 9,
         [0b1111] * 10,
         [0b1111] * 10,
         [EP_FILE["b"]] * 10,
         [-1] * 10],
        ("get_rook_moves", [SQUARE_IDX["e4"]])
    ),
    "WHITE_ROOK_CASTLE_DISABLE_SHORT": (
        [("h1", "w_rook"), ("f1", "b_bishop"), ("h5", "w_pawn"), (EP_IDX, EP_FILE["d"])],
        [["h1"] * 5,
         ["w_rook"] * 5,
         ["f1", "g1", "h2", "h3", "h4"],
         ["b_bishop"] + ["empty"] * 4,
         [0b1111] * 5,
         [0b1111 - CASTLE_STATES["w_short"]] * 5,
         [EP_FILE["d"]] * 5,
         [-1] * 5],
        ("get_rook_moves", [SQUARE_IDX["h1"]])
    ),
    "WHITE_ROOK_CASTLE_DISABLE_LONG": (
        [("a1", "w_rook"), ("f1", "b_queen"), ("a6", "w_pawn"), (EP_IDX, EP_FILE["g"])],
        [["a1"] * 9,
         ["w_rook"] * 9,
         ["f1", "e1", "d1", "c1", "b1", "a2", "a3", "a4", "a5"],
         ["b_queen"] + ["empty"] * 8,
         [0b1111] * 9,
         [0b1111 - CASTLE_STATES["w_long"]] * 9,
         [EP_FILE["g"]] * 9,
         [-1] * 9],
        ("get_rook_moves", [SQUARE_IDX["a1"]])
    ),
    "BLACK_ROOK_BASICS": (
        [("e4", "b_rook"), ("e6", "w_knight"), ("b4", "b_pawn"), (TURN_IDX, False)],
        [["e4"] * 10,
         ["b_rook"] * 10,
         ["e6", "e5", "e3", "e2", "e1", "d4", "c4", "f4", "g4", "h4"],
         ["w_knight"] + ["empty"] * 9],
        ("get_rook_moves", [SQUARE_IDX["e4"]])
    ),
    "BLACK_ROOK_EP": (
        [("e4", "b_rook"), ("e6", "w_knight"), ("b4", "b_pawn"),
         (EP_IDX, EP_FILE["c"]), (TURN_IDX, False)],
        [["e4"] * 10,
         ["b_rook"] * 10,
         ["e6", "e5", "e3", "e2", "e1", "d4", "c4", "f4", "g4", "h4"],
         ["w_knight"] + ["empty"] * 9,
         [0b1111] * 10,
         [0b1111] * 10 ,
         [EP_FILE["c"]] * 10,
         [-1] * 10],
        ("get_rook_moves", [SQUARE_IDX["e4"]])
    ),
    "BLACK_ROOK_CASTLE_DISABLE_SHORT": (
        [("h8", "b_rook"), ("f8", "w_bishop"), ("h4", "b_pawn"),
         (EP_IDX, EP_FILE["d"]), (TURN_IDX, False)],
        [["h8"] * 5,
         ["b_rook"] * 5,
         ["f8", "g8", "h7", "h6", "h5"],
         ["w_bishop"] + ["empty"] * 4,
         [0b1111] * 5,
         [0b1111 - CASTLE_STATES["b_short"]] * 5,
         [EP_FILE["d"]] * 5,
         [-1] * 5],
        ("get_rook_moves", [SQUARE_IDX["h8"]])
    ),
    "BLACK_ROOK_CASTLE_DISABLE_LONG": (
        [("a8", "b_rook"), ("f8", "w_queen"), ("a6", "b_pawn"),
         (EP_IDX, EP_FILE["g"]), (TURN_IDX, False)],
        [["a8"] * 6,
         ["b_rook"] * 6,
         ["f8", "e8", "d8", "c8", "b8", "a7"],
         ["w_queen"] + ["empty"] * 5,
         [0b1111] * 6,
         [0b1111 - CASTLE_STATES["b_long"]] * 6,
         [EP_FILE["g"]] * 6,
         [-1] * 6],
        ("get_rook_moves", [SQUARE_IDX["a8"]])
    ),
    "WHITE_QUEEN_BASIC": (
        [("d5", "w_queen"), ("d3", "b_rook"), ("f7", "w_king")],
        [["d5"] * 23,
         ["w_queen"] * 23,
         ["d3", "d4", "d6", "d7", "d8", "a5", "b5", "c5", "e5", "f5", "g5", "h5",
          "a8", "b7", "c6", "e4", "f3", "g2", "h1", "a2", "b3", "c4", "e6"],
         ["b_rook"] + ["empty"] * 22],
        ("get_queen_moves", [SQUARE_IDX["d5"]])
    ),
    "WHITE_QUEEN_EP": (
        [("d5", "w_queen"), ("d3", "b_rook"), ("f7", "w_king"), (EP_IDX, EP_FILE["h"])],
        [["d5"] * 23,
         ["w_queen"] * 23,
         ["d3", "d4", "d6", "d7", "d8", "a5", "b5", "c5", "e5", "f5", "g5", "h5",
          "a8", "b7", "c6", "e4", "f3", "g2", "h1", "a2", "b3", "c4", "e6"],
         ["b_rook"] + ["empty"] * 22,
         [0b1111] * 23,
         [0b1111] * 23,
         [EP_FILE["h"]] * 23,
         [-1] * 23],
        ("get_queen_moves", [SQUARE_IDX["d5"]])
    ),
    "BLACK_QUEEN_BASIC": (
        [("d5", "b_queen"), ("d3", "w_rook"), ("f7", "b_king"), (TURN_IDX, False)],
        [["d5"] * 23,
         ["b_queen"] * 23,
         ["d3", "d4", "d6", "d7", "d8", "a5", "b5", "c5", "e5", "f5", "g5", "h5",
          "a8", "b7", "c6", "e4", "f3", "g2", "h1", "a2", "b3", "c4", "e6"],
         ["w_rook"] + ["empty"] * 22],
        ("get_queen_moves", [SQUARE_IDX["d5"]])
    ),
    "BLACK_QUEEN_EP": (
        [("d5", "b_queen"), ("d3", "w_rook"), ("f7", "b_king"),
         (EP_IDX, EP_FILE["h"]), (TURN_IDX, False)],
        [["d5"] * 23,
         ["b_queen"] * 23,
         ["d3", "d4", "d6", "d7", "d8", "a5", "b5", "c5", "e5", "f5", "g5", "h5",
          "a8", "b7", "c6", "e4", "f3", "g2", "h1", "a2", "b3", "c4", "e6"],
         ["w_rook"] + ["empty"] * 22,
         [0b1111] * 23,
         [0b1111] * 23,
         [EP_FILE["h"]] * 23,
         [-1] * 23],
        ("get_queen_moves", [SQUARE_IDX["d5"]])
    ),
    "WHITE_PAWN_SINGLE_MOVE_SIMPLE": (
        [("h3", "w_pawn")],
        [["h3"],
         ["w_pawn"],
         ["h4"],
         ["empty"]],
        ("get_pawn_moves", [SQUARE_IDX["h3"]])
    ),
    "BLACK_PAWN_SINGLE_MOVE_SIMPLE": (
        [("a6", "b_pawn"), (TURN_IDX, False)],
        [["a6"],
         ["b_pawn"],
         ["a5"],
         ["empty"]],
        ("get_pawn_moves", [SQUARE_IDX["a6"]])
    ),
    "WHITE_PAWN_BLOCKED_ALLY": (
        [("h2", "w_pawn"), ("h3", "w_bishop")],
        [[] * 4],
        ("get_pawn_moves", [SQUARE_IDX["h2"]])
    ),
    "WHITE_PAWN_BLOCKED_ENEMY": (
        [("h2", "w_pawn"), ("h3", "b_rook")],
        [[] * 4],
        ("get_pawn_moves", [SQUARE_IDX["h2"]])
    ),
    "BLACK_PAWN_BLOCKED_ALLY": (
        [("a7", "w_pawn"), ("a6", "b_bishop"), (TURN_IDX, False)],
        [[] * 4],
        ("get_pawn_moves", [SQUARE_IDX["a7"]])
    ),
    "BLACK_PAWN_BLOCKED_ENEMY": (
        [("a7", "w_pawn"), ("a6", "w_rook"), (TURN_IDX, False)],
        [[] * 4],
        ("get_pawn_moves", [SQUARE_IDX["a7"]])
    ),
    "WHITE_PAWN_DOUBLE_MOVE": (
        [("h2", "w_pawn")],
        [["h2"] * 2,
         ["w_pawn"] * 2,
         ["h3", "h4"],
         ["empty"] * 2,
         [None, 0b1111],
         [None, 0b1111],
         [None, -1],
         [None, EP_FILE["h"]]],
        ("get_pawn_moves", [SQUARE_IDX["h2"]])
    ),
    "BLACK_PAWN_DOUBLE_MOVE": (
        [("a7", "w_pawn"), (TURN_IDX, False)],
        [["a7"] * 2,
         ["b_pawn"] * 2,
         ["a6", "a5"],
         ["empty"] * 2,
         [None, 0b1111],
         [None, 0b1111],
         [None, -1],
         [None, EP_FILE["a"]]],
        ("get_pawn_moves", [SQUARE_IDX["a7"]])
    ),
    "WHITE_PAWN_ATTACK": (
        [("d5", "w_pawn"), ("d6", "b_pawn"), ("e6", "b_rook"), ("c6", "b_bishop")],
        [["d5"] * 2,
         ["w_pawn"] * 2,
         ["e6", "c6"],
         ["b_rook", "b_bishop"]],
        ("get_pawn_moves", [SQUARE_IDX["d5"]])
    ),
    "BLACK_PAWN_ATTACK": (
        [("d5", "b_pawn"), ("d4", "b_pawn"), ("e4", "w_rook"),
         ("c4", "w_bishop"), (TURN_IDX, False)],
        [["d5"] * 2,
         ["b_pawn"] * 2,
         ["e4", "c4"],
         ["w_rook", "w_bishop"]],
        ("get_pawn_moves", [SQUARE_IDX["d5"]])
    ),
    "WHITE_PAWN_PROMOTE": (
        [("d7", "w_pawn"), (EP_IDX, EP_FILE["b"])],
        [["d7"] * 4,
         ["w_pawn"] * 4,
         ["d7"] * 4,
         ["w_queen", "w_bishop", "w_rook", "w_knight"],
         [0b1111] * 4,
         [0b1111] * 4,
         [EP_FILE["b"]] * 4,
         [-1] * 4,
         ["d7"] * 4,
         ["w_queen", "w_bishop", "w_rook", "w_knight"],
         ["d8"] * 4,
         ["empty"] * 4],
        ("get_pawn_moves", [SQUARE_IDX["d7"]])
    ),
    "BLACK_PAWN_PROMOTE": (
        [("b2", "b_pawn"), (EP_IDX, EP_FILE["b"]), (TURN_IDX, False)],
        [["b2"] * 4,
         ["b_pawn"] * 4,
         ["b2"] * 4,
         ["b_queen", "b_bishop", "b_rook", "b_knight"],
         [0b1111] * 4,
         [0b1111] * 4,
         [EP_FILE["b"]] * 4,
         [-1] * 4,
         ["b2"] * 4,
         ["b_queen", "b_bishop", "b_rook", "b_knight"],
         ["b1"] * 4,
         ["empty"] * 4],
        ("get_pawn_moves", [SQUARE_IDX["b2"]])
    ),
    "WHITE_PAWN_PROMOTE_TAKE": (
        [("d7", "w_pawn"), (EP_IDX, EP_FILE["b"]), ("e8", "b_rook"), ("c8", "b_bishop"),
         ("d8", "b_king")],
        [["d7"] * 8,
         ["w_pawn"] * 8,
         ["d7"] * 8,
         ["w_queen", "w_bishop", "w_rook", "w_knight"] * 2,
         [0b1111] * 8,
         [0b1111] * 8,
         [EP_FILE["b"]] * 8,
         [-1] * 8,
         ["d7"] * 8,
         ["w_queen", "w_bishop", "w_rook", "w_knight"] * 2,
         ["e8"] * 4 + ["c8"] * 4,
         ["b_rook"] * 4 + ["b_bishop"] * 4],
        ("get_pawn_moves", [SQUARE_IDX["d7"]])
    ),
    "BLACK_PAWN_PROMOTE_TAKE": (
        [("b2", "b_pawn"), (EP_IDX, EP_FILE["b"]), (TURN_IDX, False),
         ("a1", "w_rook"), ("c1", "w_bishop"), ("b1", "w_king")],
        [["b2"] * 8,
         ["b_pawn"] * 8,
         ["b2"] * 8,
         ["b_queen", "b_bishop", "b_rook", "b_knight"] * 2,
         [0b1111] * 8,
         [0b1111] * 8,
         [EP_FILE["b"]] * 8,
         [-1] * 8,
         ["b2"] * 8,
         ["b_queen", "b_bishop", "b_rook", "b_knight"] * 2,
         ["a1"] * 4 + ["c1"] * 4,
         ["w_rook"] * 4 + ["w_bishop"] * 4],
        ("get_pawn_moves", [SQUARE_IDX["b2"]])
    ),
    "WHITE_EN_PASSANT_TAKE_LEFT": (
        [("c5", "w_pawn"), (EP_IDX, EP_FILE["b"]), ("b5", "b_pawn")],
        [["c5"] * 2,
         ["w_pawn"] * 2,
         ["c6", "b6"],
         ["empty"] * 2,
         [0b1111] * 2,
         [0b1111] * 2,
         [EP_FILE["b"]] * 2,
         [-1] * 2,
         [None, "b5"],
         [None, "empty"],
         [None, "b5"],
         [None, "b_pawn"]],
        ("get_pawn_moves", [SQUARE_IDX["c5"]])
    ),
    "WHITE_EN_PASSANT_TAKE_RIGHT": (
        [("c5", "w_pawn"), (EP_IDX, EP_FILE["d"]), ("d5", "b_pawn")],
        [["c5"] * 2,
         ["w_pawn"] * 2,
         ["c6", "d6"],
         ["empty"] * 2,
         [0b1111] * 2,
         [0b1111] * 2,
         [EP_FILE["d"]] * 2,
         [-1] * 2,
         [None, "d5"],
         [None, "empty"],
         [None, "d5"],
         [None, "b_pawn"]],
        ("get_pawn_moves", [SQUARE_IDX["c5"]])
    ),
    "BLACK_EN_PASSANT_TAKE_LEFT": (
        [("a4", "w_pawn"), (EP_IDX, EP_FILE["a"]), ("b4", "b_pawn"), (TURN_IDX, False)],
        [["b4"] * 2,
         ["b_pawn"] * 2,
         ["b3", "a3"],
         ["empty"] * 2,
         [0b1111] * 2,
         [0b1111] * 2,
         [EP_FILE["a"]] * 2,
         [-1] * 2,
         [None, "a4"],
         [None, "empty"],
         [None, "a4"],
         [None, "w_pawn"]],
        ("get_pawn_moves", [SQUARE_IDX["b4"]])
    ),
    "BLACK_EN_PASSANT_TAKE_RIGHT": (
        [("c4", "w_pawn"), (EP_IDX, EP_FILE["c"]), ("b4", "b_pawn"), (TURN_IDX, False)],
        [["b4"] * 2,
         ["b_pawn"] * 2,
         ["b3", "c3"],
         ["empty"] * 2,
         [0b1111] * 2,
         [0b1111] * 2,
         [EP_FILE["c"]] * 2,
         [-1] * 2,
         [None, "c4"],
         [None, "empty"],
         [None, "c4"],
         [None, "w_pawn"]],
        ("get_pawn_moves", [SQUARE_IDX["b4"]])
    ),
    "WHITE_CASTLE_MOVES_NO_RIGHTS": (
        [("e1", "w_king"), ("a1", "w_rook"), ("h1", "w_rook"), (CASTLE_IDX, 0)],
        [],
        ("get_castle_moves", [])
    ),
    "BLACK_CASTLE_MOVES_NO_RIGHTS": (
        [("e8", "b_king"), ("a8", "b_rook"), ("h8", "b_rook"),
         (CASTLE_IDX, 0), (TURN_IDX, False)],
        [],
        ("get_castle_moves", [])
    ),
    "WHITE_CASTLE_MOVES_SHORT": (
        [("e1", "w_king"), ("a1", "w_rook"), ("h1", "w_rook"), (CASTLE_IDX, 0b1101)],
        [["e1"],
         ["w_king"],
         ["g1"],
         ["empty"],
         [0b1101],
         [0b1100],
         [-1],
         [-1],
         ["h1"],
         ["w_rook"],
         ["f1"],
         ["empty"]],
        ("get_castle_moves", [])
    ),
    "BLACK_CASTLE_MOVES_SHORT": (
        [("e8", "b_king"), ("a8", "b_rook"), ("h8", "b_rook"),
         (CASTLE_IDX, 0b0110), (TURN_IDX, False)],
        [["e8"],
         ["b_king"],
         ["g8"],
         ["empty"],
         [0b0110],
         [0b0010],
         [-1],
         [-1],
         ["h8"],
         ["b_rook"],
         ["f8"],
         ["empty"]],
        ("get_castle_moves", [])
    ),
    "WHITE_CASTLE_MOVES_LONG": (
        [("e1", "w_king"), ("a1", "w_rook"), ("h1", "w_rook"), (CASTLE_IDX, 0b1010)],
        [["e1"],
         ["w_king"],
         ["c1"],
         ["empty"],
         [0b1010],
         [0b1000],
         [-1],
         [-1],
         ["a1"],
         ["w_rook"],
         ["d1"],
         ["empty"]],
        ("get_castle_moves", [])
    ),
    "BLACK_CASTLE_MOVES_LONG": (
        [("e8", "b_king"), ("a8", "b_rook"), ("h8", "b_rook"),
         (CASTLE_IDX, 0b1000), (TURN_IDX, False)],
        [["e8"],
         ["b_king"],
         ["c8"],
         ["empty"],
         [0b1000],
         [0b0000],
         [-1],
         [-1],
         ["a8"],
         ["b_rook"],
         ["d8"],
         ["empty"]],
        ("get_castle_moves", [])
    ),
    "WHITE_CASTLE_MOVES_HAPPY": (
        [("e1", "w_king"), ("a1", "w_rook"), ("h1", "w_rook")],
        [["e1"] * 2,
         ["w_king"] * 2,
         ["g1", "c1"],
         ["empty"] * 2,
         [0b1111] * 2,
         [0b1100] * 2,
         [-1] * 2,
         [-1] * 2,
         ["h1", "a1"],
         ["w_rook"] * 2,
         ["f1", "d1"],
         ["empty"] * 2],
        ("get_castle_moves", [])
    ),
    "BLACK_CASTLE_MOVES_HAPPY": (
        [("e8", "b_king"), ("a8", "b_rook"), ("h8", "b_rook"), (TURN_IDX, False)],
        [["e8"] * 2,
         ["b_king"] * 2,
         ["g8", "c8"],
         ["empty"] * 2,
         [0b1111] * 2,
         [0b0011] * 2,
         [-1] * 2,
         [-1] * 2,
         ["h8", "a8"],
         ["b_rook"] * 2,
         ["f8", "d8"],
         ["empty"] * 2],
        ("get_castle_moves", [])
    ),
    "WHITE_CASTLE_MOVES_BLOCKED": (
        [("e1", "w_king"), ("a1", "w_rook"), ("h1", "w_rook"),
         ("f1", "w_bishop"), ("b1", "b_knight"),],
        [],
        ("get_castle_moves", [])
    ),
    "BLACK_CASTLE_MOVES_BLOCKED": (
        [("e8", "b_king"), ("a8", "b_rook"), ("h8", "b_rook"),
         ("f8", "w_bishop"), ("b8", "b_knight"), (TURN_IDX, False)],
        [],
        ("get_castle_moves", [])
    ),
    "WHITE_CANT_CASTLE_IN_CHECK": (
        [("e1", "w_king"), ("a1", "w_rook"), ("h1", "w_rook"), (W_KING_IDX, "e1"),
         ("e8", "b_queen")],
        [],
        ("get_castle_moves", [])
    ),
    "WHITE_CANT_CASTLE_ACROSS_THREATENED_SQUARES_SHORT": (
        [("e1", "w_king"), ("a1", "w_rook"), ("h1", "w_rook"), 
         (W_KING_IDX, "e1"), ("f8", "b_rook")],
        [["e1"],
         ["w_king"],
         ["c1"],
         ["empty"],
         [0b1111],
         [0b1100],
         [-1],
         [-1],
         ["a1"],
         ["w_rook"],
         ["d1"],
         ["empty"]],
        ("get_castle_moves", [])
    ),
    "WHITE_CANT_CASTLE_ACROSS_THREATENED_SQUARES_LONG": (
        [("e1", "w_king"), ("a1", "w_rook"), ("h1", "w_rook"), 
         (W_KING_IDX, "e1"), ("c2", "b_pawn")],
        [["e1"],
         ["w_king"],
         ["g1"],
         ["empty"],
         [0b1111],
         [0b1100],
         [-1],
         [-1],
         ["h1"],
         ["w_rook"],
         ["f1"],
         ["empty"]],
        ("get_castle_moves", [])
    ),
    "BLACK_CANT_CASTLE_IN_CHECK": (
        [("e8", "b_king"), ("a8", "b_rook"), ("h8", "b_rook"),
         (B_KING_IDX, "e8"), ("h5", "w_bishop"), (TURN_IDX, False)],
        [],
        ("get_castle_moves", [])
    ),
    "BLACK_CANT_CASTLE_ACROSS_THREATENED_SQUARES_SHORT": (
        [("e8", "b_king"), ("a8", "b_rook"), ("h8", "b_rook"),
         (B_KING_IDX, "e8"), ("g1", "w_queen"), (TURN_IDX, False)],
        [["e8"],
         ["b_king"],
         ["c8"],
         ["empty"],
         [0b1111],
         [0b0011],
         [-1],
         [-1],
         ["a8"],
         ["b_rook"],
         ["d8"],
         ["empty"]],
        ("get_castle_moves", [])
    ),
    "BLACK_CANT_CASTLE_ACROSS_THREATENED_SQUARES_LONG": (
        [("e8", "b_king"), ("a8", "b_rook"), ("h8", "b_rook"),
         (B_KING_IDX, "e8"), ("c7", "w_pawn"), (TURN_IDX, False)],
        [["e8"],
         ["b_king"],
         ["g8"],
         ["empty"],
         [0b1111],
         [0b0011],
         [-1],
         [-1],
         ["h8"],
         ["b_rook"],
         ["f8"],
         ["empty"]],
        ("get_castle_moves", [])
    ),
}


# Using the move test dict keys as test parameters for easier debugging
@pytest.mark.parametrize("test_key", MOVE_TEST_DICT.keys())
def test_get_moves(board_state_generator, test_key: str):
    """After making modifications to empty board, this calls func_name of empty board with args
    and asserts the set of that return value is the same as the set of the expected_instructions"""
    # Unpack the test information
    mods, instruction_gen_args, (func, args) = MOVE_TEST_DICT[test_key]

    # Unpack the modifications to the state and apply them
    board = board_state_generator(mods)

    # Generate the instruction set
    if len(instruction_gen_args) == 4:
        expected_instructions = set(
            (SQUARE_IDX[from_tile], SQUARE_STATES[from_state],
             SQUARE_IDX[to_tile], SQUARE_STATES[to_state])
            for from_tile, from_state, to_tile, to_state in zip(*instruction_gen_args))
    elif len(instruction_gen_args) == 8:
        expected_instructions = set(
            (SQUARE_IDX[from_tile], SQUARE_STATES[from_state],
             SQUARE_IDX[to_tile], SQUARE_STATES[to_state],
             castle_from, castle_to, ep_from, ep_to)
            for from_tile, from_state, to_tile, to_state,
                castle_from, castle_to, ep_from, ep_to in zip(*instruction_gen_args))
    else:  # This means len(instruction_gen_args) == 12
        expected_instructions = set(
            (SQUARE_IDX[from_tile], SQUARE_STATES[from_state],
             SQUARE_IDX[to_tile], SQUARE_STATES[to_state],
             castle_from, castle_to, ep_from, ep_to,
             SQUARE_IDX.get(from2_tile, None), SQUARE_STATES.get(from2_state, None),
             SQUARE_IDX.get(to2_tile, None), SQUARE_STATES.get(to2_state, None),)
            for from_tile, from_state, to_tile, to_state,
                castle_from, castle_to, ep_from, ep_to,
                from2_tile, from2_state, to2_tile, to2_state, in zip(*instruction_gen_args))

    # Remove None instructions to allow for short instructions:
    new_set = set()
    for item in expected_instructions:
        if None in item:
            new_set.add(item[:item.index(None)])
        else:
            new_set.add(item)
    expected_instructions = new_set

    # Check it against what the engine returns
    actual_instructions = set(getattr(board, func)(*args))
    print(f"{actual_instructions=}")
    print(f"{expected_instructions=}")

    # Redundant checking for easy debugging
    assert len(actual_instructions) == len(expected_instructions)
    for move in actual_instructions:
        assert move in expected_instructions
    for move in expected_instructions:
        assert move in actual_instructions
    assert actual_instructions == expected_instructions
