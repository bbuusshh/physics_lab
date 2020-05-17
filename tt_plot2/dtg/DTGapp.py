from PyQt5.QtWidgets import QApplication , QMainWindow, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from UiDTGApp import Ui_MainWindow
import matplotlib.cm as cm
import numpy as np
import dtg_api
import os

class MainApp(QMainWindow , Ui_MainWindow):
    """
    MainApp class inherit from QMainWindow and from
    Ui_MainWindow class in UiMainApp module. """
    def __init__(self):
        """ Constructor or the initializer """
        QMainWindow.__init__(self)
        # It is imperative to call self.setupUi (self) for the interface to initialize.
        self.setupUi(self) # This is defined in design.py file automatically
        self.dtg = dtg_api.DTG(dtg_adress='TCPI .. :::', channels=[1,2,3,4])
        self.checkBox_run.clicked.connect(self.on_checkBox_run)
        self.comboBox_load.currentIndexChanged.connect(self.on_comboBox_load)
        self.channel = ['A', 1]
        pulse_len_0 = self.doubleSpinBox_pulselen.value()
        pulse_sep_0 = self.doubleSpinBox_pulsesep.value()
        sequence = self.get_short_pulse_seq(pulse_len_0, pulse_sep_0)
        self.dtg.new_block('Block_short', len(sequence))
        self.dtg.set_channel_binary(self.channel, sequence)

        self.filename = './Ramsey_seq.csv'

    def get_short_pulse_seq(self, pulse_len, pulse_sep):
        block_len = pulse_len + pulse_len
        sequence = np.zeros(block_len) + np.ones(pulse_len)
        return list(sequence)
    def get_from_file_seq(self, filename):
        if 'seq.csv' in name[0]:
            file_data = np.genfromtxt(name[0], delimiter=',')
            sequence = np.zeros(np.sum(np.abs(file_data).astype(int)))
            start=0
            for i in file_data:
                seq = np.ones(abs(int(i))) if i>0 else np.zeros(abs(int(i)))
                sequence[start:int(np.abs(i) + start)] = seq
                start = int(np.abs(i)) + start
            return list(sequence)

    @pyqtSlot()
    def on_checkBox_run(self):
        if self.checkBox_run.isChecked():
            self.dtg.run_dtg()
        else:
            self.dtg.stop_dtg()
    @pyqtSlot()
    def on_checkBox_from_file(self):
        if self.checkBox_from_file.isChecked():
            sequence = self.get_from_file_seq(self.filename)
            self.dtg.new_block('Block_file', len(sequence))
            self.dtg.set_channel_binary(self.channel, sequence)
        else:
            pulse_len_0 = self.doubleSpinBox_pulselen.value()
            pulse_sep_0 = self.doubleSpinBox_pulsesep.value()
            sequence = self.get_short_pulse_seq(pulse_len_0, pulse_sep_0)
            self.dtg.new_block('Block_short', len(sequence))
            self.dtg.set_channel_binary(self.channel, sequence)

    @pyqtSlot("double")
    def on_doubleSpinBox_pulselen_valueChanged(self):
        self.pulse_len = self.doubleSpinBox_pulselen.value()
        sequence = get_short_pulse_seq(pulse_len_0, pulse_sep_0)
        self.dtg.set_channel_binary(self.channel, sequence)
    @pyqtSlot("double")
    def on_doubleSpinBox_pulsesep_valueChanged(self):
        self.pulse_sep = self.doubleSpinBox_pulsesep.value()
        block_len, sequence = get_short_pulse_seq(pulse_len_0, pulse_sep_0)
        self.dtg.set_channel_binary(self.channel, sequence)
    def on_comboBox_load(self):
        print('load')
        block_len, sequence = get_short_pulse_seq(pulse_len_0, pulse_sep_0)
        self.dtg.set_channel_binary(self.channel, sequence)
    @pyqtSlot()
    def on_pushButton_load_clicked(self):
        file_dialog = QFileDialog(self)
        name = file_dialog.getOpenFileName(self, 'Open File')
        if 'seq.csv' in name[0]:
            self.filename = name[0]
            name_txt = os.path.basename(name[0])
            self.comboBox_load.insertItem(2, name_txt[:-4])
            self.comboBox_load.setCurrentIndex(2)
            sequence = np.genfromtxt(name[0], delimiter=',')
            self.dtg.set_channel_binary(self.channel, sequence)
        else:
            print('wrong file?')
        file_dialog.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MyApplication = MainApp()
    MyApplication.show() # Show the form
    sys.exit(app.exec_()) # Execute the app