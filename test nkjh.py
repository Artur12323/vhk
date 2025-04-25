from multiprocessing.sharedctypes import typecode_to_type
from tkinter import *
from tkinter import ttk

win = Tk()
win.title("My project")
win.geometry('500x300')
win.resizable(False, False) # Заборона зміни розмірів вікна
# Елементи керування
# Написи
nap = Label(win, text="Текст для напису", font=('Comic Sans MS', 20), bg="green", fg="white")
nap.place(relx=0.1, rely= 0.1,)
# Поле для ведення тексту
ent = Entry(win, font=('Comic Sans MS', 20), width=4)
ent.place(relx=0.1, rely=0.2)
# Кнопка
but = Button(win, text='Klick', font=('Comic Sans MS', 20), width=7, height=3, bg="red", fg="#004512")
but.place(relx=0.1, rely=0.35)
#  Випадаючий список
comb = ttk.Combobox(win, font=('Comic Sans MS', 15), width=10, values=['option1', 'option2', 'option3', 'option4', 'option5'])
comb.place(relx=0.4, rely=0.35)

win.mainloop()
