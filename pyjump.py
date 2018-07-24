from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from anytree import Node, RenderTree
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QGridLayout)
from PyQt5.QtGui import QFont

Tk().withdraw()
file_path = askopenfilename()
grid = QGridLayout()
def open_file(file_path):
    code = (open(file_path, "r"))

    lines = code.readlines()
    # for every line in the code to be read
    for line in lines:
        if line.strip().startswith("#"):
            continue
        #if we define a function, and it's not indented
        if "def " in line or "class " in line:
            if not line[0].isspace():
                print(line.split())
                name = line
                last = Node(name, parent=root)
        #if we have a for loop, checks indent
        elif "for " in line or "if " in line or "while " in line or "try" in line or "else" in line or "except" in line or "finally" in line:
            if not line[0].isspace():
                last = Node(line.strip("\n"), parent =root)
            #If the current line is more indented than the last
            else:
                cond = (len(line) - len(line.strip()) - ((len(last.name) + 1) - len(last.name.strip())))
                if (cond > 0):
                    indented = Node(line.strip("\n"), parent =last)
                    last = indented
                #Need to check if equal or before
                elif (cond == 0):
                    indented = Node(line.strip("\n"), parent =last.parent)
                    last = indented
                elif (cond < 0):
                    indented = Node(line.strip("\n"), parent =last.parent.parent)
                    last = indented
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

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        # btn = QPushButton('Button', self)
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.resize(btn.sizeHint())
        # btn.move(50, 50)       
        self.display_nodes(root)
        # self.setWindowTitle('PyVi') 
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.center()   
        self.show()

    def update_items(self, selected):
        if len(selected.children) != 0:
            for i in reversed(range(grid.count())): 
                grid.itemAt(i).widget().setParent(None)
            self.display_nodes(selected)

    
    def display_nodes(self, node):
        i = 0
        j = 0
        for child in node.children:
            #Bare with me here. So a button is created for each child to a given node. At each button click
            #we must have a function to update the items. Since lamda uses the last variable given
            #we use a trick child=child to force the current child to be passed.
            childtext = child.name
            btn = QPushButton(childtext, self)
            btn.setStyleSheet("background-color: #2b2b2b; color: white; height: 100px; width: 200px; max-width: 200px;")
            if len(child.children) != 0:
                btn.setStyleSheet("background-color: #4b4b4b; color: white; height: 100px; max-width: 200px; width: 200px;")
            btn.clicked.connect(lambda state, bound_child=child: self.update_items(bound_child))
            btn.setToolTip('This button represents the ' + childtext + ' block of code')
            if i == 5:
                i = 0
                j +=1 
            grid.addWidget(btn, j, i)
            i += 1    

        if child.parent != root:
            btn = QPushButton("Back", self)
            btn.setStyleSheet("background-color: #2b2b2b; color: white; height: 100px; max-width: 200px; width: 200px;")
            btn.clicked.connect(lambda: self.update_items(node.parent))
            grid.addWidget(btn, i+1, j)
        
        self.setLayout(grid)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())