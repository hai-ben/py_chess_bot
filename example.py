from datetime import datetime
from random import random
from board import ChessBoard
from matcher import Matcher

def white_func(_):
    return random()

def black_func(_):
    return random()

m = Matcher(white_func, black_func)

current_time = datetime.now().strftime("%H:%M:%S")
print("Current Time =", current_time)
m.play_trials()
current_time = datetime.now().strftime("%H:%M:%S")
print("Current Time =", current_time)

print(m.trials)