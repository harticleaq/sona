from PyQt5 import QtCore,QtWidgets,QtGui,Qt
import sys

class SonaWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SonaWindow,self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Sona波形处理')
        self.resize(900,600)

