import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename

window = tk.Tk()
window.withdraw()

file_path = askopenfilename()

funcs = {}

def open_file(file_path):
    code = (open(file_path, "r"))

    lines = code.readlines()
    for line in lines:
        if "def" in line:
            name = line.split()[1]
            funcs[name] = []
    
    print(funcs)

open_file(file_path)

screen_width = int((window.winfo_screenwidth()/2) - 350)
screen_height = int((window.winfo_screenheight()/2) -212)

window.geometry("700x425+" + str(screen_width) + "+" + str(screen_height))
window.deiconify()
window.title("PyJump")

T = tk.Text(window)
T.config(font=("Arial"))
T.pack()
for key in funcs:
    T.insert(tk.END, key)
    T.insert(tk.END, "\n")
    

window.mainloop()