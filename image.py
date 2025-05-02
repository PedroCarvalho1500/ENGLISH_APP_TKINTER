import sqlite3
import time
from tkinter import *
import tkinter.messagebox
import random
import main
from PIL import Image, ImageTk
import io

BACKGROUND_COLOR = "#272426"
timer = None
current_french_word = ""

time_passed = 0


class ScreenFunctions():
    def __init__(self):
        pass

    def openMainPage(self):
        self.images_window.destroy()
        main_menu = Tk()
        new_screen = main.Application(main_menu)


class DB_Actions():
    def __init__(self):
        pass

    def connect_db(self):
        self.conn = sqlite3.connect("instance/english.db")
        self.cursor = self.conn.cursor()

            
    def disconnect_db(self):
        print("DATABASE DISCONNECTED!!!")
        self.conn.close()

    def get_eg_by_id(self,id):
        self.connect_db()
        eg = self.cursor.execute(""" SELECT * FROM image WHERE id=?""", [id]).fetchall()
        self.conn.commit()
        #input("EXAMPLE FOUND -> "+str(eg))

        self.disconnect_db()

        return eg
    
    def get_number_of_rows(self):
        self.connect_db()

        number = int(self.cursor.execute("""SELECT COUNT(*) FROM image;""").fetchone()[0])
        return number


class Application(ScreenFunctions):
    def __init__(self, window):
        self.images_window = window
        self.db_obj = DB_Actions()
        self.images_window.title("IMAGE SCREEN")
        self.images_window.config(background=BACKGROUND_COLOR, height=728, width=1200)
        self.images_window.resizable(False,False)
        self.id = 1
        self.current_eg = self.get_current_eg(self.id)
        self.number_rows = self.db_obj.get_number_of_rows()
        self.current_image = self.db_obj.get_eg_by_id(self.id)
        self.current_image = Image.open(io.BytesIO(self.current_image[0][1]))
        self.load_card()
        self.load_buttons()
        self.images_window.mainloop()


    def refresh_front_card(self):
        self.current_image = self.db_obj.get_eg_by_id(self.id)
        self.current_image = Image.open(io.BytesIO(self.current_image[0][1]))
        self.img_tk = ImageTk.PhotoImage(self.current_image)
        self.flashcard_canvas.itemconfig(self.image_front, image=self.img_tk)
        self.flashcard_canvas.coords(self.image_front, 230,40)
        self.flashcard_canvas.itemconfig(self.canvas_text, text="")
        


    def next_eg(self):
        if self.id == self.number_rows:
            tkinter.messagebox.showinfo("MAX NUMBER REACHED",  "This is the last Exercise!")
        
        else:
            self.id+=1
            self.current_eg = self.get_current_eg(self.id)
            self.refresh_front_card()


    def previous_eg(self):
        if self.id == 1:
            tkinter.messagebox.showinfo("MINIMUM NUMBER REACHED",  "This is the First Exercise!")
        
        else:
            self.id-=1
            self.current_eg = self.get_current_eg(self.id)
            self.refresh_front_card()


    def random_eg(self,event=None):
        self.id = random.randint(1,self.number_rows)
        self.current_eg = self.get_current_eg(self.id)
        self.refresh_front_card()


    def load_buttons(self):
        self.previous_button_image= PhotoImage(file='images/back_button.png', width=35, height=38)
        self.previous_button= Button(self.images_window, image=self.previous_button_image,command= lambda: self.previous_eg(), borderwidth=0)
        self.previous_button.place(relx=0.4, rely=0.8178)

        self.forward_button_image= PhotoImage(file='images/forward.png', width=35, height=38)
        self.forward_button= Button(self.images_window, image=self.forward_button_image,command= lambda: self.next_eg(), borderwidth=0)
        self.forward_button.place(relx=0.63, rely=0.8178)

        self.random_button_image= PhotoImage(file='images/levantando-a-mao-para-a-pergunta.png')
        self.random_button= Button(self.images_window, image=self.random_button_image,command= lambda: self.random_eg(), borderwidth=0)
        self.random_button.place(relx=0.001, rely=0.001, relheight=0.8, relwidth=0.15)

        self.see_answer = Button(self.images_window,text='Check Answer', border=2, bg="#CC1705", font=('verdana', 12, 'bold'), activebackground='#108ecb' ,activeforeground='white', command=lambda: self.change_to_back_card(self.flashcard_canvas,self.images_window,self.new_image))
        self.see_answer.place(relx=0.43, rely=0.8, relwidth=0.2, relheight=0.1)

        self.back_button = Button(self.images_window,text='Back to Menu', border=2, bg="#CC1705", font=('verdana', 10, 'bold'), activebackground='#108ecb' ,activeforeground='white', command=self.openMainPage)
        self.back_button.place(relx=0.43, rely=0.9, relwidth=0.2, relheight=0.1)


    def load_card(self):
        self.flashcard_canvas = Canvas(width=600, height=400, background=BACKGROUND_COLOR, highlightthickness=0)
        self.new_image = PhotoImage(file="images/card_back.png")
        #self.canvas_text = self.flashcard_canvas.create_text(80,80,text="",font=("Arial", 34, 'bold'))
        self.img_tk = ImageTk.PhotoImage(self.current_image)
        self.image_front = self.flashcard_canvas.create_image(230,40,anchor='nw', image=self.img_tk)
        self.flashcard_canvas.place(relx=0.11, rely=0.01, relwidth=0.8, relheight=0.8)
        self.canvas_text = self.flashcard_canvas.create_text(470,233,text="",font=("Times New Roman", 72, 'bold'))


    def change_to_back_card(self,canvas, window, new_image):
        canvas.itemconfig(self.image_front, image=new_image)
        canvas.coords(self.image_front, 90,40)
        
        canvas.itemconfig(self.canvas_text, text=str(self.current_eg[0][2]))
        

    def get_current_eg(self,id):
        obj = self.db_obj.get_eg_by_id(id)
        return obj


if __name__ == '__main__':
    new_window = Tk()
    Application(new_window)

    