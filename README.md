# Tic-Tac-Toe-with-AI
Play Tic-Tac-Toe with friends or against the AI!

# Features
1) Supports 3 AI difficulties with the following protocols:

  * Easy: Play randomly
  * Medium: Win if possible. If not, block if possible. If not, play randomly.
  * Hard: Make optimal move (via minimax algorithm)

2) Supports 4 game modes:

  * Human vs Human
  * Human vs AI
  * AI vs Human
  * AI vs AI

3) The move-making protocols are determined at run time using a Behavioral Design Pattern
known as Strategy Method (aka Policy Method) which permits easier scalability if more
difficulty levels were to be introduced. In this code, the contents of the make_move
method in the Player class are replaced with the contents of the four strategy functions
defined outside the class.

4) Rewards AI for quicker wins and reduces the punishment for late game losses via "decay
reward/punishment as depth of recursion increases" idea.

5) Handles improper input and various sessions

# Minimax Algorithm

The Minimax algorithm is a recursive search algorithm that determines the best move given
the current board state. It does this by creating a tree of all future possibilities where 
positive endings (i.e. it wins) result in a reward and negative endings (i.e. it loses) result
in a negative reward. Ties result in no reward. This recursion continues until all possible states
(in the case of Tic Tac Toe) have been evalauted and the best move is determined as the move with 
the greatest score. Below is an example of the algorithm at work courtesy of 
theoryofprogramming.com.

![minimax_alg] (minimax_alg.JPG?raw=true)
Fig. 1 Minimax Algorithm Search Tree




