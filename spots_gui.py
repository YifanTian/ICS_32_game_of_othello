#Yifan Tian Lab 5 ID:78921267

import point
import spots_model
import tkinter
import greetings

WHITE = 1
BLACK = 2

DEFAULT_FONT = ('Helvetica', 20)


class Winner_Dialog:
    '''Winner dialog, print winner information and get command to process afterwards'''
    def __init__(self,winner,root_window):
        self._dialog_window = tkinter.Toplevel()
        self._root_window = root_window

        if winner is 1:
            winner_str = 'WHITE'
        elif winner is 2:
            winner_str = 'BLACK'
        else:
            winner_str = 'None'
        
        who_label = tkinter.Label(
            master = self._dialog_window, text = 'WINNER: '+ winner_str,
            font = DEFAULT_FONT)

        who_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        button_frame = tkinter.Frame(master = self._dialog_window)

        button_frame.grid(
            row = 1, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.S)

        ok_button = tkinter.Button(
            master = button_frame, text = 'Retry', font = DEFAULT_FONT,
            command = self._on_ok_button)

        ok_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        cancel_button = tkinter.Button(
            master = button_frame, text = 'Cancel', font = DEFAULT_FONT,
            command = self._on_cancel_button)

        cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        self._dialog_window.rowconfigure(3, weight = 1)
        self._dialog_window.columnconfigure(1, weight = 1)

        self._afterwards = 0

    def _on_ok_button(self) -> None:
        self._afterwards = 1
        self._dialog_window.destroy()
        self._root_window.destroy()

    def _on_cancel_button(self) -> None:
        self._dialog_window.destroy()

    def _on_retry_button(self) -> None:
        self._dialog_window.destroy()

    def show(self) -> None:
        # This is how we turn control over to our dialog box and make that
        # dialog box modal.
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def afterwards(self):
        return self._afterwards


class SpotsApplication:
    def __init__(self, state: spots_model.SpotsState):
        ''' game class, draw board and print information'''
        self._state = state
        self._root_window = tkinter.Tk()

        self._rows = state._rows
        self._cols = state._cols
        self._topleft = state._topleft
        self._first_player = state._first_player
        self._rule = state._rule
        
        self._info_frame = tkinter.Frame(
            master = self._root_window, background = '')

        self._info_frame.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        self._weights_white = tkinter.Label(
            master = self._info_frame,text = '',
            font = DEFAULT_FONT)
        
        self._weights_white.grid(
            row = 0, column = 0, padx = 40, pady = 10)

        self._weights_black = tkinter.Label(
            master = self._info_frame,textvariable = '',
            font = DEFAULT_FONT)
        self._weights_black.grid(
            row = 0, column = 2, padx = 40, pady = 10,
            sticky = tkinter.E)

        
        self._turn_label = tkinter.Label(
            master = self._info_frame,text = '',
            font = DEFAULT_FONT)
        self._turn_label.grid(
            row = 1, column = 0, padx = 40, pady = 10,
            sticky = tkinter.E)
        
        self._rule_label = tkinter.Label(
            master = self._info_frame,text = '',
            font = DEFAULT_FONT)

        self._rule_label.grid(
            row = 1, column = 2, padx = 40, pady = 10,
            sticky = tkinter.E)

        
        self._canvas = tkinter.Canvas(
            master = self._root_window, width = 600, height = 600,
            background = '#006000')     #change background
        
        self._canvas.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)  #arrangement of widgets
        
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.columnconfigure(0, weight = 2)
        


    def run(self) -> None:
        self._root_window.mainloop()


    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''deal with resize event'''
        self._redraw_all_spots()


    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        '''deal with click event'''
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        click_point = point.from_pixel(
            event.x, event.y, width, height)

        self._state.handle_click(click_point)

        self._redraw_all_spots()
        

    def _redraw_all_spots(self) -> None:
        self._canvas.delete(tkinter.ALL)

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        #print information on tk window
        self._weights_white['text'] = 'WHITE:     {}'.format(self._state._othello._weight[1])
        self._weights_black['text'] = 'BLACK:     {}'.format(self._state._othello._weight[0])                
        self._turn_label['text'] = 'TURN:     {}'.format(self._state._othello.turn_show()[-1])
        self._rule_label['text'] = 'RULE:     {}'.format(self._rule)
        
        #draw pieces 
        for spot in self._state.all_spots():
            center_x, center_y = spot.center().pixel(canvas_width, canvas_height)

            radius_x = spot.radius_frac()[0]*canvas_width
            radius_y = spot.radius_frac()[1]*canvas_height

            if spot._color is WHITE:
                self._canvas.create_oval(
                    center_x - radius_x, center_y - radius_y,
                    center_x + radius_x, center_y + radius_y,
                    fill = 'snow', outline = '#000000')
            elif spot._color is BLACK:
                self._canvas.create_oval(
                    center_x - radius_x, center_y - radius_y,
                    center_x + radius_x, center_y + radius_y,
                    fill = '#000000', outline = '#000000')

        #draw grid on board
        diax = 2*radius_x
        diay = 2*radius_y
        for i in range(self._rows):
            self._canvas.create_line(0,diay*i,canvas_width,diay*i)
        for j in range(self._cols):
            self._canvas.create_line(diax*j,0,diax*j,canvas_height)
        #winner window and get information about how to process afterwards
        if self._state.winner():
            winner_window = Winner_Dialog(self._state.winner(),self._root_window)
            winner_window.show()
            afterwards = winner_window.afterwards()
            if afterwards is 1:
                SpotsApplication(spots_model.SpotsState(self._rows,self._cols,self._first_player,self._topleft,self._rule)).run()
        


