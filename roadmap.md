## Roadmap ##

This is just a place for me to mess around with python, ML, and code performance evaluation right now the rough road map is:
- Get a decent engine with stock python. No numpy, I want to really see what I can push out of stock python:
    - Algebriac notation
        - I/O will let me interface with other chess bots fairly easily
        - Allows of unit tests to make sure the engine doesn't have any weird bugs
    - Get some base-line performance numbers for for future performance testing

- Train an extremely basic chess bot:
    - Each "node" in the board (6x8x8) will connect to this neuron with a weight.
    - The sum of inputs times weights will determine the "score" of a board state
    - Each legal move will be evaluated using this score and the best move (0-depth) will be chosen
    - Starting from a normal random distrubtion on the weights, chose a random descent vector
    - Perform gradient descent steps until a plateau is reached
    - Evaluate the bot's performance against stockfish on different settings

- More advanced work to come