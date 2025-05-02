import sqlite3
import time
from tkinter import *
import tkinter.messagebox
import random
import main

BACKGROUND_COLOR = "#272426"
timer = None
current_french_word = ""

time_passed = 0


class ScreenFunctions():
    def __init__(self):
        pass

    def openMainPage(self):
        self.grammar_window.destroy()
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

        #print("GETTING EXAMPLE BY ID -> "+str(id))
        eg = self.cursor.execute(""" SELECT * FROM grammar WHERE id=?""", [id]).fetchall()
        self.conn.commit()
        #input("EXAMPLE FOUND -> "+str(eg))

        self.disconnect_db()

        return eg
    
    def get_number_of_rows(self):
        self.connect_db()

        number = int(self.cursor.execute("""SELECT COUNT(*) FROM grammar;""").fetchone()[0])
        return number


class Application(ScreenFunctions):
    def __init__(self, window):
        self.grammar_window = window
        self.db_obj = DB_Actions()
        self.grammar_window.title("ENGLISH APP")
        self.grammar_window.config(background=BACKGROUND_COLOR, height=728, width=1200)
        self.grammar_window.resizable(True,True)
        self.id = 1
        self.current_eg = self.get_current_eg(self.id)
        self.number_rows = self.db_obj.get_number_of_rows()
        self.load_card()
        self.load_buttons()
        self.grammar_window.mainloop()


    def refresh_front_card(self):
        self.flashcard_canvas.itemconfig(self.image_front, image=self.my_flashcard_image)
        self.flashcard_canvas.itemconfig(self.canvas_example,text="Exercise",font=("Arial", 30, 'italic'))


    def next_eg(self):
        if self.id == self.number_rows:
            tkinter.messagebox.showinfo("MAX NUMBER REACHED",  "This is the last Exercise!")
        
        else:
            self.id+=1
            self.current_eg = self.get_current_eg(self.id)
            self.refresh_front_card()
            self.flashcard_canvas.itemconfig(self.canvas_text, text=str(self.current_eg[0][1]))


    def previous_eg(self):
        if self.id == 1:
            tkinter.messagebox.showinfo("MINIMUM NUMBER REACHED",  "This is the First Exercise!")
        
        else:
            self.id-=1
            self.current_eg = self.get_current_eg(self.id)
            self.refresh_front_card()
            self.flashcard_canvas.itemconfig(self.canvas_text, text=str(self.current_eg[0][1]))

    # def create_button(self,name, screen, text, border, bg, font, activebackground ,activeforeground, command, x, y):
    #     name = Button(screen, text=text, border=border, bg=bg, font=font, activebackground=activebackground ,activeforeground=activeforeground, command=lambda: command())
    #     name.place(relx=x, rely=y, relwidth=0.2, relheight=0.1)
    #     buttons_list.append(name)
    #     #input(f'{buttons_list}')
    #     return name

    def load_buttons(self):
        self.previous_button_image= PhotoImage(file='images/back_button.png', width=35, height=38)
        self.previous_button= Button(self.grammar_window, image=self.previous_button_image,command= lambda: self.previous_eg(), borderwidth=0)
        self.previous_button.place(relx=0.4, rely=0.8178)

        self.forward_button_image= PhotoImage(file='images/forward.png', width=35, height=38)
        self.forward_button= Button(self.grammar_window, image=self.forward_button_image,command= lambda: self.next_eg(), borderwidth=0)
        self.forward_button.place(relx=0.63, rely=0.8178)

        self.see_answer = Button(self.grammar_window,text='Check Answer', border=2, bg="#CC1705", font=('verdana', 12, 'bold'), activebackground='#108ecb' ,activeforeground='white', command=lambda: self.change_to_back_card(self.flashcard_canvas,self.grammar_window,self.new_image))
        self.see_answer.place(relx=0.43, rely=0.8, relwidth=0.2, relheight=0.1)

        self.back_button = Button(self.grammar_window,text='Back to Menu', border=2, bg="#CC1705", font=('verdana', 10, 'bold'), activebackground='#108ecb' ,activeforeground='white', command=self.openMainPage)
        self.back_button.place(relx=0.43, rely=0.9, relwidth=0.2, relheight=0.1)


    def load_card(self):
        self.flashcard_canvas = Canvas(width=800, height=518, background=BACKGROUND_COLOR, highlightthickness=0)
        self.my_flashcard_image = PhotoImage(file="images/card_front.png")
        self.new_image = PhotoImage(file="images/card_back.png")

        #print(self.current_eg)

        self.image_front = self.flashcard_canvas.create_image(400,270,image=self.my_flashcard_image)
        self.canvas_text = self.flashcard_canvas.create_text(400,263,text=str(self.current_eg[0][1]),font=("Arial", 16, 'bold'))
        self.canvas_example = self.flashcard_canvas.create_text(400,80,text="Exercise",font=("Arial", 30, 'italic'))
        self.flashcard_canvas.place(relx=0.19, rely=0.07, relwidth=0.8, relheight=0.8)

    def change_to_back_card(self,canvas, window, new_image):
        canvas.itemconfig(self.image_front, image=new_image)
        canvas.itemconfig(self.canvas_text, text=str(self.current_eg[0][2]))
        canvas.itemconfig(self.canvas_example, text=str(self.current_eg[0][3]),font=("Arial", 16, 'italic'))

    def get_current_eg(self,id):
        obj = self.db_obj.get_eg_by_id(id)
        return obj


if __name__ == '__main__':
    new_window = Tk()
    Application(new_window)

    