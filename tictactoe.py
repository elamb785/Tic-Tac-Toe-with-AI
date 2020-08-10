# TIC TAC TOE with AI
# Written By: Evan Lamb
# Date Written: 8/8/2020 - 8/10/20
# Create a Tic Tac Toe game with 3 levels of AI difficulty, and 4 game modes
# human vs AI, AI vs human, human vs human, and AI vs AI

import random
from itertools import combinations

class Board():

    win_conditions = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],

        ['1', '4', '7'],
        ['2', '5', '8'],
        ['3', '6', '9'],

        ['1', '5', '9'],
        ['7', '5', '3']
    ]
    
    def __init__(self):
        self.board = {'7': ' ', '8': ' ', '9': ' ',
            '4': ' ', '5': ' ', '6': ' ',
            '1': ' ', '2': ' ', '3': ' '}

    def get_keys(self):
        return self.board.keys()

    def print_board(self):
        print("-------------")
        print(f'| {self.board["7"]} | {self.board["8"]} | {self.board["9"]} |')
        print("-------------")
        print(f'| {self.board["4"]} | {self.board["5"]} | {self.board["6"]} |')
        print("-------------")
        print(f'| {self.board["1"]} | {self.board["2"]} | {self.board["3"]} |')
        print("-------------")

    def update_board(self, move, flag, player=None, isMaximizing=None):
        # for use in simulated games
        if isMaximizing != None and player == None:
            if flag == 1:
                self.board[move] = 'X' if isMaximizing else 'O'
            else:
                self.board[move] = 'O' if isMaximizing else 'X'
        # for use in real game
        elif player and isMaximizing == None:
            self.board[move] = player.token
        # for use in simulated games
        else:
            self.board[move] = ' '

    def is_open(self, move):
        return True if self.board[move] == ' ' else False

    def open_spaces(self):
        return [k for k,v in self.board.items() if v == ' ']

    def is_full(self):
        return True if set(self.board.values()) == {'X', 'O'} else False

    def win_possible(self, player):
        '''return where to play for a possible win'''
        for win in self.win_conditions:
            for i in combinations(win, 2):
                if self.board[i[0]] == self.board[i[1]] == player.token:
                    move_prelim = [spot for spot in win if spot not in i][0]     
                    if self.is_open(move_prelim):
                        return move_prelim 
        return None

    def is_winner(self, game):
        '''return whether someone has won and if so, who'''
        for i, j, k in self.win_conditions:
            if self.board[i] == self.board[j] == self.board[k] == 'X':
                return True, game.p1
            elif self.board[i] == self.board[j] == self.board[k] == 'O':
                return True, game.p2
        return False, 'No winner'

    def game_over(self, game): 
        '''returns bool game_over, bool is_winner, obj who_won'''
        results = self.is_winner(game)
        full = self.is_full()
        # Case 1: Game over
        if full or results[0] == True:
           return True, results[0], results[1]
        # Case 2: Game not over
        else:
            return False, False, 'No winner'

class Player():

    def __init__(self, strategy, token, name, scores):
        self.strategy = strategy
        self.token = token
        self.name = name
        self.scores = scores

    def make_move(self, game):
        return self.strategy(self, game)

def minimax(game, depth, isMaximizer, flag):
    '''recursively determine the optimal play for all board positions'''
    # flag = 1, player1 is using minimax in real game
    # flag = 2, player2 is using minimax in real game

    # base case
    game_complete, is_winner, who_won = game.board.game_over(game)
    if game_complete:
        if is_winner: 
            if who_won.token == 'X' and flag == 1:
                score = game.p1.scores['X'] - depth
            elif who_won.token == 'O' and flag == 1:
                score = game.p1.scores['O'] + depth
            elif who_won.token == 'X' and flag == 2:
                score = game.p2.scores['X'] + depth
            else:
                score = game.p2.scores['O'] - depth
        else:
            score = game.p1.scores['Tie']
        return score

    if isMaximizer:
        bestScore = float("-inf")
        for move in game.board.open_spaces():
            game.board.update_board(move, flag, isMaximizing=isMaximizer) 
            score = minimax(game, depth + 1, False, flag)
            # undo the winning, tying, or losing move
            game.board.update_board(move, None)  
            bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = float("inf")
        for move in game.board.open_spaces():
            game.board.update_board(move, flag, isMaximizing=isMaximizer)
            score = minimax(game, depth + 1, True, flag)
            # undo the winning, tying, or losing move
            game.board.update_board(move, None) 
            bestScore = min(score, bestScore)
        return bestScore

