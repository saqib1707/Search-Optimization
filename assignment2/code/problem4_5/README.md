Implement Expectimax to Play 2048
=========
[DO NOT FORK THIS REPO]
----
Implement a game AI for the 2048 game based on expectimax search. The base game engine uses code from [here](https://gist.github.com/lewisjdeane/752eeba4635b479f8bb2). 

Task
-----
Model the AI player as a max player, and the computer as a chance player (picking a random open spot to place a 2-tile). Implement a depth-3 game tree and the expectimax algorithm to compute decisions for the AI player. Use the score returned by the game engine as the evaluation function value at the leaf nodes of the depth-3 game trees. 

You can play the game manually using the arrow keys. Pressing 'Enter' will let the AI play, and pressing 'Enter' again will stop the AI player. Read the game engine code from 'game.py' and see how it returns the game state and evaluate its score from an arbitrary game state after an arbitrary player move. 

A depth-3 game tree means the tree should have the following levels: 

- root: player
- level 1: computer 
- level 2: player
- level 3: terminal with payoff (note that we say "terminal" to mean the leaf nodes in the shallow game tree, not the termination of the game itself)

This tree represents all the game states of a player-computer-player sequence (the player makes a move, the computer place a tile, and then the player makes another move, and then evaluate the score) from the current state. Compute the expectimax values of all the nodes in the game tree, and return the optimal move for the player. In the starter code, the AI just returns a random move.

If you have implemented the AI correctly, your depth-3 search should almost always reach 512 tiles and a score over 5000 quite often, as shown in 'demo.mov'. 

Usage
-----
To run the program:
```
    python main.py
```

The file 'test.py' contains code for testing that with the depth-3 tree and the expectimax algorithm, your AI returns the right directions and values on 3 test states. Run the tests using:
```
    python main.py -t 1
```

To run extra credit tests, run:
```
    python main.py -t 2
```

Once your program is running, here are a few keyboard options available in-game:
- 'r': restart the game
- 'u': undo a move
- '3'-'7': change board size
- 'g': toggle grayscale
- 'e': switch to extra credit

NOTE: For grading, we will run tests in the same way on other test states and see if your depth-3 tree and experimax values are computed correctly. 

Design Evaluation Functions
------
While depth-3 search gives okay performance, it can apparently be improved by searching more depth or improving the evaluation function, or both. For improving the evaluation function, you can implement a heuristic value that takes into account of the difference between a "good" and "bad" game state. You can feel free to use online resources to see what strategies people have been using to reach higher scores in 2048. 

You can implement a stronger AI in the `compute_decision_ec` function at the bottom of the `ai.py` file. When running the game, pressing `e` will activate/deactivate the decisions made by the `compute_decision_ec` function. 

To test this part of the implementation, run:

```
    python main.py -t 2
```

NOTE: In order to get the extra credits, you will need to achieve a score of more than 20,000 on at least 4/10 runs. The tester will show whether you have succeeded. 
