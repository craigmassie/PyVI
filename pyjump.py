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

def get_indent(current, parent):
    if parent != root:
        if ((len(current) - len(current.strip())) - ((len(parent.name)) - len(parent.name.strip())) == 0):
            return parent.parent
        else:
            return get_indent(current, parent.parent)
    else:
        return root


def open_file(file_path):
    code = (open(file_path, "r"))

    lines = code.readlines()
    # for every line in the code to be read
    for line in lines:
        if line.strip().startswith("#"):
            continue

        keywords = ["def ", "class ", "for ", "if ", "elif", "while ", "try", "else", "except", "finally"]

        if any(line.strip().startswith(keyword) for keyword in keywords):
            if not line[0].isspace():
                last = Node(line, parent =root)
            #If the current line is more indented than the last
            else:
                cond = ((len(line) - len(line.strip())) - ((len(last.name)) - len(last.name.strip())))
                if (cond > 0):
                    indented = Node(line, parent =last)
                    last = indented
                #Need to check if equal or before
                elif (cond == 0):
                    indented = Node(line, parent =last.parent)
                    last = indented
                #If that current line is indented less than previous
                elif (cond < 0):
                    indented = Node(line, parent = get_indent(line, last.parent))
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

class PyViUI(QWidget):
    
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
            childtext = child.name.strip()
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
    ex = PyViUI()
    sys.exit(app.exec_())