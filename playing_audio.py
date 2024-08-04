from tkinter import *
from pygame import mixer


mixer.init()
sound = mixer.Sound("listen.mp3")


root = Tk()
Button(root, command=sound.play).pack()
root.mainloop()