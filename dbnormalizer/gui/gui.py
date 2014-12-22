__author__ = 'Maira'

import sys
from PySide.QtCore import *
from PySide.QtGui import *

app = QApplication(sys.argv)

label = QLabel("Hello World")

label.show()

app.exec_()
sys.exit()