# Define the possible strategies for make_move method

def Hard(player, game):
    '''Best move is determined using the minimax algorithm'''
    # Determine which player is using minimax to make their turn
    flag = 1 if player.token == 'X' else 2
    bestScore = float("-inf")
    bestMove = None
    # loop through possible moves given the current board
    for move in game.board.open_spaces():
        game.board.update_board(move, None, player=player)
        score = minimax(game, 0, False, flag) 
        game.board.update_board(move, None) # undo the update 
        if score > bestScore:
                bestScore = score
                bestMove = move  
    return bestMove

def Medium(player, game):
    '''Win, if possible. If not, block. Else, random.'''
    move = game.board.win_possible(player)
    if move:
        return move
    move = game.board.win_possible(game.change_turn(player))
    if move:
        return move
    else:
        return random.choice(game.board.open_spaces())

def Easy(player, game):
    '''Play randomly'''
    return random.choice(game.board.open_spaces())

def User(player, game):
    move = input("Insert move (1-9): ")
    while move not in game.board.get_keys():
        print("Please enter a value between 1 and 9")
        move = input("Insert move (1-9): ")
    return move

class Game():

    def __init__(self, p1_diff, p2_diff, p1_name, p2_name):
        self.p1 = Player(p1_diff, 'X', p1_name, scores1)
        self.p2 = Player(p2_diff, 'O', p2_name, scores2)
        self.board = Board()

    def change_turn(self, player):
        if player is self.p1:
            return self.p2
        else:
            return self.p1

# Convert inputted strings to function types
function_mappings = {
    'Hard': Hard,
    'Medium': Medium,
    'Easy': Easy,
    'User': User
}

# define the rewards/penalties for minimax
scores1 = {
    'X': 10,
    'O': -10,
    'Tie': 0
}

scores2 = {
    'X': -10,
    'O': 10,
    'Tie': 0
}

def get_players_diff():
    '''Determine and convert to functions the inputted difficulties'''
    players = ("User", "Easy", "Medium", "Hard")
    player = []
    for i in range(1, 3):
        player_diff = input(f"Who is player {i} {players}? ").title()
        while player_diff not in players:
            print("Please enter an acceptable player name.")
            player_diff = input(f"Who is player {i} {players}? ").title()
        player.append(player_diff)
    return function_mappings[player[0]], function_mappings[player[1]]

def query_new_game():
    ans = input("Do you want to play again? [y/n] ")
    while ans not in ('y', 'n'):
        print("Please enter acceptable answer")
        ans = input("Do you want to play again? [y/n] ")
    return True if ans == 'y' else False

def start_game(p1, p2):
    p1_user = input("What is player 1's name? ")
    p2_user = input("What is player 2's name? ")
    game = Game(p1, p2, p1_user, p2_user)
    print("\n------------BEGIN GAME--------------\n")
    print("NOTE: Locations are numbered 1-9 where 1 is bottom left")
    print("and numbers increase left to right. Ex. 4 is first location")
    print("in the second row.\n")
    game.board.print_board()
    player = game.p1
    print(f'{player.name}\'s Turn')

    # initial play begins here
    while True:
        move = str(player.make_move(game))
        while not game.board.is_open(move):
            print("Position already occupied. Please try again.")
            move = player.make_move(game)
        game.board.update_board(move, None, player=player)
        print(f'Last Move: {player.name} played at position {move}.')
        game.board.print_board()
        game_complete, is_winner, who_won = game.board.game_over(game)
        if game_complete:
            if is_winner:
                print(f'{who_won.name} wins!')
                return query_new_game()
            else:
                print("Tie!")
                return query_new_game()
        else:
            player = game.change_turn(player)
            print(f'{player.name}\'s Turn')

def start_session():
    new_game = True
    while new_game:
        p1, p2 = get_players_diff()
        new_game = start_game(p1, p2)
        
if __name__ == '__main__':
    start_session()