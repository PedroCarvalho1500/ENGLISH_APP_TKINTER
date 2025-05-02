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
from pygame import mixer
from pydub import AudioSegment
from pydub.playback import play

BACKGROUND_COLOR = "#272426"
timer = None
current_french_word = ""




class ScreenFunctions():
    def __init__(self):
        pass

    def openMainPage(self):
        self.pronunciation_window.destroy()
        main_menu = Tk()
        new_screen = main.Application(main_menu)


class DB_Actions():
    def __init__(self):
        pass

    def connect_db(self):
        self.conn = sqlite3.connect("instance/english.db")
        self.cursor = self.conn.cursor()

            
    def disconnect_db(self):
        #print("DATABASE DISCONNECTED!!!")
        self.conn.close()

    def get_complete_example(self,id):
        self.connect_db()

        #print("GETTING EXAMPLE BY ID -> "+str(id))
        eg = self.cursor.execute(""" SELECT * FROM pronunciation WHERE id=?""", [id]).fetchall()
        self.conn.commit()

        self.disconnect_db()

        return eg   


    def get_audio_by_id(self,id):
        self.connect_db()

        #print("GETTING EXAMPLE BY ID -> "+str(id))
        eg = self.cursor.execute(""" SELECT * FROM pronunciation WHERE id=?""", [id]).fetchall()
        self.conn.commit()

        self.disconnect_db()

        return eg[2]
    
    def get_word_by_id(self,id):
        self.connect_db()

        #print("GETTING EXAMPLE BY ID -> "+str(id))
        eg = self.cursor.execute(""" SELECT * FROM pronunciation WHERE id=?""", [id]).fetchall()
        self.conn.commit()

        self.disconnect_db()
        return eg[0][1]
    
    def get_audio(self,id):
        self.connect_db()

        audio = self.cursor.execute(""" SELECT * FROM pronunciation WHERE id=?""", [id]).fetchall()
        return audio[0][2]


    def get_number_of_rows(self):
        self.connect_db()

        number = int(self.cursor.execute("""SELECT COUNT(*) FROM pronunciation;""").fetchone()[0])
        return number

    def get_meaning(self,id):
        self.connect_db()
        meaning = self.cursor.execute(""" SELECT * FROM pronunciation WHERE id=?""", [id]).fetchall()
        self.conn.commit()

        self.disconnect_db()
        return meaning[0][3]
    


