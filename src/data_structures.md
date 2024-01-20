# Data Structures
## Internal Board State Representation
This list is used to completely represent a chessboard, minus some information regarding draws.
[a8][b8]...[g1][h1][white_king_idx][black_king_idx][castle_state][en_passant_state][white_to_play]

A more detailed explaination of what indices represent:
* 0-63 inclusive represent each square on the chessboard. Stored at each of these indicies is an int representing one of the 13 unique states a square can have:
    * 0: Empty
    * 1: White Pawn.
    * 2: White Knight.
    * 3: White Bishop.
    * 4: White Rook.
    * 5: White Queen.
    * 6: White King.
    * 7-12: Black pieces, in the same order as white.
    This order is important as it's very fast to check which player controlls the piece on the tile, if these states were interwoven (1/2 representing white/black pawns). e.g.: ```7 > list[2] > 0``` is much faster than ```list[2] != and list[2] % 2 == 0```.

* 64 and 65 store the index of which tile the black and white king are "in" respectively

* 66 stores an int representing one of the 16 possible castling-right combinations:
    * 0b0000: No player can castle.
    * 0b0001: White can short castle.
    * 0b0010: White can long castle.
    * 0b0100: Black can short castle.
    * 0b1000: Black can long castle.

* 67 stores an int representing which file, if any, en passant is legal on:
    * -1: Enpassant is not legal.
    * 0: Enpassant is legal on the a-file.
    * 7: Enpassant is legal on the h-file.

* 68 stores an bool that is True if it is white's turn to play.


## Board Traversals/Operations
A set of operations that transforms board state A to board state B is tuple of length 4, 8, or 12 with the following entries in order:
* The following are always included:
    * origin_tile_index (used for king in a castle command)
    * origin_tile_state (used for king in a castle command)
    * destiniation_tile_index
    * destiniation_tile_state
* The following are only included if there is a change in castle and/or enpassant state
    * pre_move_castle_state
    * post_move_castle_state
    * pre_move_en_passant_state
    * post_move_en_passant_state
* The following are used for a second move set, to do things like castling, en_passant pawn deletion, or pawn promotion
    * origin_tile2_index
    * origin_tile2_state
    * destiniation_tile2_index
    * destiniation_tile2_state

Here are some example instruction sets:
* Black takes a rook on a3 with their knight: ```("c4", "b_knight", "a3", "w_rook")```
* White double moves a pawn: ```("d2", "w_pawn", "d4", "empty", 0b1111, 0b1111, -1, "d-file")```
* Black moves their king: ```("e8", "b_king", "f7", "b_king", "empty", 0b1111, 0b0011, "d-file", -1)```
* A short castle for white: ```("e1", "w_king", "g1", "empty", 0b1111, 0b1100, "h1", "w_rook", "f1", "empty")```
* Black takes a pawn on the g-file via en passant: ```("f4", "b_pawn", "g3", "empty", 0b1011, 0b1011, "g-file", -1, "g4", "empty", "g4", "w_pawn")```
* White promotes a pawn on b8 ```("b7", "w_pawn", "b7", "w_queen", 0b0000, 0b0000, -1, -1, "b7", "w_queen", "b8", "empty")```

Additional Notes:
* The order for the double instruction sets is important to make accurate hashes.
* It is assumed that the player to play changes during each transition.
* This setup makes it very easy to iterate over a tuple to modify a board state as well as updating Zobrist hashes.

## Board Sate Tracking
### Engine
The engine has the following data structures to track board-states:
* A Dictionary representing a graph
    * Key: ```zobrist_hash```
    * Value: ```((instruction_set_tuple), new_zobrist_hash)```
    A value of ```None``` is used when the position has no further legal moves (stalemate or checkmate conditions)
* A stack that holds the instruction_set_tuple's necessary to reach the current game_state form the starting game state. This way instruction sets can be popped from the top of the stack and reversed to traverse up the graph of board states

### Evaluator
* A queue that holds unexplored instruction-sets for future evaluations
* A Dictionary that holds the evaluation of each state:
    * Entry: ```zobrist_hash```
    * Value: ```board_score``` (float)