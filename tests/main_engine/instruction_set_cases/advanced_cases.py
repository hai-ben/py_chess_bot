"""Advanced test cases for the instruction set generator"""
from src.resources.data_translators import B_KING_IDX, W_KING_IDX, CASTLE_IDX, TURN_IDX, EP_IDX


ADVANCED_MOVE_TESTS = {
    "OPENING_MOVES": (
        [],
        [["a2"] * 2 + ["b2"] * 2 + ["c2"] * 2 + ["d2"] * 2 + ["e2"] * 2 + ["f2"] * 2 + ["g2"] * 2\
         + ["h2"] * 2 + ["b1"] * 2 + ["g1"] * 2,
         ["w_pawn"] * 16 + ["w_knight"] * 4,
         ["a3", "a4", "b3", "b4", "c3", "c4", "d3", "d4", "e3", "e4", "f3", "f4", "g3", "g4", "h3",
          "h4", "a3", "c3", "f3", "h3", ],
         ["empty"] * 20,
         [None, 0b1111] * 8 + [None] * 4,
         [None, 0b1111] * 8 + [None] * 4,
         [None, -1] * 8 + [None] * 4,
         [None, 0, None, 1, None, 2, None, 3, None, 4, None, 5, None, 6, None, 7] + [None] * 4],
        ("get_all_moves", [])
    ),
    "CANT_MOVE_PINNED_PIECES_W": (
        [("a2", "w_king"), ("b2", "w_pawn"), ("c2", "b_rook"),
         (CASTLE_IDX, 0), (W_KING_IDX, "a2")],
        [["a2"] * 4,
         ["w_king"] * 4,
         ["a3", "a1", "b3", "b1"],
         ["empty"] * 4],
        ("get_all_moves", [])
    ),
    "CANT_MOVE_PINNED_PIECES_B": (
        [("a2", "b_king"), ("b2", "b_pawn"), ("c2", "w_rook"),
         (CASTLE_IDX, 0), (B_KING_IDX, "a2"), (TURN_IDX, False)],
        [["a2"] * 4,
         ["b_king"] * 4,
         ["a3", "a1", "b3", "b1"],
         ["empty"] * 4],
        ("get_all_moves", [])
    ),
    "KING_WONT_WALK_INTO_CHECK_W": (
        [("a1", "w_king"), ("c1", "b_king"), (W_KING_IDX, "a1"),
         (CASTLE_IDX, 0), (B_KING_IDX, "c1")],
        [["a1"],
         ["w_king"],
         ["a2"],
         ["empty"]],
        ("get_all_moves", [])
    ),
    "KING_WONT_WALK_INTO_CHECK_B": (
        [("a1", "b_king"), ("c1", "w_king"), (B_KING_IDX, "a1"),
         (CASTLE_IDX, 0), (W_KING_IDX, "c1"), (TURN_IDX, False)],
        [["a1"],
         ["b_king"],
         ["a2"],
         ["empty"]],
        ("get_all_moves", [])
    ),
    "ONLY_KING_MOVES_FOR_DOUBLE_CHECK_W": (
        [("a1", "w_king"), ("h7", "w_rook"), (W_KING_IDX, "a1"),
         (CASTLE_IDX, 0), ("a4", "b_rook"), ("c2", "b_knight")],
        [["a1"] * 2,
         ["w_king"] * 2,
         ["b2", "b1"],
         ["empty"] * 2],
        ("get_all_moves", [])
    ),
    "ONLY_KING_MOVES_FOR_DOUBLE_CHECK_B": (
        [("a1", "b_king"), ("h7", "b_rook"), (B_KING_IDX, "a1"), (TURN_IDX, False),
         (CASTLE_IDX, 0), ("a4", "w_rook"), ("c2", "w_knight")],
        [["a1"] * 2,
         ["b_king"] * 2,
         ["b2", "b1"],
         ["empty"] * 2],
        ("get_all_moves", [])
    ),
    "ONLY_KING_MOVES_ONTO_NON_THREAT_FOR_DOUBLE_CHECK_W": (
        [("a1", "w_king"), ("h7", "w_rook"), (W_KING_IDX, "a1"), ("c1", "b_bishop"),
         (CASTLE_IDX, 0), ("a4", "b_rook"), ("c2", "b_knight")],
        [["a1"],
         ["w_king"],
         ["b1"],
         ["empty"]],
        ("get_all_moves", [])
    ),
    "ONLY_KING_MOVES_ONTO_NON_THREAT_FOR_DOUBLE_CHECK_B": (
        [("a1", "b_king"), ("h7", "b_rook"), (B_KING_IDX, "a1"), (TURN_IDX, False),
         (CASTLE_IDX, 0), ("a4", "w_rook"), ("c2", "w_knight"), ("c1", "w_bishop")],
        [["a1"],
         ["b_king"],
         ["b1"],
         ["empty"]],
        ("get_all_moves", [])
    ),
    "MUST_CAPTURE_OR_MOVE_CLOSE_ATTACKS_W": (
        [("c6", "w_king"), (W_KING_IDX, "c6"), ("d5", "b_pawn"), ("a7", "b_rook"),
         (CASTLE_IDX, 0), ("b8", "b_rook")],
        [["c6"] * 3,
         ["w_king"] * 3,
         ["c5", "d6", "d5"],
         ["empty"] * 2 + ["b_pawn"]],
        ("get_all_moves", [])
    ),
    "MUST_CAPTURE_OR_MOVE_CLOSE_ATTACKS_B": (
        [("h3", "b_king"), ("e5", "b_pawn"), (B_KING_IDX, "h3"), (TURN_IDX, False),
         (CASTLE_IDX, 0), ("g1", "w_queen"), ("f4", "w_knight"), ("g8", "b_rook")],
        [["h3", "e5"],
         ["b_king", "b_pawn"],
         ["h4", "f4"],
         ["empty", "w_knight"]],
        ("get_all_moves", [])
    ),
    "BLOCKING_MOVES_ALLOWED_W": (
        [("h1", "b_king"), (W_KING_IDX, "h1"), ("g1", "w_pawn"), ("g2", "w_pawn"),
         (CASTLE_IDX, 0), ("a3", "w_rook"), ("h8", "b_rook")],
        [["a3"],
         ["w_rook"],
         ["h3"],
         ["empty"]],
        ("get_all_moves", [])
    ),
    "BLOCKING_MOVES_ALLOWED_B": (
        [("a1", "b_king"), ("f2", "b_bishop"), (B_KING_IDX, "a1"), (TURN_IDX, False),
         (CASTLE_IDX, 0), ("b1", "b_knight"), ("a2", "b_pawn"), ("h8", "w_bishop")],
        [["f2", "b1"],
         ["b_bishop", "b_knight"],
         ["d4", "c3"],
         ["empty"] * 2],
        ("get_all_moves", [])
    ),
    "TAKE_ROOK_DISABLE_CASTLE_W_SHORT": (
        [("h1", "w_rook"), ("b7", "b_bishop"), ("a8", "b_king"),
         (B_KING_IDX, "a8"), (TURN_IDX, False), (CASTLE_IDX, 0b0011)],
        [["b7"] * 8 + ["a8"] * 2,
         ["b_bishop"] * 8 + ["b_king"] * 2,
         ["c6", "d5", "e4", "f3", "g2", "a6", "c8", "h1", "a7", "b8"],
         ["empty"] * 7 + ["w_rook"] + ["empty"] * 2,
         [None] * 7 + [0b0011] + [None] * 2,
         [None] * 7 + [0b0010] + [None] * 2,
         [None] * 7 + [-1] + [None] * 2,
         [None] * 7 + [-1] + [None] * 2],
        ("get_all_moves", [])
    ),
    "B_KING_REMOVES_EP": (
        [("a8", "b_queen"), ("a7", "b_king"), ("h4", "w_king"), (W_KING_IDX, "h4"),
         (B_KING_IDX, "a7"), (TURN_IDX, False), (CASTLE_IDX, 0b0000), (EP_IDX, 6)],
        [["a8"] * 14 + ["a7"] * 4,
         ["b_queen"] * 14 + ["b_king"] * 4,
         ["b8", "c8", "d8", "e8", "f8", "g8", "h8", "b7", "c6", "d5", "e4", "f3", "g2", "h1",
          "a6", "b6", "b7", "b8"],
         ["empty"] * 18,
         [0] * 18,
         [0] * 18,
         [6] * 18,
         [-1] * 18],
        ("get_all_moves", [])
    ),
}
