# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fraunh.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1062, 706)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mplwidget = MPL_WIDGET(self.centralwidget)
        self.mplwidget.setGeometry(QtCore.QRect(210, 20, 631, 641))
        self.mplwidget.setObjectName("mplwidget")
        self.label_lambda = QtWidgets.QLabel(self.centralwidget)
        self.label_lambda.setGeometry(QtCore.QRect(10, 10, 120, 16))
        self.label_lambda.setObjectName("label_lambda")
        self.SpinBox_lambda = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.SpinBox_lambda.setGeometry(QtCore.QRect(20, 30, 68, 24))
        self.SpinBox_lambda.setMinimum(1.0)
        self.SpinBox_lambda.setMaximum(1000.0)
        self.SpinBox_lambda.setProperty("value", 590.0)
        self.SpinBox_lambda.setObjectName("SpinBox_lambda")
        self.slider_lambda = QtWidgets.QSlider(self.centralwidget)
        self.slider_lambda.setGeometry(QtCore.QRect(10, 60, 160, 22))
        self.slider_lambda.setMinimum(1)
        self.slider_lambda.setMaximum(1000)
        self.slider_lambda.setProperty("value", 590)
        self.slider_lambda.setOrientation(QtCore.Qt.Horizontal)
        self.slider_lambda.setObjectName("slider_lambda")
        self.SpinBox_b = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.SpinBox_b.setGeometry(QtCore.QRect(20, 120, 68, 24))
        self.SpinBox_b.setMinimum(1.0)
        self.SpinBox_b.setProperty("value", 50.0)
        self.SpinBox_b.setObjectName("SpinBox_b")
        self.slider_b = QtWidgets.QSlider(self.centralwidget)
        self.slider_b.setGeometry(QtCore.QRect(10, 150, 160, 22))
        self.slider_b.setMinimum(1)
        self.slider_b.setProperty("value", 50)
        self.slider_b.setOrientation(QtCore.Qt.Horizontal)
        self.slider_b.setObjectName("slider_b")
        self.label_b = QtWidgets.QLabel(self.centralwidget)
        self.label_b.setGeometry(QtCore.QRect(10, 100, 120, 16))
        self.label_b.setObjectName("label_b")
        self.slider_h = QtWidgets.QSlider(self.centralwidget)
        self.slider_h.setGeometry(QtCore.QRect(10, 230, 160, 22))
        self.slider_h.setMinimum(1)
        self.slider_h.setPageStep(8)
        self.slider_h.setProperty("value", 50)
        self.slider_h.setOrientation(QtCore.Qt.Horizontal)
        self.slider_h.setObjectName("slider_h")
        self.label_h = QtWidgets.QLabel(self.centralwidget)
        self.label_h.setGeometry(QtCore.QRect(10, 180, 120, 16))
        self.label_h.setObjectName("label_h")
        self.SpinBox_h = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.SpinBox_h.setGeometry(QtCore.QRect(20, 200, 68, 24))
        self.SpinBox_h.setProperty("value", 50.0)
        self.SpinBox_h.setObjectName("SpinBox_h")
        self.slider_a = QtWidgets.QSlider(self.centralwidget)
        self.slider_a.setGeometry(QtCore.QRect(10, 320, 160, 22))
        self.slider_a.setMinimum(1)
        self.slider_a.setProperty("value", 4)
        self.slider_a.setOrientation(QtCore.Qt.Horizontal)
        self.slider_a.setObjectName("slider_a")
        self.label_a = QtWidgets.QLabel(self.centralwidget)
        self.label_a.setGeometry(QtCore.QRect(10, 270, 120, 16))
        self.label_a.setObjectName("label_a")
        self.SpinBox_a = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.SpinBox_a.setGeometry(QtCore.QRect(20, 290, 68, 24))
        self.SpinBox_a.setMaximum(100.0)
        self.SpinBox_a.setProperty("value", 15.0)
        self.SpinBox_a.setObjectName("SpinBox_a")
        self.slider_f2 = QtWidgets.QSlider(self.centralwidget)
        self.slider_f2.setGeometry(QtCore.QRect(10, 400, 160, 22))
        self.slider_f2.setMinimum(1)
        self.slider_f2.setProperty("value", 4)
        self.slider_f2.setOrientation(QtCore.Qt.Horizontal)
        self.slider_f2.setObjectName("slider_f2")
        self.label_f2 = QtWidgets.QLabel(self.centralwidget)
        self.label_f2.setGeometry(QtCore.QRect(10, 350, 120, 16))
        self.label_f2.setObjectName("label_f2")
        self.SpinBox_f2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.SpinBox_f2.setGeometry(QtCore.QRect(20, 370, 68, 24))
        self.SpinBox_f2.setProperty("value", 2.0)
        self.SpinBox_f2.setObjectName("SpinBox_f2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1062, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_lambda.setText(_translate("MainWindow", "Wavelength (nm)"))
        self.label_b.setText(_translate("MainWindow", "b (1e-5 m)"))
        self.label_h.setText(_translate("MainWindow", "h (1e-5 m)"))
        self.label_a.setText(_translate("MainWindow", "a(mm)"))
        self.label_f2.setText(_translate("MainWindow", "f2(m)"))
from mplwidget import MPL_WIDGET


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
