# Tic-Tac-Toe-with-AI
Play Tic-Tac-Toe with friends or against the AI!


# Features
1) Locations are marked as if it were a numerical keypad for intutive use.

2) Supports 3 AI difficulties with the following protocols:

  * Easy: Play randomly
  * Medium: Win if possible. If not, block if possible. If not, play randomly.
  * Hard: Make optimal move (via minimax algorithm)

3) Supports 4 game modes:

  * Human vs Human
  * Human vs AI
  * AI vs Human
  * AI vs AI

4) The move-making protocols are determined at run time using a Behavioral Design Pattern
known as Strategy Method (aka Policy Method) which permits easier scalability if more
difficulty levels were to be introduced. In this code, the contents of the make_move
method in the Player class are replaced with the contents of the four strategy functions
defined outside the class.

5) Rewards AI for quicker wins and reduces the punishment for late game losses via "decay
reward/punishment as depth of recursion increases" idea.

6) Handles improper input and various sessions

# Minimax Algorithm

The Minimax algorithm is a recursive search algorithm that determines the best move given
the current board state. It does this by creating a tree of all future possibilities where 
positive endings (i.e. it wins) result in a reward and negative endings (i.e. it loses) result
in a negative reward. Ties result in no reward. This recursion continues until all possible states
(in the case of Tic Tac Toe) have been evalauted and the best move is determined as the move with 
the greatest score. The two assumptions for minimax to work properly are that 1) the opponent 
is trying to win, and 2) there is no chance component to the game. Below is an example of the 
algorithm at work courtesy of theoryofprogramming.com.

![minimax_alg](minimax_alg.jpg?raw=true)
Fig. 1 Minimax Algorithm Search Tree

The algorithm is trying to determine the best move for X by trying all possible moves and assigning
appropriate rewards. If the game does not end, the algorithm plays for the opponent as well (O's in 
case) until a terminal state is reached. Rewards propagate up the tree from children, grandchildren, 
etc. to the root. Each of the possible choices on the actual, current game board are 
assigned a score and the greatest value is the best move. The depth is considered when applying scores.

Applying this to the above example:

| Possible Moves  | Score      | Stage Best Move| Overall Best Move     |
| --------------- | ---------- | -------------- | --------------------- |
| 2               |a. 0        |     [ ]        |     N/A               |
| 2               |b. 10-2 = 8 |     [x]        |      [ ]              |
| 4               |     10     |     N/A        |      [x]              |
| 6               | -10+1 = 9  |     N/A        |      [ ]              |



