# TIC TAC TOE with AI
# Written By: Evan Lamb
# Date Written: 8/8/2020
# Create a Tic Tac Toe game with 3 levels of difficulty

# ISSUES:
# 1) Code requires running of is_winner twice in the case that game_over returns True (that's a lot of wasted time)
# 2) Hard difficulty assumes that player1 is hard and player2 is something else (because I 
# hard coded the scores dictionary)
# 3) Minimax algorithm does not work--check use of is_winner because I do not think the alg
# is recognizing the potential for winning for its opponent

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
        print("------------")
        print(f'| {self.board["7"]} | {self.board["8"]} | {self.board["9"]} |')
        print("------------")
        print(f'| {self.board["4"]} | {self.board["5"]} | {self.board["6"]} |')
        print("------------")
        print(f'| {self.board["1"]} | {self.board["2"]} | {self.board["3"]} |')
        print("------------")

    def update_board(self, move, player=None):
        if player:
            self.board[move] = player.token 
        else:
            self.board[move] = ' '

    def is_open(self, move):
        return True if self.board[move] == ' ' else False

    def open_spaces(self):
        options = [k for k,v in self.board.items() if v == ' ']
        return options

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

    def is_winner(self, player):
        '''return whether someone has one. If so, who'''
        for i, j, k in self.win_conditions:
            if self.board[i] == self.board[j] == self.board[k] == player.token:
                return True, player
        return False

    def game_over(self, player):
        return True if self.is_full() or self.is_winner(player) else False

class Player():

    def __init__(self, strategy, token, name):
        self.strategy = strategy
        self.token = token
        self.name = name

    def make_move(self, board, game):
        return self.strategy(self, board, game)

def minimax(board, player, game, depth, isMaximizer):
    '''recursively determine the optimal play for all board positions'''
    # base case -- Problem is probably in these base cases
    if board.game_over(player):
        if board.is_winner(player): 
            score = scores[player.token]
        else:
            score = scores['Tie']
        return score

    if isMaximizer:
        bestScore = float("-inf")
        for move in board.open_spaces():
            board.update_board(move, player)
            score = minimax(board, game.change_turn(player), game, depth + 1, False)
            board.update_board(move) # undo the update 
            bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = float("inf")
        for move in board.open_spaces():
            board.update_board(move, player) 
            score = minimax(board, game.change_turn(player), game, depth + 1, True)
            board.update_board(move) # undo the update 
            bestScore = min(score, bestScore)
        return bestScore

# Define the possible strategies for make_move method

def Hard(player, board, game):
    '''best move is determined using the minimax algorithm'''
    bestScore = float("-inf")
    bestMove = None
    # loop through possible moves given the current board
    for move in board.open_spaces():
        board.update_board(move, player)
        score = minimax(board, player, game, 0, False) #using True doesn't help
        board.update_board(move) # undo the update 
        if score > bestScore:
            bestScore = score
            bestMove = move
    return bestMove


def Medium(player, board, game):
    '''Win, if possible. If not, block. Else, random.'''
    move = board.win_possible(player)
    if move:
        return move
    move = board.win_possible(game.change_turn(player))
    if move:
        return move
    else:
        return random.choice(board.open_spaces())

def Easy(player, board, game=None):
    '''Play randomly'''
    return random.choice(board.open_spaces())

def User(player, board, game=None):
    move = input("Insert move (1-9): ")
    while move not in board.get_keys():
        print("Please enter a value between 1 and 9")
        move = input("Insert move (1-9): ")
    return move

class Game():

    def __init__(self, p1_diff, p2_diff, p1_name, p2_name):
        self.p1 = Player(p1_diff, 'X', p1_name)
        self.p2 = Player(p2_diff, 'O', p2_name)
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

# Assign reward values for minimax
scores = {
    'X': 1,
    'O': -1,
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
        move = str(player.make_move(game.board, game))
        while not game.board.is_open(move):
            print("Position already occupied. Please try again.")
            move = player.make_move(game.board, game)
        game.board.update_board(move, player)
        print(f'{player.name} played at position {move}.')
        game.board.print_board()

        if game.board.game_over(player):
            if game.board.is_winner(player):
                print(f'{player.name} wins!')
                return query_new_game()
            else:
                if game.board.is_full():
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