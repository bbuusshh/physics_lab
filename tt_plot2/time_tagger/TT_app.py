from PyQt5.QtWidgets import QApplication , QMainWindow, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from UiTimeTaggerApp import Ui_MainWindow
import matplotlib.cm as cm
import numpy as np
import time_tagger_api
import yaml

pars_file = open("./params.yaml", 'r')
PARAMS = yaml.safe_load(pars_file)

class MainApp(QMainWindow , Ui_MainWindow):
    """
    MainApp class inherit from QMainWindow and from
    Ui_MainWindow class in UiMainApp module. """
    def __init__(self):
        """ Constructor or the initializer """
        QMainWindow.__init__(self)
        # It is imperative to call self.setupUi (self) for the interface to initialize.
        self.setupUi(self) # This is defined in design.py file automatically
        self.tt = time_tagger_api.TT(PARAMS, runTest=True)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MyApplication = MainApp()
    MyApplication.show() # Show the form
    sys.exit(app.exec_()) # Execute the app