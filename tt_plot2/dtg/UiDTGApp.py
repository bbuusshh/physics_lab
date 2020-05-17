# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dtg.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(155, 370)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBox_run = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_run.setGeometry(QtCore.QRect(30, 20, 71, 41))
        self.checkBox_run.setObjectName("checkBox_run")
        self.doubleSpinBox_pulselen = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_pulselen.setGeometry(QtCore.QRect(20, 90, 68, 24))
        self.doubleSpinBox_pulselen.setMinimum(1.0)
        self.doubleSpinBox_pulselen.setMaximum(150.0)
        self.doubleSpinBox_pulselen.setObjectName("doubleSpinBox_pulselen")
        self.label_pulselen = QtWidgets.QLabel(self.centralwidget)
        self.label_pulselen.setGeometry(QtCore.QRect(20, 70, 101, 16))
        self.label_pulselen.setObjectName("label_pulselen")
        self.doubleSpinBox_pulsesep = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_pulsesep.setGeometry(QtCore.QRect(20, 150, 68, 24))
        self.doubleSpinBox_pulsesep.setMinimum(5.0)
        self.doubleSpinBox_pulsesep.setMaximum(200.0)
        self.doubleSpinBox_pulsesep.setProperty("value", 50.0)
        self.doubleSpinBox_pulsesep.setObjectName("doubleSpinBox_pulsesep")
        self.label_pulsesep = QtWidgets.QLabel(self.centralwidget)
        self.label_pulsesep.setGeometry(QtCore.QRect(20, 130, 131, 16))
        self.label_pulsesep.setObjectName("label_pulsesep")
        self.label_load = QtWidgets.QLabel(self.centralwidget)
        self.label_load.setGeometry(QtCore.QRect(20, 190, 101, 16))
        self.label_load.setObjectName("label_load")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 210, 105, 88))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox_load = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_load.setObjectName("comboBox_load")
        self.comboBox_load.addItem("")
        self.verticalLayout.addWidget(self.comboBox_load)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_load = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_load.setObjectName("pushButton_load")
        self.verticalLayout_2.addWidget(self.pushButton_load)
        self.checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_2.addWidget(self.checkBox)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 155, 22))
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
        self.checkBox_run.setText(_translate("MainWindow", "RUN"))
        self.label_pulselen.setText(_translate("MainWindow", "pulse length, ns"))
        self.label_pulsesep.setText(_translate("MainWindow", "pulse separation, ns"))
        self.label_load.setText(_translate("MainWindow", "load sequence"))
        self.comboBox_load.setItemText(0, _translate("MainWindow", "Ramsey"))
        self.pushButton_load.setText(_translate("MainWindow", "load seq"))
        self.checkBox.setText(_translate("MainWindow", "from file"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
