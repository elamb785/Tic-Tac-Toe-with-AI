# TIC TAC TOE with AI
# Written By: Evan Lamb
# Date Written: 8/8/2020
# Create a Tic Tac Toe game with 3 levels of difficulty

# ISSUES:
# 1) Code requires running of is_winner twice in the case that game_over returns True (that's a lot of wasted time)
# 2) Game __init__ is terribly long and there's got to be a shorter way

import random

class Board():
    # class variables
    
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

    def update_board(self, move, player):
        self.board[move] = player.token

    def is_open(self, move):
        return True if self.board[move] == ' ' else False

    def open_spaces(self):
        options = [k for k,v in self.board.items() if v == ' ']
        return options

    def is_full(self):
        return True if set(self.board.values()) == {'X', 'O'} else False

    def is_winner(self, player):
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
        for i, j, k in win_conditions:
            if self.board[i] == self.board[j] == self.board[k] == player.token:
                return True, player.name
        return False

    def game_over(self, player):
        return True if self.is_full() or self.is_winner(player) else False

class Player():
    # class variables

    def __init__(self, strategy, token, name):
        self.strategy = strategy
        self.token = token
        self.name = name

    def make_move(self, board=None):
        return self.strategy(self, board)

# Define the possible strategies for make_move method
def Hard(player, board):
    pass

def Medium(player, board):
    pass

def Easy(player, board):
    return random.choice(board.open_spaces())

def User(player, board):
    move = input("Insert move (1-9): ")
    while move not in board.get_keys():
        print("Please enter a value between 1 and 9")
        move = input("Insert move (1-9): ")
    return move

class Game():
    # class varaibles

    def __init__(self, p1_diff, p2_diff, p1_name, p2_name):
        if p1_diff == 'Hard':
            self.p1 = Player(Hard, 'X', p1_name)
        elif p1_diff == 'Medium':
            self.p1 = Player(Medium, 'X', p1_name)
        elif p1_diff == 'Easy':
            self.p1 = Player(Easy, 'X', p1_name)
        else:
            self.p1 = Player(User, 'X', p1_name)

        if p2_diff == 'Hard':
            self.p2 = Player(Hard, 'O', p2_name)       
        elif p2_diff == 'Medium':
            self.p2 = Player(Medium, 'O', p2_name)
        elif p2_diff == 'Easy':
            self.p2 = Player(Easy, 'O', p2_name)
        else:
            self.p2 = Player(User, 'O', p2_name)

        self.board = Board()

    def change_turn(self, player):
        if player is self.p1:
            return self.p2
        else:
            return self.p1

def get_players_diff():
    players = ("User", "Easy", "Medium", "Hard")
    player = []
    for i in range(1, 3):
        player_diff = input(f"Who is player {i} {players}? ").title()
        while player_diff not in players:
            print("Please enter an acceptable player name.")
            player_diff = input(f"Who is player {i} {players}? ").title()
        player.append(player_diff)
    return player[0], player[1]

def query_new_game():
    ans = input("Do you want to play again? [y/n] ")
    while ans not in ('y', 'n'):
        print("Please enter acceptable answer")
        ans = input("Do you want to play again? [y/n] ")
    return True if ans == 'y' else False

def start_game(p1, p2):
    game_going = True

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

    while game_going:
        move = str(player.make_move(game.board))
        # Verify that move generation works
        while not game.board.is_open(move):
            print("Position already occupied. Please try again.")
            move = player.make_move(game.board)
        game.board.update_board(move, player)
        print(f'{player.name} played at position {move}.')
        game.board.print_board()

        if game.board.game_over(player):
            if game.board.is_winner(player):
                print(f'{player.name} wins!')
                game_going = False
                return query_new_game() # return False if session over 
            else:
                if game.board.is_full():
                    print("Tie!")
                    game_going = False
                    return query_new_game() # return False if session over 
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