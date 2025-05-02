import sqlite3
import time
from tkinter import *
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText

import random
import main
import requests

BACKGROUND_COLOR = "#403E3E"
timer = None
current_french_word = ""

time_passed = 0
folders_created = []



class ScreenFunctions():
    def __init__(self):
        pass

    def openMainPage(self):
        self.vocabulary_window.destroy()
        main_menu = Tk()
        new_screen = main.Application(main_menu)


class DB_Actions():
    def __init__(self):
        pass



class Application(ScreenFunctions):
    def __init__(self, window):
        self.vocabulary_window = window
        self.db_obj = DB_Actions()
        self.vocabulary_window.title("ENGLISH APP")
        self.vocabulary_window.config(background=BACKGROUND_COLOR, height=728, width=1200)
        self.vocabulary_window.resizable(False,False)
        icon = main.InsertIcon(self.vocabulary_window)
        self.load_text_area()
        self.load_input_field()
        self.load_buttons()
        #translation = requests.get(url='https://api.dictionaryapi.dev/api/v2/entries/en/'+str('write')).json()[0]["meanings"]
        #for definition in translation:
        #    print(str(definition["definitions"][0]["definition"]))
        self.vocabulary_window.mainloop()


    def find_meanings(self):
        word_to_search = (str(self.input_word.get()))
        self.input_word.delete(0, 'end')
        try:
            translation = requests.get(url='https://api.dictionaryapi.dev/api/v2/entries/en/'+word_to_search).json()[0]["meanings"]
        except:
            translation = ""
        
        
        self.textarea.config(state=NORMAL)
        self.textarea.delete('1.0', END)
        for definitions in translation:
            self.textarea.insert(INSERT, "--------------------------------"+str(definitions["partOfSpeech"]).upper()+"--------------------------------"+"\n")
            for definition in definitions["definitions"]:
                self.textarea.insert(INSERT, str(definition["definition"])+"\n")
                try:
                    self.textarea.insert(INSERT, "SENTENCE: "+str(definition["example"])+"\n")
                    self.textarea.insert(INSERT,"\n\n")
                except:
                    pass
            self.textarea.insert(INSERT,"\n\n\n")



    def load_text_area(self):
        self.textarea = ScrolledText(self.vocabulary_window,foreground='black',background="#F8F3EA")
        self.textarea.config(state=DISABLED)
        self.textarea.place(relx=0.007, rely=0.09, relwidth=0.98, relheight=0.65)
        


    def load_input_field(self):
        self.input_word = Entry(text='Type your word here')
        self.input_word.place(relx=0.38, rely=0.78, relwidth=0.3, relheight=0.04)


    def load_buttons(self):
        self.search_for_meaning_button = Button(self.vocabulary_window,text='Search', border=2, bg="#CC1705", font=('verdana', 10, 'bold'), activebackground='#108ecb' ,activeforeground='white', command=self.find_meanings)
        self.search_for_meaning_button.place(relx=0.43, rely=0.85, relwidth=0.2, relheight=0.05)
        self.back_button = Button(self.vocabulary_window,text='Back to Menu', border=2, bg="#CC1705", font=('verdana', 10, 'bold'), activebackground='#108ecb' ,activeforeground='white', command=self.openMainPage)
        self.back_button.place(relx=0.43, rely=0.95, relwidth=0.2, relheight=0.05)




if __name__ == '__main__':
    new_window = Tk()
    Application(new_window)

    