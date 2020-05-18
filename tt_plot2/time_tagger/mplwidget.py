"""MATPLOTLIB WIDGET"""
# Python Qt5 bindings for GUI objects
from PyQt5.QtWidgets import QSizePolicy, QWidget, QVBoxLayout
 # import the Qt5Agg FigureCanvas object, that binds Figure to
# Qt5Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# Matplotlib Toolbar
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
# Matplotlib Figure object
from matplotlib.figure import Figure
from matplotlib import rcParams
import numpy as np
rcParams["font.size"] = 9
class MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self):
        # setup Matplotlib Figure and Axis
        self.interval = 10
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax_plot = self.ax.plot(0,0)
        self.y_ = [0]
        self.new_y_data = lambda x: 0
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding ,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self) 
        
    def update_canvas(self):
        self.y_.append(self.new_data())     # Add new datapoint
        self.ax_plot.set_ydata(self.y_)
        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.ax_plot)
        self.update()
        self.flush_events()

class MPL_WIDGET(QWidget):
    """ Widget defined in Qt Designer """
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.navi_toolbar = NavigationToolbar(self.canvas, self)
        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.navi_toolbar)
        self.setLayout(self.vbl)
        self.show()