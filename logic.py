#Yifan Tian Lab 5 ID:78921267


'''
game logic module
'''

from collections import namedtuple

GameState = namedtuple('Gamestae', ['board','turn'])
NONE = 0
WHITE = 1
BLACK = 2

direction = {'N':[-1,0],'NE':[-1,1],'E':[0,1],'SE':[1,1],\
		  'S':[1,0],'SW':[1,-1],'W':[0,-1],'NW':[-1,-1]}

def _new_game_board(row:int,column:int,topleft:'player') -> [[int]]:
    '''create blank 2D board'''
    board = []
    for cols in range(row):
        board.append([])
        for rows in range(column):
            board[-1].append(NONE)
    board[int(row/2)-1][int(column/2)-1] = topleft
    board[int(row/2)][int(column/2)] = topleft
    board[int(row/2)-1][int(column/2)] = 3 - topleft  # 3-2=1. 3-1=2. easy to change state
    board[int(row/2)][int(column/2)-1] = 3 - topleft
    return board

def _new_game(row:int,column:int,topleft:'player',first_player:'player') -> GameState:
    '''
    Returns a GameState representing a brand new game in which no
    moves have been made yet.
    '''
    return GameState(board = _new_game_board(row,column,topleft), turn = first_player)


def _draw_board(gamestate:GameState)->None:
    '''draw board according to 2D lists'''
    board = gamestate.board
    for i in range(len(board)):
        row_string = ''
        for j in range(len(board[i])):
            if board[i][j] == 1:
                row_string += 'W '
            elif board[i][j] == 2:
                row_string += 'B '
            else:
                row_string += '. '
        print(row_string)

def _game_weight(gamestate:GameState)->tuple:
    '''obtain the number of white pieces and black pieces'''
    white_num = 0
    black_num = 0
    for row in gamestate.board:
        white_num += row.count(1)
        black_num += row.count(2)
    return (black_num,white_num)

def _change_player(gamestate:GameState)->GameState:
    '''change player, used when current player cannot play'''
    new_board = gamestate.board
    new_turn = 3 - gamestate.turn
    new_GameState = GameState(board = new_board,turn = new_turn)  
    return new_GameState    


def _player_can_move(gamestate:GameState)->bool:              #check which player can moove next
    '''check if current player can move'''
    board = gamestate.board
    flag = {WHITE:0,BLACK:0}
    for i in range(len(board)):                                 #sweep all sites to check 
        for j in range(len(board[i])):
            if is_empty(gamestate,[i,j]):
                if valid_position(gamestate,[i,j])[0]:
                    flag[gamestate.turn] = 1
                    return True       
    return False

def gamestate_change(gamestate:GameState,position:list,valid_d:list)->GameState:
    ''' drop and flip pieces according to the input arguments'''
    new_board = gamestate.board
    for i in range(len(valid_d)):
        fp = [position[0],position[1]]
        direction = valid_d[i][1]
        for j in range(valid_d[i][2]):
            new_board[fp[0]][fp[1]] = gamestate.turn
            fp = [fp[0]+direction[0],fp[1]+direction[1]]
    new_turn = WHITE if gamestate.turn == BLACK else BLACK
    new_GameState = GameState(board = new_board,turn = new_turn)  
    return new_GameState


def is_empty(gamestate:GameState,p:list)->bool:
    '''check if the specfied position is occupied or not'''
    board = gamestate.board
    if board[p[0]][p[1]] == 0:
        return True
    else:
        return False

def valid_position(gamestate:GameState,position:list)->tuple:
    '''key part of the logic, input is a specifed position, check if this position is valid
    by checking its neighboring site and 8 directions'''
    board = gamestate.board
    color = gamestate.turn
    valid_d = []
    flag = 0                                        #check if there is a valid direction
    result = [False]
    for d in direction.keys():                     # check 8 directions
        cp = [position[0]+direction[d][0],position[1]+direction[d][1]]          
        try:
            if cp[0]>=0 and cp[1]>=0 and board[cp[0]][cp[1]] == (3-color):                        #check if the neighboring site has opposite color
                length = 1
                while True:                                             # choose 1 direction
                    cp = [cp[0]+direction[d][0],cp[1]+direction[d][1]]
                    if cp[0]>=0 and cp[1]>=0:
                        length += 1
                        if board[cp[0]][cp[1]] == color:                  #check if it is same color
                            flag = 1
                            valid_d.append([cp,direction[d],length])
                            break
                        if board[cp[0]][cp[1]] == 0: break #when meet blank position, break
                    else:                   #out of board, break
                        break
        except:                            #out of board
            pass
    if flag > 0:    result = (True,position,valid_d)
    return result
    

class othello:
    """class of game, has attributes describing the state of game and method to return information about game"""
    def draw_board(self)->None:
        _draw_board(self._gamestate)
    def __init__(self,row:int,column:int,first_player:'player',topleft:'player',condition:'condition')->None:           #constructor
        self._row = row
        self._column = column
        self._state = _new_game_board(row,column,topleft)
        self._turn = first_player
        self._topleft = topleft
        self._gamestate = GameState(board = self._state, turn = self._turn)
        self._condition = condition
        self._weight = _game_weight(self._gamestate)
    def game_weight(self)->str:                                                 #return how many pieces each color has
        self._weight = _game_weight(self._gamestate)
        return "B: {:} W: {:}".format(self._weight[0],self._weight[1])
    def turn_show(self)->str:                                                   #return the current turn
        show_str = 'Turn: '+ ('W' if self._gamestate.turn == WHITE else 'B')
        return show_str
    def valid_move(self,move:dict)->str:                #return if the specified position is allowed to drop and flip accordingly
        position = [move['row']-1,move['col']-1]
        if is_empty(self._gamestate,position):          #check if the position is empty
            move_result = valid_position(self._gamestate,position)
        else:
            return False
        if move_result[0]:      #move_result[0]is a boolean to determine whether there is a valid direction
            self._gamestate = gamestate_change(self._gamestate,move_result[1],move_result[2])
            self._turn = self._gamestate.turn
            return True
        else:
            return False
    def player_can_move(self)->bool:                #check if the current player can move
        return _player_can_move(self._gamestate)
    def weight_winner(self)->str:                       #check which player is winner by checking the number of pieces
        if self._condition is '>':          #rule for more pieces
            if self._weight[0] > self._weight[1]:
                print_str = 'WINNER: BLACK'
                winner = BLACK
            elif self._weight[1] > self._weight[0]:
                print_str = 'WINNER: WHITE'
                winner = WHITE
            else:
                print_str = 'WINNER: NONE'
                winner = 3
        elif self._condition is '<':            #rule for less pieces
            if self._weight[0] > self._weight[1]:
                print_str = 'WINNER: WHITE'
                winner = WHITE
            elif self._weight[1] > self._weight[0]:
                print_str = 'WINNER: BLACK'
                winner = BLACK
            else:
                print_str = 'WINNER: NONE'
                winner = 3
        #return print_str
        return winner
    def change_player(self)->None:                      #change player if the current player cannot move
        self._gamestate = _change_player(self._gamestate)


