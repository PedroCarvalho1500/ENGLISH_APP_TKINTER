import sqlite3
import time
from tkinter import *
import pandas
import random
import grammar
import vocabulary
import pronunciation
import listening
import image
import phrases

BACKGROUND_COLOR = "#B1DDC6"
timer = None
current_french_word = ""

time_passed = 0
#data_words = pandas.read_csv("data/french_words.csv")
#to_learn = data_words.to_dict(orient="records")
#words_to_learn_data = ""
#words_to_learn_dict_list = to_learn
folders_created = []
buttons_list = []

buttons_titles = ["Grammar", "Reading", "Adverb", "Vocabulary", "Listening", "Preposition", "Pronunciation", "Writing", "Conjunction", "Images", "Noun", "Pronoun", "Idioms", "Adjective", "Interjection", "Phrasal Verbs", "Verb", "Tenses"]



class ScreenFunctions():
    def __init__(self):
        pass

    def openGrammarPage(self):
        #print("ENTERED...")
        self.main_window.destroy()
        grammar_screen = Tk()
        new_screen = grammar.Application(grammar_screen)

    def openVocabularyPage(self):
        self.main_window.destroy()
        vocabulary_screen = Tk()
        new_screen = vocabulary.Application(vocabulary_screen)


    def openPronunciationPage(self):
        self.main_window.destroy()
        pronunciation_screen = Tk()
        new_screen = pronunciation.Application(pronunciation_screen)

    def openListeningPage(self):
        self.main_window.destroy()
        listening_screen = Tk()
        new_screen = listening.Application(listening_screen)


    def openImagePage(self):
        self.main_window.destroy()
        image_screen = Tk()
        new_screen = image.Application(image_screen)

    def openPhrasesPage(self):
        self.main_window.destroy()
        phrases_screen = Tk()
        new_screen = phrases.Application(phrases_screen)


class DB_Actions():
    def __init__(self):
        pass

    def connect_db(self):
        self.conn = sqlite3.connect("instance/english.db")
        self.cursor = self.conn.cursor()

            
    def disconnect_db(self):
        print("DATABASE DISCONNECTED!!!")
        self.conn.close()

    def mountTables(self):
        self.connect_db()
        print("Conectando ao Banco de Dados!")
            
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS grammar (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                example VARCHAR(100) UNIQUE NOT NULL,
                answer VARCHAR(100000) NOT NULL,
                explanation VARCHAR(100000) NOT NULL
                )""")
                
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS pronunciation (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                word VARCHAR(100) UNIQUE NOT NULL,
                audio BLOB NOT NULL,
                meaning VARCHAR(1000) NOT NULL
                )""")

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS listening (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100) NOT NULL,
                audio BLOB NOT NULL,
                transcription VARCHAR(10000000) NOT NULL
                )""")

        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS image (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                image BLOB NOT NULL,
                word VARCHAR(100) NOT NULL
                )""")


        self.conn.commit()
        print("DATABASE CREATED!!!")
        self.disconnect_db()

# def generate_random_french_word():
#     global current_french_word, words_to_learn_data, words_to_learn_dict_list
#     #current_french_word = random.choice(to_learn)
#     #return current_french_word["French"]
#     try:
#         words_to_learn_data = pandas.read_csv("data/words_to_learn.csv")
#         words_to_learn_dict_list = words_to_learn_data.to_dict(orient="records")
#         current_french_word = random.choice(words_to_learn_dict_list)
#         return current_french_word["French"]

#     except FileNotFoundError:
#         df = pandas.DataFrame(to_learn)
#         df.to_csv('data/words_to_learn.csv', index=False)
#         current_french_word = random.choice(to_learn)
#         return current_french_word["French"] 

#     except IndexError:
#         #file = open("data/words_to_learn.csv", mode="w")
#         current_french_word = random.choice(to_learn)
#         return current_french_word["French"]



# def get_the_english_word():
#     global current_french_word
#     return current_french_word["English"]

    
# def is_known():
#     global words_to_learn_dict_list, current_french_word
#     words_to_learn_dict_list.remove(current_french_word)


# def update_words_to_learn_csv():
#     global words_to_learn_dict_list
#     #print(len(words_to_learn_dict_list))
#     df = pandas.DataFrame(words_to_learn_dict_list)
#     df.to_csv('data/words_to_learn.csv', index=False)


# def update_front_card(canvas):
#     canvas.itemconfig(canvas_text, text=generate_random_french_word())


# def change_to_back_card(canvas, window, new_image):
#     canvas.itemconfig(image_front, image=new_image)
#     canvas.itemconfig(canvas_text, text=get_the_english_word())
#     canvas.itemconfig(canvas_language, text="English",font=("Arial", 40, 'italic'))
#     window.after_cancel(window)

# def change_to_front_card(canvas, window, old_image, miss=0):
#     global words_to_learn_data, words_to_learn_dict_list, current_french_word

