import io
import os
import re
import sqlite3
import time
from tkinter import *
from tkinter import simpledialog
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText

import random
import main
from pygame import mixer
from pydub import AudioSegment
from pydub.playback import play
import phrases

BACKGROUND_COLOR = "#272426"
timer = None
current_french_word = ""




class ScreenFunctions():
    def __init__(self):
        pass

    def openPhrases(self):
        self.specific_phrases.destroy()
        main_menu = Tk()
        new_screen = phrases.Application(main_menu)


class DB_Actions():
    def __init__(self):
        pass

    def connect_db(self):
        self.conn = sqlite3.connect("instance/english.db")
        self.cursor = self.conn.cursor()

            
    def disconnect_db(self):
        #print("DATABASE DISCONNECTED!!!")
        self.conn.close()

    def get_all_preps_with_verb(self,verb_id):
        self.connect_db()

        #print("GETTING EXAMPLE BY ID -> "+str(id))
        eg = self.cursor.execute("""SELECT DISTINCT prepositions.word,verb_prep.meaning FROM verb_prep 
                                    INNER JOIN prepositions
                                    INNER JOIN verbs ON verb_prep.verb_id = ? AND verb_prep.prep_id = prepositions.id;""",[verb_id]).fetchall()
        
        self.conn.commit()

        self.disconnect_db()
        #print(eg)
        return eg   
    


class Application(ScreenFunctions):
    def __init__(self, window, verb_list):
        mixer.init()
        self.specific_phrases = window
        self.specific_phrases = window
        width = 1200
        height = 728
        x_position = 100
        y_position = 150
        self.specific_phrases.geometry(f"{width}x{height}+{x_position}+{y_position}")
        icon = main.InsertIcon(self.specific_phrases)
        self.db_obj = DB_Actions()
        self.verb_list = verb_list
        self.specific_phrases.title("PHRASES FOR VERB "+str(self.verb_list[1])+" WINDOW")
        self.specific_phrases.config(background=BACKGROUND_COLOR)
        self.specific_phrases.resizable(True,True)
        self.specific_phrases.x_position = 1200

        self.load_text_area()
        self.load_buttons()
        self.fill_up_text_area()
        
        
        self.specific_phrases.mainloop()

    def load_text_area(self):
        F_font = ('bold', 30)
        self.textarea = ScrolledText(self.specific_phrases,foreground='black',background="#F8F3EA",font=F_font)
        self.textarea.config(state=DISABLED)
        self.textarea.place(relx=0.007, rely=0.09, relwidth=0.98, relheight=0.65)

    def load_buttons(self):
        self.back_button = Button(self.specific_phrases,text='Back to Phrases', border=2, bg="#CC1705", font=('verdana', 10, 'bold'), activebackground='#108ecb' ,activeforeground='white', command=self.openPhrases)
        self.back_button.place(relx=0.43, rely=0.95, relwidth=0.2, relheight=0.05)

    def fill_up_text_area(self):

        all_phrases = self.db_obj.get_all_preps_with_verb(self.verb_list[0])
        #print(all_phrases)
        self.textarea.config(state=NORMAL)
        for i in all_phrases:
            self.textarea.insert(INSERT, i[0]+" -> "+i[1]+"\n\n\n")
        self.textarea.config(state=DISABLED)
        

if __name__ == '__main__':
    new_window = Tk()
    Application(new_window)

    