class Application(ScreenFunctions):
    def __init__(self, window):
        mixer.init()
        self.ask_for_start_point()
        self.pronunciation_window = window
        icon = main.InsertIcon(self.pronunciation_window)
        self.db_obj = DB_Actions()
        self.pronunciation_window.title("PRONUNCIATION WINDOW")
        self.pronunciation_window.config(background=BACKGROUND_COLOR, height=728, width=1200)
        self.pronunciation_window.resizable(True,True)
        self.id = 1
        self.current_word = self.get_current_word(self.id)
        self.complete_example = self.get_complete_example(self.id)
        self.current_meaning = self.get_current_meaning(self.id)
        self.number_rows = self.db_obj.get_number_of_rows()
        self.load_card()
        self.load_buttons()
        
        
        self.pronunciation_window.mainloop()

 
    def validate_input(input_str,pattern):
        if re.match(pattern, input_str):
            return True
        else:
             return False
            
            
    def ask_for_start_point(self):
        #while True:
        self.USER_INP = simpledialog.askstring(title="Enter the Starting point for Random",prompt="From which point do you want to start choosing randomly?")
            #if self.USER_INP and self.validate_input(self.USER_INP,pattern='^([\s\d]+)$'):
            #    return self.USER_INP
            #else:
            #    print("Invalid input. Please try again.")

        

    def refresh_front_card(self):
        self.flashcard_canvas.itemconfig(self.image_front, image=self.my_flashcard_image)
        self.flashcard_canvas.itemconfig(self.canvas_example,text="Word",font=("Arial", 30, 'italic'))
        self.flashcard_canvas.itemconfig(self.meaning_text,text=self.current_meaning,font=("Arial", 12, 'italic'))

    def next_eg(self,event=None):


        if self.id == (self.number_rows):
            self.id = 1
            self.complete_example = self.get_complete_example(self.id)
            self.current_word = self.get_current_word(self.id)
            self.current_meaning = self.get_current_meaning(self.id)
            self.flashcard_canvas.itemconfig(self.canvas_text, text=str(self.current_word))
            self.refresh_front_card()
            
        
        else:
            self.id+=1
            self.complete_example = self.get_complete_example(self.id)
            self.current_word = self.get_current_word(self.id)
            self.current_meaning = self.get_current_meaning(self.id)
            self.flashcard_canvas.itemconfig(self.canvas_text, text=str(self.current_word))
            self.refresh_front_card()


    def previous_eg(self,event=None):
        if self.id == 1:

            self.id = self.number_rows
            self.complete_example = self.get_complete_example(self.id)
            self.current_word = self.get_current_word(self.id)
            self.current_meaning = self.get_current_meaning(self.id)
            self.flashcard_canvas.itemconfig(self.canvas_text, text=str(self.current_word))
            self.refresh_front_card()
        
        else:
            self.id-=1
            self.complete_example = self.get_complete_example(self.id)
            self.current_word = self.get_current_word(self.id)
            self.current_meaning = self.get_current_meaning(self.id)
            self.flashcard_canvas.itemconfig(self.canvas_text, text=str(self.current_word))
            self.refresh_front_card()

    def random_eg(self,event=None):
        self.id = random.randint(int(self.USER_INP),int(self.USER_INP)+100)
        if self.id > self.number_rows: self.id = self.number_rows
        self.complete_example = self.get_complete_example(self.id)
        self.current_word = self.get_current_word(self.id)
        self.current_meaning = self.get_current_meaning(self.id)
        self.flashcard_canvas.itemconfig(self.canvas_text, text=str(self.current_word))
        self.refresh_front_card()


    def play_audio(self,id,event=None):
        sound_to_play = self.get_sound(id)
        song = AudioSegment.from_file(io.BytesIO(sound_to_play), format="mp3")
        song.export('audio.mp3')
        mixer.music.load('audio.mp3')
        mixer.music.play(loops=1)
        try:
            os.system('rm -rf audio.mp3')
        except:
            os.system('del audio.mp3')


    def load_buttons(self):
        self.previous_button_image= PhotoImage(file='images/back_button.png')
        self.previous_button= Button(self.pronunciation_window, image=self.previous_button_image,command= lambda: self.previous_eg(), borderwidth=0)
        self.previous_button.place(relx=0.43, rely=0.7999, relheight=0.099, relwidth=0.04)

        self.forward_button_image= PhotoImage(file='images/forward.png')
        self.forward_button= Button(self.pronunciation_window, image=self.forward_button_image,command= lambda: self.next_eg(), borderwidth=0)
        self.forward_button.place(relx=0.589, rely=0.7999, relheight=0.099, relwidth=0.04)

        self.random_button_image= PhotoImage(file='images/levantando-a-mao-para-a-pergunta.png')
        self.random_button= Button(self.pronunciation_window, image=self.random_button_image,command= lambda: self.random_eg(), borderwidth=0)
        self.random_button.place(relx=0.001, rely=0.001, relheight=0.8, relwidth=0.23)

        self.play_audio_image= PhotoImage(file='images/play_audio.png', width=60, height=60)
        self.see_answer = Button(self.pronunciation_window,text='Play Audio', border=2, image=self.play_audio_image, activebackground='#108ecb' ,activeforeground='white', command=lambda: self.play_audio(self.complete_example[0][0]))
        self.see_answer.place(relx=0.5, rely=0.8)

        self.back_button = Button(self.pronunciation_window,text='Back to Menu', border=2, bg="#CC1705", font=('verdana', 10, 'bold'), activebackground='#108ecb' ,activeforeground='white', command=self.openMainPage)
        self.back_button.place(relx=0.43, rely=0.9, relwidth=0.2, relheight=0.1)

        self.pronunciation_window.bind('<Right>', self.next_eg)
        self.pronunciation_window.bind('<Left>', self.previous_eg)
        self.pronunciation_window.bind('<space>', lambda event: self.play_audio(self.complete_example[0][0]))


    def load_card(self):
        self.flashcard_canvas = Canvas(width=800, height=518, background=BACKGROUND_COLOR, highlightthickness=0)
        #self.flashcard_canvas = Canvas(self.pronunciation_window,background='white', highlightthickness=0)
        self.my_flashcard_image = PhotoImage(file="images/card_front.png")
        self.new_image = PhotoImage(file="images/card_back.png")

        #print(self.current_eg)

        self.image_front = self.flashcard_canvas.create_image(400,270,image=self.my_flashcard_image)
        self.canvas_text = self.flashcard_canvas.create_text(400,263,text=str(self.current_word),font=("Arial", 26, 'bold'))
        self.canvas_example = self.flashcard_canvas.create_text(400,80,text="Word",font=("Arial", 30, 'italic'))
        self.meaning_text = self.flashcard_canvas.create_text(400,420,text=self.current_meaning,font=("Arial", 12, 'italic'))
        self.flashcard_canvas.place(relx=0.25, rely=0.07, relwidth=0.8, relheight=0.8)

    def get_current_meaning(self,id):
        obj = self.db_obj.get_meaning(id)
        return obj


    def get_current_word(self,id):
        obj = self.db_obj.get_word_by_id(id)
        return obj

    def get_complete_example(self,id):
        obj = self.db_obj.get_complete_example(id)
        return obj

    def get_sound(self,id):
        obj = self.db_obj.get_audio(id)
        return obj


if __name__ == '__main__':
    new_window = Tk()
    Application(new_window)

    