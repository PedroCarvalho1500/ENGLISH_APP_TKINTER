import io
import os
import re
import sqlite3
import time
from tkinter import *
from tkinter import simpledialog
import tkinter.messagebox
import random
import main
import phraseSpecific

BACKGROUND_COLOR = "black"
timer = None
current_french_word = ""




buttons_list = []

class ScreenFunctions():
    def __init__(self):
        pass

    def openMainPage(self):
        self.phrases.destroy()
        main_menu = Tk()
        new_screen = main.Application(main_menu)
    
    def openPhrasePage(self,buttonValue):
        self.phrases.destroy()
        phrasePage = Tk()
        db_action = DB_Actions()
        #print(buttonValue)
        verb_id = db_action.getVerbIdByWord(buttonValue)
        new_screen = phraseSpecific.Application(phrasePage,verb_id)

class DB_Actions():
    def __init__(self):
        pass

    def connect_db(self):
        self.conn = sqlite3.connect("instance/english.db")
        self.cursor = self.conn.cursor()

            
    def disconnect_db(self):
        #print("DATABASE DISCONNECTED!!!")
        self.conn.close()

    def get_all_verbs(self):
        self.connect_db()

        #print("GETTING EXAMPLE BY ID -> "+str(id))
        eg = self.cursor.execute(""" SELECT * FROM verbs ORDER BY word""").fetchall()
        self.conn.commit()

        self.disconnect_db()

        return eg   

    def getVerbIdByWord(self,name):
        self.connect_db()

        #print("GETTING EXAMPLE BY ID -> "+str(id))
        eg = self.cursor.execute(""" SELECT * FROM verbs WHERE word=?""",[name]).fetchall()
        self.conn.commit()

        self.disconnect_db()

        return eg[0]

    def get_verb_by_id(self,id):
        self.connect_db()

        eg = self.cursor.execute(""" SELECT * FROM verbs WHERE id=?""", [id]).fetchall()
        self.conn.commit()

        self.disconnect_db()

        return eg


    def get_number_of_rows(self):
        self.connect_db()

        number = int(self.cursor.execute("""SELECT COUNT(*) FROM verbs;""").fetchone()[0])
        return number

    


class Application(ScreenFunctions):
    def __init__(self, window):
        self.phrases = window
        width = 1500
        height = 728
        x_position = 100
        y_position = 150
        self.phrases.geometry(f"{width}x{height}+{x_position}+{y_position}")
        icon = main.InsertIcon(self.phrases)
        self.db_obj = DB_Actions()
        self.phrases.title("PHRASES WINDOW")
        self.phrases.config(background=BACKGROUND_COLOR)
        self.phrases.resizable(True,True)
        self.id = 1
        self.number_rows = self.db_obj.get_number_of_rows()
        self.load_buttons()
        
        
        self.phrases.mainloop()

    def create_button(self,name, screen, text, border, bg, font, activebackground ,activeforeground, command, x, y):
        name = Button(screen, text=text, border=border, bg="white", font=font, activebackground="green" ,activeforeground="black", command=lambda: self.openPhrasePage(text))
        name.place(relx=x, rely=y, relwidth=0.06, relheight=0.08)
        buttons_list.append(name)
        
        #input(f'{buttons_list}')
        return name


    def load_buttons(self):
        x = 0.02
        y = 0.001
        index = 0
        
        buttons_titles = (i[1] for i in self.db_obj.get_all_verbs())
        #print(buttons_titles)

        for folder in buttons_titles:
            #input("FOLDER -> "+str(folder))
            #folders_created.append(folder)
            self.create_button(folder, self.phrases, folder, 2, "black", ('verdana', 10, 'bold'), 'white' ,'white', str(folder),x,y)
            
            x+=0.07
            if(x >= 0.94):
                x = 0.02
                y+=0.06
            index+=1

        #input(f"CREATING BACK")
        self.bt_main_menu = Button(self.phrases, text="Main Menu", border=2, bg="white", font=('verdana', 10, 'bold'), activebackground='green' ,activeforeground='black', command=lambda: self.openMainPage())
        self.bt_main_menu.place(relx=0.25,rely=0.86, relwidth=0.37, relheight=0.1)
        
        #DELETE LINE BELOW IF SOME PROBLEM APPEARS.
        buttons_list.append(self.bt_main_menu)



if __name__ == '__main__':
    new_window = Tk()
    Application(new_window)

    