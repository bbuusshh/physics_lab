from PyQt5.QtWidgets import QApplication , QMainWindow, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from UiTimeTaggerApp import Ui_MainWindow
import matplotlib.cm as cm
import numpy as np
import time_tagger_api
import yaml
import sys

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
        self.histo1()

    def histo1(self):
        mpl=self.widget_histo1.canvas
        mpl.ax.clear()

        t_max = self.tt.binWidth1 * self.tt.numBins1 / 1000 # ns
        t_range = np.lispace(0, t_max, self.tt.numBins1)

        mpl.y_ = self.tt.hist_1.getData()/(self.tt.binWidth1/1000)
        mpl.new_y_data = lambda x: self.tt.hist_1.getData()/(self.tt.binWidth1/1000)

        mpl.ax_plot = mpl.ax.plot(t_range, mpl.y_)
        mpl.ax.set_xlabel(u"$time, ns$",fontsize=12, fontweight="bold" )
        mpl.ax.set_ylabel(u"$countrate, kcps$",fontsize=12, fontweight="bold" )
        mpl.ax.set_xticks(linspace(0, self.numBins1, 5));
        mpl.ax.set_xticklabels(linspace(0, t_max, 5), color="r" )
        mpl.ax.set_yticks(linspace(0, len(mpl.y_), 5));
        mpl.ax.set_yticklabels(linspace(0, max(mpl.y_), 5), color="r" )
        mpl.draw()

        mpl.timer= mpl.new_timer(mpl.interval, [(mpl.update_canvas, (), {})])
        mpl.timer.start()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MyApplication = MainApp()
    MyApplication.show() # Show the form
    sys.exit(app.exec_()) # Execute the app