#     if(miss == 1):
#         #input(f'{words_to_learn_dict_list}')
#         if current_french_word not in words_to_learn_dict_list:
#             df = pandas.DataFrame({"French": [current_french_word["French"]], "English": [current_french_word["English"]]})
#             df.to_csv('data/words_to_learn.csv', mode='a', index=False, header=False)
#         window.after_cancel(window)
#         canvas.itemconfig(image_front, image=old_image)
#         canvas.itemconfig(canvas_text, text=generate_random_french_word())
#         canvas.itemconfig(canvas_language, text="French",font=("Arial", 40, 'italic'))
#         window.after(3000, change_to_back_card, flashcard_canvas, window, new_image)

#     else:
#         is_known()
#         update_words_to_learn_csv()

#         window.after_cancel(window)
#         canvas.itemconfig(image_front, image=old_image)
#         canvas.itemconfig(canvas_text, text=generate_random_french_word())
#         canvas.itemconfig(canvas_language, text="French",font=("Arial", 40, 'italic'))
#         window.after(3000, change_to_back_card, flashcard_canvas, window, new_image)


class InsertIcon():
    def __init__(self,window) -> None:
        window.iconphoto(False,PhotoImage(file='english.png'))


class Application(ScreenFunctions):
    def __init__(self, window):


        self.button_functions = {
            "Grammar": lambda: self.openGrammarPage(),
            "Vocabulary": lambda: self.openVocabularyPage(),
            "Pronunciation": lambda: self.openPronunciationPage(),
            "Listening": lambda: self.openListeningPage(),
            "Images": lambda: self.openImagePage(),
            "Phrasal Verbs": lambda: self.openPhrasesPage()
        }

        
        self.main_window = window
        width = 1200
        height = 728
        x_position = 100
        y_position = 150
        self.main_window.geometry(f"{width}x{height}+{x_position}+{y_position}")
        self.main_window.title("ENGLISH APP")
        icon = InsertIcon(self.main_window)
        self.main_window.config(background=BACKGROUND_COLOR)
        self.main_window.resizable(True,True)
        self.load_buttons()
        #self.load_textarea_to_mark_words()
        #self.load_timer_element()
        #self.main_window.iconphoto(False,PhotoImage(file='english.png'))
        self.main_window.mainloop()


    def create_button(self,name, screen, text, border, bg, font, activebackground ,activeforeground, command, x, y):
        name = Button(screen, text=text, border=border, bg=bg, font=font, activebackground=activebackground ,activeforeground=activeforeground, command=lambda: self.button_functions[command]())
        name.place(relx=x, rely=y, relwidth=0.2, relheight=0.1)
        buttons_list.append(name)
        #input(f'{buttons_list}')
        return name


    def load_buttons(self):
        x = 0.05
        y = 0.001
        index = 0
        

        for folder in buttons_titles:
            #input("FOLDER -> "+str(folder))
            #folders_created.append(folder)
            self.create_button(folder, self.main_window, folder, 2, "#CC1705", ('verdana', 10, 'bold'), '#108ecb' ,'white', str(folder),x,y)
            
            x+=0.3
            if(x >= 0.85):
                x = 0.05
                y+=0.14
            index+=1

        #input(f"CREATING BACK")
        self.bt_quit = Button(self.main_window, text="Quit", border=2, bg="#CC1705", font=('verdana', 10, 'bold'), activebackground='#108ecb' ,activeforeground='white', command=self.main_window.destroy)
        self.bt_quit.place(relx=0.25,rely=0.86, relwidth=0.4, relheight=0.1)
        
        #DELETE LINE BELOW IF SOME PROBLEM APPEARS.
        buttons_list.append(self.bt_quit)



if __name__ == '__main__':
    db_obj = DB_Actions()
    db_obj.mountTables()
    new_window = Tk()
    Application(new_window)


    #print(to_learn)
    #data_frame = pandas.DataFrame.to_dict(data_words, orient="records")


    #print(data_frame)
    # words_dict = {row.French: row.English for (index, row) in data_words.iterrows()}
    
    
    

    # flashcard_canvas = Canvas(width=800, height=518, background=BACKGROUND_COLOR, highlightthickness=0)
    # my_flashcard_image = PhotoImage(file="images/card_front.png")
    # new_image = PhotoImage(file="images/card_back.png")

    # image_front = flashcard_canvas.create_image(400,270,image=my_flashcard_image)
    # canvas_text = flashcard_canvas.create_text(400,263,text=generate_random_french_word(),font=("Arial", 60, 'bold'))
    # canvas_language = flashcard_canvas.create_text(400,150,text="French",font=("Arial", 40, 'italic'))
    # flashcard_canvas.grid(column=1, row=1, columnspan=2)



    # right_image = PhotoImage(file="images/right.png")
    # button_right = Button(image=right_image, highlightthickness=0, command=lambda: change_to_front_card(flashcard_canvas, window, my_flashcard_image, 0))
    # button_right.grid(column=2, row=2, pady=50, padx=50)


    # left_image = PhotoImage(file="images/wrong.png")
    # button_left = Button(image=left_image, highlightthickness=0, command=lambda: change_to_front_card(flashcard_canvas, window, my_flashcard_image, 1))
    # button_left.grid(column=1, row=2, pady=50, padx=50)

    # window.after(3000, change_to_back_card, flashcard_canvas, window, new_image)
    