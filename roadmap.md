## Roadmap ##

This is just a place for me to mess around with python, ML, and code performance evaluation right now the rough road map is:
- Get a decent engine with stock python. No numpy, I want to really see what I can push out of stock python:
    - **DONE** Prototype to get a good hold on the problem
    - **DONE** Get some base-line performance numbers for for future performance testing
    - **DONE** Datastructure Definition
        - **DONE** What the list represents
        - **DONE** How the graph will be tracked
    - Class Diagrams
        - The board itself
        - The wrapper that tells the engine to do stuff
    - Full suite of unit tests from small_board and board tests
    - Basic engine should be able to at least generate 100k states per second before proceeding to bot building

- Train an extremely basic chess bot:
    - Prototype a game-playing framework, using basic strategies
    inspired and copied by work done by tom7 http://tom7.org/chess/weak.pdf:
        - random_move
        - same_color
        - swarm
        - generous
        - cccp
        - suicide_king
        - min_oppt_moves
        - pacifist
    - Build an extremely simple strategy that has a score look-up for each square-state combination
    - Play this strategy against itself to perform a gradient descent
    - Create plugins for other engines to add to the evaluation
    - Construct addtiional NN-based architecture strategies.