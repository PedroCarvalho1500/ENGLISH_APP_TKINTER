import io
import os
import sqlite3
import time
from tkinter import *
import tkinter.messagebox
import random
import main
#Install uninstallable
#pip install pydub
#pip install pygame
#pip install pyaudio
from pygame import mixer
from pydub import AudioSegment
from pydub.playback import play
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText

BACKGROUND_COLOR = "#272426"
timer = None
current_french_word = ""




class ScreenFunctions():
    def __init__(self):
        pass

    def openMainPage(self):
        self.listening_window.destroy()
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

    def get_eg_by_id(self,id):
        self.connect_db()

        eg = self.cursor.execute(""" SELECT * FROM listening WHERE id=?""", [id]).fetchall()
        self.conn.commit()

        self.disconnect_db()

        return eg
    
    def get_number_of_rows(self):
        self.connect_db()

        number = int(self.cursor.execute("""SELECT COUNT(*) FROM listening;""").fetchone()[0])
        return number

    def get_complete_example(self,id):
        self.connect_db()

        eg = self.cursor.execute(""" SELECT * FROM listening WHERE id=?""", [id]).fetchall()
        self.conn.commit()

        self.disconnect_db()

        return eg
    
    def get_audio(self,id):
        self.connect_db()

        audio = self.cursor.execute(""" SELECT * FROM listening WHERE id=?""", [id]).fetchall()
        return audio[0][2]

class Application(ScreenFunctions):
    def __init__(self, window):
        mixer.init()
        self.listening_window = window
        icon = main.InsertIcon(self.listening_window)
        self.db_obj = DB_Actions()
        self.listening_window.title("LISTENING WINDOW")
        self.listening_window.config(background=BACKGROUND_COLOR, height=728, width=1200)
        self.listening_window.resizable(True,True)
        self.id = 1
        self.load_text_area()
        self.complete_example = self.get_complete_example(self.id)
        self.current_eg = self.get_current_eg(self.id)
        self.number_rows = self.db_obj.get_number_of_rows()
        self.load_buttons()
        self.canvas_title()
        self.listening_window.mainloop()

    def load_text_area(self):
        self.textarea = ScrolledText(self.listening_window,foreground='black',background="#F8F3EA")
        self.textarea.config(state=DISABLED)
        self.textarea.place(relx=0.01, rely=0.12, relwidth=0.99, relheight=0.66)

    def refresh_text_area(self):
        self.textarea.config(state=NORMAL)
        self.textarea.delete('1.0', END)
        self.textarea.insert(INSERT, self.complete_example[0][3])
        self.textarea.config(state=DISABLED)

    def canvas_title(self):
        self.flashcard_canvas = Canvas(background='white', highlightthickness=0)
        self.canvas_title_text = self.flashcard_canvas.create_text(540,40,text=str(self.complete_example[0][1]),font=("Arial", 26, 'bold'))
        self.flashcard_canvas.place(relx=0.01, rely=0.01, relheight=0.1, relwidth=0.99)


    def refresh_front_card(self):
        self.flashcard_canvas.itemconfig(self.canvas_title_text, text=str(self.complete_example[0][1]),font=("Arial", 26, 'bold'))
        self.refresh_text_area()

    def next_eg(self,event=None):
        if self.id == (self.number_rows):
            self.id = 1
            self.complete_example = self.get_complete_example(self.id)
            self.refresh_front_card()
            
        
        else:
            self.id+=1
            self.complete_example = self.get_complete_example(self.id)
            self.refresh_front_card()


    def previous_eg(self,event=None):
        if self.id == 1:
            self.id = self.number_rows-1
            self.complete_example = self.get_complete_example(self.id)
            self.refresh_front_card()
        
        else:
            self.id-=1
            self.complete_example = self.get_complete_example(self.id)
            self.refresh_front_card()





    def load_buttons(self):
        self.previous_button_image= PhotoImage(file='images/back_button.png', width=40, height=67)
        self.previous_button= Button(self.listening_window, image=self.previous_button_image,command= lambda: self.previous_eg(), borderwidth=0)
        self.previous_button.place(relx=0.399, rely=0.9)

        self.forward_button_image= PhotoImage(file='images/forward.png', width=40, height=67)
        self.forward_button= Button(self.listening_window, image=self.forward_button_image,command= lambda: self.next_eg(), borderwidth=0)
        self.forward_button.place(relx=0.63, rely=0.9)

        self.play_audio_image= PhotoImage(file='images/play_audio.png', width=60, height=60)
        self.see_answer = Button(self.listening_window,text='Play Audio', border=2, image=self.play_audio_image, activebackground='#108ecb' ,activeforeground='white', command=lambda: self.play_audio(self.complete_example[0][0]))
        self.see_answer.place(relx=0.5, rely=0.79)

        self.back_button = Button(self.listening_window,text='Back to Menu', border=2, bg="#CC1705", font=('verdana', 10, 'bold'), activebackground='#108ecb' ,activeforeground='white', command=self.openMainPage)
        self.back_button.place(relx=0.43, rely=0.9, relwidth=0.2, relheight=0.1)

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


    def get_complete_example(self,id):
        obj = self.db_obj.get_complete_example(id)
        return obj
    
    def get_sound(self,id):
        obj = self.db_obj.get_audio(id)
        return obj


    def get_current_eg(self,id):
        obj = self.db_obj.get_eg_by_id(id)
        self.refresh_text_area()
        return obj


if __name__ == '__main__':
    new_window = Tk()
    Application(new_window)

    