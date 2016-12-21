#Yifan Tian ID 78921267


import tkinter
import spots_gui
import spots_model


DEFAULT_FONT = ('Helvetica', 18)

class NameDialog:
    '''Get game setup information from here'''
    def __init__(self):
        self._dialog_window = tkinter.Toplevel()

        setup_label = tkinter.Label(
            master = self._dialog_window, text = 'Setup for Othello',
            font = DEFAULT_FONT)

        setup_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.S)

        #rows option menu
        rows_label = tkinter.Label(
            master = self._dialog_window, text = 'Rows:',
            font = DEFAULT_FONT)

        rows_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        self._rows_val = tkinter.StringVar(self._dialog_window)
        self._rows_val.set('4')
        self._rows_option = tkinter.OptionMenu(self._dialog_window,self._rows_val,'4','6','8','10','12','14','16')
        self._rows_option.grid(row = 1,column = 1,sticky = tkinter.W + tkinter.E)

        #columns option menu
        cols_label = tkinter.Label(
            master = self._dialog_window, text = 'Columns:',
            font = DEFAULT_FONT)

        cols_label.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        self._cols_val = tkinter.StringVar(self._dialog_window)
        self._cols_val.set('4')
        self._cols_option = tkinter.OptionMenu(self._dialog_window,self._cols_val,'4','6','8','10','12','14','16')
        self._cols_option.grid(row = 2,column = 1,sticky = tkinter.W + tkinter.E)

        #button for first player information
        first_player_label = tkinter.Label(
            master = self._dialog_window, text = 'First_player:',
            font = DEFAULT_FONT)

        first_player_label.grid(
            row = 3, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.fpvar = tkinter.IntVar()               #first player
        radiobutton_frame1 = tkinter.Frame(master = self._dialog_window)
        radiobutton_frame1.grid(
            row = 3, column = 1, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._first_player_Radiobutton1 = tkinter.Radiobutton(
            master = radiobutton_frame1, text = 'White',value = 1,variable = self.fpvar)
        
        self._first_player_Radiobutton1.grid(
            row = 0, column = 0, padx = 5, pady = 1,
            sticky = tkinter.W )

        self._first_player_Radiobutton2 = tkinter.Radiobutton(
            master = radiobutton_frame1, text = 'Black',value = 2, variable = self.fpvar)

        self._first_player_Radiobutton2.grid(
            row = 0, column = 1, padx = 5, pady = 1,
            sticky = tkinter.W )

        #button for topleft player information
        topleft_player_label = tkinter.Label(
            master = self._dialog_window, text = 'Topleft_player:',
            font = DEFAULT_FONT)

        topleft_player_label.grid(
            row = 4, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.tlvar = tkinter.IntVar()             #topleft player
        radiobutton_frame2 = tkinter.Frame(master = self._dialog_window)
        radiobutton_frame2.grid(
            row = 4, column = 1, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._topleft_player_Radiobutton1 = tkinter.Radiobutton(
            master = radiobutton_frame2, text = 'White',value = 1,variable = self.tlvar)
        
        self._topleft_player_Radiobutton1.grid(
            row = 0, column = 0, padx = 5, pady = 1,
            sticky = tkinter.W )

        self._topleft_player_Radiobutton2 = tkinter.Radiobutton(
            master = radiobutton_frame2, text = 'Black',value = 2, variable = self.tlvar)

        self._topleft_player_Radiobutton2.grid(
            row = 0, column = 1, padx = 5, pady = 1,
            sticky = tkinter.W )

        #button for rule information
        rule_label = tkinter.Label(
            master = self._dialog_window, text = 'Rule:',
            font = DEFAULT_FONT)

        rule_label.grid(
            row = 5, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self.rule_var = tkinter.IntVar()

        radiobutton_frame3 = tkinter.Frame(master = self._dialog_window)
        radiobutton_frame3.grid(
            row = 5, column = 1, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._rule_Radiobutton = tkinter.Radiobutton(
            master = radiobutton_frame3, text = '>',value = 1,variable = self.rule_var)
        
        self._rule_Radiobutton.grid(
            row = 0, column = 0, padx = 5, pady = 1,
            sticky = tkinter.W )

        self._rule_Radiobutton = tkinter.Radiobutton(
            master = radiobutton_frame3, text = '<',value = 2, variable = self.rule_var)

        self._rule_Radiobutton.grid(
            row = 0, column = 1, padx = 5, pady = 1,
            sticky = tkinter.W )
                

        #button for confirm
        button_frame = tkinter.Frame(master = self._dialog_window)

        button_frame.grid(
            row = 8, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.S)

        ok_button = tkinter.Button(
            master = button_frame, text = 'OK', font = DEFAULT_FONT,
            command = self._on_ok_button)

        ok_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        cancel_button = tkinter.Button(
            master = button_frame, text = 'Cancel', font = DEFAULT_FONT,
            command = self._on_cancel_button)

        cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        self._dialog_window.rowconfigure(3, weight = 1)
        self._dialog_window.columnconfigure(1, weight = 1)

        self._ok_clicked = False
        self._rows = 4
        self._cols = 4
        self._rule = 1
        self._fp = 1
        self._tl = 1


    def show(self) -> None:
        # This is how we turn control over to our dialog box and make that
        # dialog box modal.
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def was_ok_clicked(self) -> bool:
        return self._ok_clicked

    def get_rows(self) -> str:
        return self._rows

    def get_cols(self) -> str:
        return self._cols

    def get_first_player(self) -> str:
        return self._first_player

    def get_topleft(self) -> str:
        return self._topleft

    def get_rule(self) -> str:
        return self._rule

    def get_fp(self) -> int:
        return self._fp

    def get_tl(self) -> int:
        return self._tl


    def _on_ok_button(self) -> None:
        self._ok_clicked = True
        self._rows = 4
        self._cols = 4
        self._rows = self._rows_val.get()
        self._cols = self._cols_val.get()
        self._rule = self.rule_var.get()
        self._fp = self.fpvar.get()
        self._tl = self.tlvar.get()
        self._dialog_window.destroy()


    def _on_cancel_button(self) -> None:
        self._dialog_window.destroy()



class GreetingsApplication:
    '''Greeting interface, start application from here'''
    def __init__(self):
        self._root_window = tkinter.Tk()

        self._cols = 0
        self._rows = 0

        greet_button = tkinter.Button(
            master = self._root_window, text = 'Start Othello', font = DEFAULT_FONT,
            command = self._on_greet)

        greet_button.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.S)


        self._greeting_text = tkinter.StringVar()
        self._greeting_text.set('Not start yet!')

        greeting_label = tkinter.Label(
            master = self._root_window, textvariable = self._greeting_text,
            font = DEFAULT_FONT)

        greeting_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N)

        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)       

    def start(self) -> None:
        self._root_window.mainloop()

    def _on_greet(self) -> None:
        dialog = NameDialog()
        dialog.show()
        #default setup
        fp = dialog.get_fp()
        tl = dialog.get_tl()
        rows = int(dialog.get_rows())
        cols = int(dialog.get_cols())
        rule = ('>' if dialog.get_rule() is 1 else '<')
        if dialog.was_ok_clicked():                     #get setup parameter from dialog
            fp = dialog.get_fp()
            tl = dialog.get_tl()
            rows = int(dialog.get_rows())
            cols = int(dialog.get_cols())
            rule = ('>' if dialog.get_rule() is 1 else '<')
        first_player_str = ('White' if fp == 1 else 'Black')
        topleft_str = ('White' if tl == 1 else 'Black')
        self._greeting_text.set('Setup: Rows:{} Cols:{}  First player: {} Topleft: {}  rule: {}'.format(rows, cols,first_player_str,topleft_str,rule))
        #run othello
        spots_gui.SpotsApplication(spots_model.SpotsState(rows,cols,fp,tl,rule)).run()



if __name__ == '__main__':
    GreetingsApplication().start()
    
