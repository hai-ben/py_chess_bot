# pylint: disable-all
from src.prototyping.board import ChessBoard


class Matcher:
    PLAYER_LOOKUP = {
        1: "WHITE",
        -1: "BLACK"
    }

    def __init__(self, white_eval_func, black_eval_func) -> None:
        self.trials = {
            "DRAW": 0,
            "WHITE": {
                "win_turns": [],
                "stalemate_turns": []
            },
            "BLACK": {
                "win_turns": [],
                "stalemate_turns": []
            },
        }
        self.white_eval = white_eval_func
        self.black_eval = black_eval_func
    
    def play_trials(self, n_trials=100, max_turns=1_000):
        for _ in range(n_trials):
            print(f"trial {_} of 100.")
            result, player, turn = self.play_match(max_turns)
            if result == "DRAW":
                self.trials["DRAW"] += 1
            elif result == "CHECKMATE":
                self.trials[self.PLAYER_LOOKUP[-player]]["win_turns"].append(turn)
            else:
                self.trials[self.PLAYER_LOOKUP[-player]]["stalemate_turns"].append(turn)

    def play_match(self, max_turns=1_000):
        state = ChessBoard()
        state.standard_setup()
        for i in range(max_turns):
            if i % 10 == 0:
                print(f"turn {i} of {max_turns}")
            new_moves = state.legal_moves(state.player_turn)
            if len(new_moves) < 1:
                if state.in_check(state.player_turn):
                    return "CHECKMATE", state.player_turn, i + 1
                else:
                    return "STALEMATE", state.player_turn, i + 1
            state = self.play_best_move(new_moves, state.player_turn)
            # print(state)
            # print("\n\n")
            # _ = input()
        return "DRAW", state.player_turn, i + 1
    
    def play_best_move(self, moves, player):
        best_move = moves[0]
        max_eval = self.white_eval(moves[0])
        eval_func = self.white_eval if player == 1 else self.black_eval
        for move in moves:
            new_eval = eval_func(move)
            if new_eval > max_eval:
                max_eval = new_eval
                best_move = move
        return best_move