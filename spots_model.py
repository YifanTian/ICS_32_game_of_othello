#Yifan Tian Lab 5 ID:78921267

import point
import logic

WHITE = 1
BLACK = 2


class Spot:
    def __init__(self, center: point.Point, radius_frac_x: float,radius_frac_y: float,color:int):
        '''
        Initialize a newly-created Spot object, given its center
        point (a Point object) and the spot's radius (in
        fractional coordinates).
        '''
        self._center = center
        self._radius_frac_x = radius_frac_x
        self._radius_frac_y = radius_frac_y
        self._color = color


    def center(self) -> point.Point:
        '''
        Returns a Point object representing this Spot's center.
        '''
        return self._center


    def radius_frac(self):
        '''
        Returns the radius of this Spot, in terms of fractional
        coordinates.
        '''
        return (self._radius_frac_x,self._radius_frac_y)

    def color(self):
        return self._color


def grid_position(pointc:point.Point,rows,cols)->'tuple of grid coordinates':
    '''transform x,y pixal information to i,j coordinate of 2D board list'''
    (frac_x,frac_y) = pointc.frac()
    x_int = 1/rows;y_int = 1/cols
    grid_radius = 0.5*x_int
    return (x_int*(int(frac_x/x_int)+0.5),y_int*(int(frac_y/y_int)+0.5),grid_radius)

def spots_state(othello:'2D list')->list:
    '''get information from othello object and transform them to Spot object list to draw on Canvas'''
    board = othello._gamestate.board
    rows = othello._row
    cols = othello._column
    intx = 1/cols; inty = 1/rows
    radius_x = 0.5/cols
    radius_y = 0.5/rows
    spots_list = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is WHITE:
                cx = (j+0.5)*intx; cy = (i+0.5)*inty
                grid_point = point.Point(cx,cy)
                spots_list.append(Spot(grid_point, radius_x,radius_y,WHITE))
            if board[i][j] is BLACK:
                cx = (j+0.5)*intx; cy = (i+0.5)*inty
                grid_point = point.Point(cx,cy)
                spots_list.append(Spot(grid_point, radius_x,radius_y,BLACK))          
    return spots_list
    

def transform(click_point:point.Point,rows,cols)->tuple:
    ''' '''
    (frac_x,frac_y) = click_point.frac()
    inty = 1/rows; intx = 1/cols
    move_x = int(frac_x/intx)+1
    move_y = int(frac_y/inty)+1
    return (move_y,move_x)

class SpotsState:
    def __init__(self,rows,cols,first_player,topleft,rule):
        '''
        Initializes the state of the Spots application.  Initially,
        there are no spots.
        '''
        self._spots = []
        self._first_player = first_player
        self._rows = rows
        self._cols = cols
        self._topleft = topleft
        self._rule = rule
        self._othello = logic.othello(self._rows,self._cols,self._first_player ,self._topleft,self._rule)

        self._spots = spots_state(self._othello)
        self._winner = False      
        

    def all_spots(self) -> [Spot]:
        '''Returns a list of all of the Spot objects that currently exist.'''
        return self._spots

    def winner(self)->'winner player':
        return self._winner


    def handle_click(self, click_point: point.Point) -> None:
        '''
        Handle a click on the given point, first calculate the (i,j) from (x,y)
        then call te othello object to get the new configueration of the game board
        '''
        (move_x,move_y) = transform(click_point,self._rows,self._cols)
        movedic = {'row':move_x,'col':move_y}

        if self._othello.valid_move(movedic):
            self._othello.game_weight()
        if not self._othello.player_can_move():
            self._othello.change_player()
            if not self._othello.player_can_move():
                self._winner = self._othello.weight_winner()

        self._spots = spots_state(self._othello)





        
