from tkinter import *

win = Tk()
win.title("My project")
win.geometry('500x300')
win.resizable(False, False) # Заборона зміни розмірів вікна
# Елементи керування
# Написи
nap = Label(win, text="Текст для напису", font=('Comic Sans MS', 20), bg="green", fg="white")
nap.place(relx=0.1, rely= 0.4)

win.mainloop()
