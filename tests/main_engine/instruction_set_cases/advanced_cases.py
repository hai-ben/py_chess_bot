"""Advanced test cases for the instruction set generator"""
from src.resources.data_translators import SQUARE_IDX, B_KING_IDX, W_KING_IDX, CASTLE_IDX, EP_IDX,\
    TURN_IDX, CASTLE_STATES, EP_FILE


ADVANCED_MOVE_TESTS = {
    "OPENING MOVES": (
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
    "CANT_MOVE_PINNED_PIECES": (
        [("a2", "w_king"), ("b2", "w_pawn"), ("c2", "b_rook"),
         (CASTLE_IDX, 0), (W_KING_IDX, "a2")],
        [["a2"] * 4,
         ["w_king"] * 4,
         ["a3", "a1", "b3", "b1"],
         ["empty"] * 4],
        ("get_all_moves", [])
    ),
    "KING_WONT_WALK_INTO_CHECK": (
        [("a1", "b_king"), ("c1", "w_king"), (B_KING_IDX, "a1"),
         (CASTLE_IDX, 0), (W_KING_IDX, "c1"), (TURN_IDX, False)],
        [["a1"],
         ["b_king"],
         ["a2"],
         ["empty"]],
        ("get_all_moves", [])
    ),
}
