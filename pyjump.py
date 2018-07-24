import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
import os
from anytree import Node, RenderTree

window = tk.Tk()
window.withdraw()

file_path = askopenfilename()

def open_file(file_path):
    code = (open(file_path, "r"))

    lines = code.readlines()
    # for every line in the code to be read
    for line in lines:
        #if we define a function, and it's not indented
        if "def " in line:
            if not line[0].isspace():
                name = line.split()[1]
                last = Node(name, parent=root)
        #if we have a for loop, checks indent
        elif "for " in line or "if " in line or "while " in line or "try" in line or "else" in line or "except" in line or "finally" in line:
            if not line[0].isspace():
                last = Node(line.strip("\n"), parent =root)
            else:
                indented = Node(line.strip("\n"), parent =last)
        else:
            try:
                if not last.name == "Code Block" and not line[0].isspace():
                    last = Node("Code Block", parent=root)
            except NameError:
                continue
            

root = Node(os.path.basename(file_path))
open_file(file_path)
for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))


screen_width = int((window.winfo_screenwidth()/2) - 350)
screen_height = int((window.winfo_screenheight()/2) -212)

window.geometry("700x425+" + str(screen_width) + "+" + str(screen_height))
window.deiconify()
window.title("PyJump")

# T = tk.Text(window)
# T.config(font=("Arial"))
# T.pack()

def callback(child):
    print(child)

def update_items(selected):
    if len(selected.children) != 0:
        for button in window.children.values(): button.pack_forget()
        display_nodes(selected)


def display_nodes(node):
    for child in node.children:
        #Bare with me here. So a button is created for each child to a given node. At each button click
        #we must have a function to update the items. Since lamda uses the last variable given
        #we use a trick child=child to force the current child to be passed.
        b = Button(window, text=child, command = lambda child=child: update_items(child))
        b.pack()
    if child.parent != root:
        b = Button(window, text="Back", command = lambda: update_items(node.parent))
        b.pack()
    

display_nodes(root)
window.mainloop()