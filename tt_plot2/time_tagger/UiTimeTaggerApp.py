# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TT.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1049, 714)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget_up = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_up.setGeometry(QtCore.QRect(280, 0, 751, 331))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.tabWidget_up.setFont(font)
        self.tabWidget_up.setStyleSheet("")
        self.tabWidget_up.setObjectName("tabWidget_up")
        self.tab_histo1 = PyQtGraph()
        self.tab_histo1.setObjectName("tab_histo1")
        self.widget_histo1 = PyQtGraph(self.tab_histo1)
        self.widget_histo1.setGeometry(QtCore.QRect(0, 0, 751, 301))
        self.widget_histo1.setObjectName("widget_histo1")
        self.tabWidget_up.addTab(self.tab_histo1, "")
        self.tab_correlation = QtWidgets.QWidget()
        self.tab_correlation.setObjectName("tab_correlation")
        self.widget_correlation = PyQtGraph(self.tab_correlation)
        self.widget_correlation.setGeometry(QtCore.QRect(0, 0, 751, 301))
        self.widget_correlation.setObjectName("widget_correlation")
        self.tabWidget_up.addTab(self.tab_correlation, "")
        self.tab_freeze = QtWidgets.QWidget()
        self.tab_freeze.setObjectName("tab_freeze")
        self.widget_freeze = PyQtGraph(self.tab_freeze)
        self.widget_freeze.setGeometry(QtCore.QRect(0, 0, 751, 301))
        self.widget_freeze.setObjectName("widget_freeze")
        self.tabWidget_up.addTab(self.tab_freeze, "")
        self.tabWidget_down = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_down.setGeometry(QtCore.QRect(280, 330, 751, 331))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.tabWidget_down.setFont(font)
        self.tabWidget_down.setObjectName("tabWidget_down")
        self.tab_histo2 = QtWidgets.QWidget()
        self.tab_histo2.setObjectName("tab_histo2")
        self.widget_histo2 = PyQtGraph(self.tab_histo2)
        self.widget_histo2.setGeometry(QtCore.QRect(0, 0, 751, 301))
        self.widget_histo2.setObjectName("widget_histo2")
        self.tabWidget_down.addTab(self.tab_histo2, "")
        self.tab_countrate = QtWidgets.QWidget()
        self.tab_countrate.setObjectName("tab_countrate")
        self.widget_countrate = PyQtGraph(self.tab_countrate)
        self.widget_countrate.setGeometry(QtCore.QRect(0, 0, 751, 301))
        self.widget_countrate.setObjectName("widget_countrate")
        self.tabWidget_down.addTab(self.tab_countrate, "")
        self.tab_gate = QtWidgets.QWidget()
        self.tab_gate.setObjectName("tab_gate")
        self.widget_gate = PyQtGraph(self.tab_gate)
        self.widget_gate.setGeometry(QtCore.QRect(0, 0, 751, 301))
        self.widget_gate.setObjectName("widget_gate")
        self.tabWidget_down.addTab(self.tab_gate, "")
        self.label_settings = QtWidgets.QLabel(self.centralwidget)
        self.label_settings.setGeometry(QtCore.QRect(10, 10, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_settings.setFont(font)
        self.label_settings.setFrameShape(QtWidgets.QFrame.Box)
        self.label_settings.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_settings.setTextFormat(QtCore.Qt.RichText)
        self.label_settings.setAlignment(QtCore.Qt.AlignCenter)
        self.label_settings.setObjectName("label_settings")
        self.label_binsNumber = QtWidgets.QLabel(self.centralwidget)
        self.label_binsNumber.setGeometry(QtCore.QRect(10, 60, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_binsNumber.setFont(font)
        self.label_binsNumber.setObjectName("label_binsNumber")
        self.label_binWidth = QtWidgets.QLabel(self.centralwidget)
        self.label_binWidth.setGeometry(QtCore.QRect(10, 140, 61, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_binWidth.setFont(font)
        self.label_binWidth.setObjectName("label_binWidth")
        self.spinBox_binsNumber = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_binsNumber.setGeometry(QtCore.QRect(10, 80, 61, 24))
        self.spinBox_binsNumber.setMinimum(50)
        self.spinBox_binsNumber.setMaximum(2000)
        self.spinBox_binsNumber.setSingleStep(50)
        self.spinBox_binsNumber.setProperty("value", 1000)
        self.spinBox_binsNumber.setObjectName("spinBox_binsNumber")
        self.spinBox_binWidth = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_binWidth.setGeometry(QtCore.QRect(10, 160, 61, 24))
        self.spinBox_binWidth.setMinimum(50)
        self.spinBox_binWidth.setMaximum(2000)
        self.spinBox_binWidth.setSingleStep(50)
        self.spinBox_binWidth.setProperty("value", 1000)
        self.spinBox_binWidth.setObjectName("spinBox_binWidth")
        self.horizontalSlider_binsNumber_binWidth = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_binsNumber_binWidth.setGeometry(QtCore.QRect(10, 110, 241, 22))
        self.horizontalSlider_binsNumber_binWidth.setMinimum(50)
        self.horizontalSlider_binsNumber_binWidth.setMaximum(2000)
        self.horizontalSlider_binsNumber_binWidth.setSingleStep(50)
        self.horizontalSlider_binsNumber_binWidth.setProperty("value", 1000)
        self.horizontalSlider_binsNumber_binWidth.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_binsNumber_binWidth.setObjectName("horizontalSlider_binsNumber_binWidth")
        self.horizontalSlider_binWidth = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_binWidth.setGeometry(QtCore.QRect(10, 190, 241, 22))
        self.horizontalSlider_binWidth.setMinimum(50)
        self.horizontalSlider_binWidth.setMaximum(2000)
        self.horizontalSlider_binWidth.setSingleStep(50)
        self.horizontalSlider_binWidth.setProperty("value", 1000)
        self.horizontalSlider_binWidth.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_binWidth.setObjectName("horizontalSlider_binWidth")
        self.radioButton_plotI = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_plotI.setGeometry(QtCore.QRect(100, 20, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.radioButton_plotI.setFont(font)
        self.radioButton_plotI.setObjectName("radioButton_plotI")
        self.radioButton_plotII = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_plotII.setGeometry(QtCore.QRect(170, 20, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.radioButton_plotII.setFont(font)
        self.radioButton_plotII.setObjectName("radioButton_plotII")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(260, 10, 20, 651))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.spinBox_refresh = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_refresh.setGeometry(QtCore.QRect(10, 260, 51, 24))
        self.spinBox_refresh.setMinimum(1)
        self.spinBox_refresh.setMaximum(50)
        self.spinBox_refresh.setSingleStep(1)
        self.spinBox_refresh.setProperty("value", 1)
        self.spinBox_refresh.setDisplayIntegerBase(10)
        self.spinBox_refresh.setObjectName("spinBox_refresh")
        self.horizontalSlider_refresh = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_refresh.setGeometry(QtCore.QRect(10, 290, 241, 22))
        self.horizontalSlider_refresh.setMinimum(1)
        self.horizontalSlider_refresh.setMaximum(50)
        self.horizontalSlider_refresh.setSingleStep(1)
        self.horizontalSlider_refresh.setProperty("value", 1)
        self.horizontalSlider_refresh.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_refresh.setObjectName("horizontalSlider_refresh")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(10, 230, 87, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.checkBox.setFont(font)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 210, 251, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 310, 251, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_correlation = QtWidgets.QLabel(self.centralwidget)
        self.label_correlation.setGeometry(QtCore.QRect(10, 330, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_correlation.setFont(font)
        self.label_correlation.setFrameShape(QtWidgets.QFrame.Box)
        self.label_correlation.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_correlation.setAlignment(QtCore.Qt.AlignCenter)
        self.label_correlation.setObjectName("label_correlation")
        self.radioButton_apdI = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_apdI.setGeometry(QtCore.QRect(20, 380, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.radioButton_apdI.setFont(font)
        self.radioButton_apdI.setChecked(True)
        self.radioButton_apdI.setAutoExclusive(False)
        self.radioButton_apdI.setObjectName("radioButton_apdI")
        self.radioButton_apdII = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_apdII.setGeometry(QtCore.QRect(120, 380, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.radioButton_apdII.setFont(font)
        self.radioButton_apdII.setChecked(True)
        self.radioButton_apdII.setAutoRepeat(False)
        self.radioButton_apdII.setAutoExclusive(False)
        self.radioButton_apdII.setObjectName("radioButton_apdII")
        self.radioButton_apdIII = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_apdIII.setGeometry(QtCore.QRect(120, 420, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.radioButton_apdIII.setFont(font)
        self.radioButton_apdIII.setChecked(True)
        self.radioButton_apdIII.setAutoExclusive(False)
        self.radioButton_apdIII.setObjectName("radioButton_apdIII")
        self.radioButton_apdIV = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_apdIV.setGeometry(QtCore.QRect(20, 420, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.radioButton_apdIV.setFont(font)
        self.radioButton_apdIV.setChecked(True)
        self.radioButton_apdIV.setAutoExclusive(False)
        self.radioButton_apdIV.setObjectName("radioButton_apdIV")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(10, 440, 251, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.label_correlation_dump = QtWidgets.QLabel(self.centralwidget)
        self.label_correlation_dump.setGeometry(QtCore.QRect(10, 460, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_correlation_dump.setFont(font)
        self.label_correlation_dump.setFrameShape(QtWidgets.QFrame.Box)
        self.label_correlation_dump.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_correlation_dump.setAlignment(QtCore.Qt.AlignCenter)
        self.label_correlation_dump.setObjectName("label_correlation_dump")
        self.comboBox_dump = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_dump.setGeometry(QtCore.QRect(90, 460, 171, 31))
        self.comboBox_dump.setObjectName("comboBox_dump")
        self.comboBox_dump.addItem("")
        self.comboBox_dump.addItem("")
        self.comboBox_dump.addItem("")
        self.comboBox_dump.addItem("")
        self.comboBox_dump.addItem("")
        self.comboBox_dump.addItem("")
        self.comboBox_dump.addItem("")
        self.checkBox_dump = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_dump.setGeometry(QtCore.QRect(10, 490, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.checkBox_dump.setFont(font)
        self.checkBox_dump.setObjectName("checkBox_dump")
        self.label_size = QtWidgets.QLabel(self.centralwidget)
        self.label_size.setGeometry(QtCore.QRect(90, 490, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_size.setFont(font)
        self.label_size.setAlignment(QtCore.Qt.AlignCenter)
        self.label_size.setObjectName("label_size")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(10, 520, 251, 20))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.label_countrate = QtWidgets.QLabel(self.centralwidget)
        self.label_countrate.setGeometry(QtCore.QRect(10, 550, 221, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.label_countrate.setFont(font)
        self.label_countrate.setObjectName("label_countrate")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(10, 580, 251, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.line_6.setFont(font)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 630, 87, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.label_countrate_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_countrate_2.setGeometry(QtCore.QRect(10, 600, 221, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.label_countrate_2.setFont(font)
        self.label_countrate_2.setObjectName("label_countrate_2")
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setGeometry(QtCore.QRect(10, 650, 251, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1049, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget_up.setCurrentIndex(0)
        self.tabWidget_down.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tab_histo1.setWhatsThis(_translate("MainWindow", "histo_1"))
        self.tab_histo1.setAccessibleName(_translate("MainWindow", "histo_1"))
        self.tabWidget_up.setTabText(self.tabWidget_up.indexOf(self.tab_histo1), _translate("MainWindow", "Histo"))
        self.tabWidget_up.setTabText(self.tabWidget_up.indexOf(self.tab_correlation), _translate("MainWindow", "g2"))
        self.tabWidget_up.setTabText(self.tabWidget_up.indexOf(self.tab_freeze), _translate("MainWindow", "Freeze"))
        self.tabWidget_down.setTabText(self.tabWidget_down.indexOf(self.tab_histo2), _translate("MainWindow", "Histo"))
        self.tabWidget_down.setTabText(self.tabWidget_down.indexOf(self.tab_countrate), _translate("MainWindow", "Count"))
        self.tabWidget_down.setTabText(self.tabWidget_down.indexOf(self.tab_gate), _translate("MainWindow", "Gate"))
        self.label_settings.setText(_translate("MainWindow", "Settings"))
        self.label_binsNumber.setText(_translate("MainWindow", "bins number"))
        self.label_binWidth.setText(_translate("MainWindow", "bin width"))
        self.radioButton_plotI.setText(_translate("MainWindow", "plot I"))
        self.radioButton_plotII.setText(_translate("MainWindow", "plot II"))
        self.checkBox.setText(_translate("MainWindow", "refresh"))
        self.label_correlation.setText(_translate("MainWindow", "Correlations"))
        self.radioButton_apdI.setText(_translate("MainWindow", "APD I"))
        self.radioButton_apdII.setText(_translate("MainWindow", "APD II"))
        self.radioButton_apdIII.setText(_translate("MainWindow", "APD IV"))
        self.radioButton_apdIV.setText(_translate("MainWindow", "APD III"))
        self.label_correlation_dump.setText(_translate("MainWindow", "Dump"))
        self.comboBox_dump.setItemText(0, _translate("MainWindow", "Other"))
        self.comboBox_dump.setItemText(1, _translate("MainWindow", "Rabi"))
        self.comboBox_dump.setItemText(2, _translate("MainWindow", "Ramsey"))
        self.comboBox_dump.setItemText(3, _translate("MainWindow", "Imaging"))
        self.comboBox_dump.setItemText(4, _translate("MainWindow", "T2 map"))
        self.comboBox_dump.setItemText(5, _translate("MainWindow", "Rabi splitting"))
        self.comboBox_dump.setItemText(6, _translate("MainWindow", "New project"))
        self.checkBox_dump.setText(_translate("MainWindow", "DUMP"))
        self.label_size.setText(_translate("MainWindow", "size: 0 Mb"))
        self.label_countrate.setText(_translate("MainWindow", "Countrate :  0 kcps"))
        self.checkBox_2.setText(_translate("MainWindow", "Gate"))
        self.label_countrate_2.setText(_translate("MainWindow", "Gated countrate :  0 kcps"))
from pyqtgraph import PyQtGraph


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
