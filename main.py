from window import Window
from PyQt5 import QtWidgets
import sys

qapp = QtWidgets.QApplication([])
application = Window()
application.show()
sys.exit(qapp.exec())