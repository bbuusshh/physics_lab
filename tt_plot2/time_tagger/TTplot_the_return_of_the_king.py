#! /usr/bin/env python3

import os
from os.path import join, getsize, isfile
import sys
import time
import io
import yaml

import numpy as np
import pandas as pd
from scipy import signal
from matplotlib import cm
from matplotlib import pyplot as plt

import pyqtgraph as pg
import pyqtgraph.exporters
from PyQt5.QtCore import QTimer, QThread, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
from PyQt5.QtWidgets import QApplication, QMainWindow,  QInputDialog, QLineEdit
from PyQt5 import QtGui

from tt_layout import Ui_MainWindow
from TimeTagger import createTimeTagger, Dump, Correlation, Histogram, Counter, TimeTagStream, TimeTagStreamBuffer, GatedChannel, DelayedChannel, Combiner

sys.path.insert(0, '/home/cryo/lab/code/scripts/')
pars_file = open("/home/cryo/lab/code/tt-gui/params.yaml", 'r')
PARAMS = yaml.safe_load(pars_file)


UPDATE_INTERVALL = 50   # update intervall in ms
# print(PARAMS)

# buffer = []
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tag = TT(PARAMS)
        self.data_times = np.array([])
        self.data_channels = np.array([])
        self.trig_len = 0
        self.gate_corr = False
        self.gate_scan = False
        self.m_ui = Ui_MainWindow()
        self.m_ui.setupUi(self)

        self.threadpool = QThreadPool()
        self.tick_counter = 0
        self.sec = 0    

        # SET BINS
        self.m_ui.binsTextField.returnPressed.connect(self.setBins)
        self.m_ui.binsWidthTextField.returnPressed.connect(self.setBins)
        self.m_ui.binsTextField2.returnPressed.connect(self.setBins2)
        self.m_ui.binsWidthTextField2.returnPressed.connect(self.setBins2)

        # SET REFRESH TIME
        self.m_ui.refreshTextField.returnPressed.connect(self.setRefreshTime)
        self.m_ui.refreshTextField2.returnPressed.connect(self.setRefreshTime2)

        # SET DELAY TIME
        self.m_ui.delayTextField.returnPressed.connect(self.delayTime)
        self.m_ui.delayTextField2.returnPressed.connect(self.delayTime2)
        
        # DUMP DATA
        self.m_ui.dumpFile.returnPressed.connect(self.dumpTextField)
        self.m_ui.saveToggle.toggled.connect(self.dumpData)
        self.m_ui.actionNew_cooldown.triggered.connect(self.new_cooldown)    

        # SELECT CHANNEL1
        self.m_ui.chSelect.setCurrentIndex(self.tag.currentChan[0] - 1)
        self.m_ui.chSelect.currentTextChanged.connect(self.setChannel)

        self.m_ui.chSelect2.setCurrentIndex(self.tag.currentChan2[0] - 1)
        self.m_ui.chSelect2.currentTextChanged.connect(self.setChannel2)

        # NEW MEASUREMENT
        self.m_ui.button.clicked.connect(self.newMeasurement)
        self.m_ui.button2.clicked.connect(self.newMeasurement)

        # FREEZE
        self.m_ui.freeze.clicked.connect(self.switch)
        self.freeze = False
        self.m_ui.lr42.sigRegionChanged.connect(self.regionChanged42)
        self.m_ui.lr41.sigRegionChanged.connect(self.regionChanged41)

        # SAVE PARAMS
        self.m_ui.saveButt.clicked.connect(self.save_Params)

        #LOAD PARAMS
        self.m_ui.loadButt.clicked.connect(self.load_Params)

        # PLOT DATA
        self.m_ui.saveFig.clicked.connect(self.saveFigure)

        self.font = QtGui.QFont()
        self.font.setPixelSize(20)
        self.trig_len=150   # in ns
        self.p1 = self.m_ui.win.addPlot(rowspan=2)
        self.p1 = self.plot_curve(self.p1, return_p=True)
        #ax = self.p1.getAxis('bottom')
       
        #ticks = np.linspace(0, self.trig_len, 10)
        #ax.setTicks([[(v, str(round(v))) for v in ticks ]])
        self.curve_hist_1 = self.p1.plot()

        self.p1_2 = self.m_ui.win2.addPlot(rowspan=2)
        self.p1_2 = self.plot_curve(self.p1_2, return_p=True)
        #ax = self.p1_2.getAxis('bottom')
        #ticks = np.linspace(0, self.trig_len, 10)
        #ax.setTicks([[(v, str(round(v))) for v in ticks ]])
        self.curve_hist_2 = self.p1_2.plot()

        self.p2 = self.m_ui.win_2.addPlot()
        self.curve_corr_1 = self.plot_curve(self.p2) 

        self.p2_2 = self.m_ui.win_2_2.addPlot()
        self.curve_corr_2 = self.plot_curve(self.p2_2) 

        self.p31 = self.m_ui.win_3.addPlot()
        self.p31 = self.plot_curve(self.p31, return_p=True)
        self.p31.addItem(self.m_ui.lr41)
        self.curve_freeze_1 = self.p31.plot()

        self.m_ui.win_3.nextRow()
        self.p32 = self.m_ui.win_3.addPlot()
        self.p32 = self.plot_curve(self.p32, return_p=True)
        self.p32.addItem(self.m_ui.lr42)
        self.curve_freeze_2 = self.p32.plot()


        self.p3_2 = self.m_ui.win_3_2.addPlot()
        self.p3_2 = self.plot_curve(self.p3_2, return_p=True) 
        self.curve_count_rate_2 = self.p3_2.plot()

        self.init_params_ui()

        self.timer = QTimer()
        self.loop_dump = 0
        self.loop_refresh = [0,0]
        self.updateTime = 50

        self.timer.timeout.connect(self.update)
        self.timer.start(self.updateTime)

        self.moving_average_upper = None
        self.moving_average_lower = None

    def new_cooldown(self):
        text, okPressed = QInputDialog.getText(self, "Cooldown Name","Name:", QLineEdit.Normal, "")
        if okPressed and text:
            if text not in os.listdir(self.tag.dataDir):
                self.tag.saveDir = f"{self.tag.dataDir}/{text}"
                os.makedirs(self.tag.saveDir)
                self.save_Params()
                print("New folder created")
            else:
                print("Such a name already exists!")
            
    def plot_curve(self, p, return_p = False):
        p.setLabel('left', text='kcps')
        p.setLabel('bottom', text='T, ns')
        p.showGrid(x=True, y=True, alpha=0.2)
        p.getAxis("bottom").tickFont = self.font
        p.getAxis("left").tickFont = self.font
        p.getAxis("bottom").setStyle(tickTextOffset = 20)
        if return_p:
            return p
        else:
            return p.plot()

    def saveFigure(self):
        name = self.m_ui.figureName.text()
        listDir = os.listdir(self.tag.saveDir)

        if name:
            name = f"{self.tag.saveDir}/{name}_figures_{str(len([i for i in listDir if name in i]))}"
        else:
            name = f"{self.tag.saveDir}/default_figures_{str(len([i for i in listDir if 'default_figures' in i]))}"
        os.makedirs(name)

        datas = ["hist_1", "corr_1", "hist_2", "corr_2"]
        for i in datas:
            data = self.__dict__['tag'].__dict__[i].getData()
            plt.plot(data)
            plt.savefig(f"{name}/{i}.pdf")
            plt.clf()
            np.savetxt(f"{name}/{i}.csv", data, delimiter=",")
        print("Image saved")

    def regionChanged41(self):
        regionOf41 = self.m_ui.lr41.getRegion()
        self.m_ui.lr42.setRegion(regionOf41)

    def regionChanged42(self):
        regionOf42 = self.m_ui.lr42.getRegion()
        self.m_ui.lr41.setRegion(regionOf42)

    def gate_button(self):
        self.gate = not self.gate

    def delayTime(self):
        self.delayTime = int(self.sender().text())
        self.tag.delayTimes[self.tag.currentChan[0]-1] = self.delayTime
        if self.tag.currentChan[0] in [9,10]:
            self.tag.virtChannel.setDelay(delay=self.delayTime)
        else:
            self.tag.tagger.setInputDelay(delay=self.delayTime, channel = self.tag.currentChan[0])
        self.newMeasurement()

    def delayTime2(self):
        self.delayTime2 = int(self.sender().text())
        self.tag.delayTimes[self.tag.currentChan2[0]-1] = self.delayTime2
        if self.tag.currentChan2[0] in [9,10]:
            self.tag.virtChannel.setDelay(delay=self.delayTime2)
        else:
            self.tag.tagger.setInputDelay(delay=self.delayTime2, channel = self.tag.currentChan2[0])
        self.newMeasurement()

    def setRefreshTime(self):
        self.tag.refreshTime = int(self.sender().text())
        self.moving_average_upper = int(self.sender().text())

    def setRefreshTime2(self):
        self.tag.refreshTime2 = int(self.sender().text())
        self.moving_average_lower = int(self.sender().text())

    def switch(self):
        self.freeze = not self.freeze

    def setBins(self):
        self.tag.numBins = int(self.m_ui.binsTextField.text())
        self.tag.binWidth = int(self.m_ui.binsWidthTextField.text())
        print(f"Number of bins: {self.tag.numBins}\tbin width:{self.tag.binWidth}")

    def setBins2(self):
        self.tag.numBins2 = int(self.m_ui.binsTextField2.text())
        self.tag.binWidth2 = int(self.m_ui.binsWidthTextField2.text())
        print(f"Number of bins: {self.tag.numBins2}\tbin width:{self.tag.binWidth2}")

    def setCounterBins(self):
        self.tag.numBinsCounter = int(self.m_ui.binsCounterTextField.text())
        self.tag.binWidthCounter = int(self.m_ui.binsWidthCounterTextField.text())
        print(f"Number of bins: {self.tag.numBinsCounter}\tbin width:{self.tag.binWidthCounter}")

    def setChannel(self):
        ch = self.sender()
        print(ch.currentText())
        if ch.currentText() == "all":
            self.tag.currentChan = [i for i in self.tag.allChans if i not in self.tag.trigChans]
            print(self.tag.currentChan)
            self.newMeasurement()
            return
        print("setChannel", self.m_ui.chSelect.currentIndex() + 1)
        self.tag.currentChan = [self.m_ui.chSelect.currentIndex() + 1]
        self.newMeasurement()

    def setChannel2(self):
        ch = self.sender()
        print(ch.currentText())
        if ch.currentText() == "all":
            self.tag.currentChan2 = [i for i in self.tag.allChans if i not in self.tag.trigChans]
            print(self.tag.currentChan2)
            self.newMeasurement()
            return
        print("setChannel", self.m_ui.chSelect2.currentIndex() + 1)
        self.tag.currentChan2 = [self.m_ui.chSelect2.currentIndex() + 1]
        self.newMeasurement()

    def dumpData(self):
        checkBox = self.sender()

        if checkBox.isChecked():
            self.tag.setDumpPath(self.m_ui.dumpFile.text())
            self.tag.tagger.setConditionalFilter(filtered=self.tag.trigChans, trigger = self.tag.apdChans)
            self.tag.dump = Dump(self.tag.tagger, self.tag.dumpPath, self.tag.maxDumps,\
                                self.tag.allChans)
            self.tag.dump.start()
            self.howIsTheDump()
        else:
            self.tag.tagger.setConditionalFilter(filtered=[], trigger=[])
            self.tag.dump.stop()
            self.howIsTheDump()
            # if f"{self.tag.dumpPath.split('/')[-1]}_imgs" not in  os.listdir():
            #     os.makedirs(f"{self.tag.dumpPath}_imgs")
            #     plt.plot(self.tag.hist_1.getData())
            #     plt.savefig(f"{self.tag.dumpPath}_imgs/hist.pdf")
            #     plt.clf()
            #     plt.plot(self.tag.corr_1.getData())
            #     plt.savefig(f"{self.tag.dumpPath}_imgs/corr.pdf")
            #     plt.clf()
            #     np.savetxt(f"{self.tag.dumpPath}_imgs/hist.csv", self.tag.hist_1.getData(), delimiter=",")
            #     np.savetxt(f"{self.tag.dumpPath}_imgs/corr.csv", self.tag.corr_1.getData(), delimiter=",")
            #     np.savetxt(f"{self.tag.dumpPath}_imgs/hist2.csv", self.tag.hist_2.getData(), delimiter=",")
            #     np.savetxt(f"{self.tag.dumpPath}_imgs/corr2.csv", self.tag.corr_2.getData(), delimiter=",")

    def save_Params(self):
        # SAVE PARAMS:
        PARAMS['delayTimes'] = self.tag.delayTimes
        PARAMS['saveDir'] = self.tag.saveDir
        # print(PARAMS)
        with open('params.yaml', 'w', encoding='utf8') as outfile:
             yaml.dump(PARAMS, outfile, default_flow_style=True, allow_unicode=True)

    def load_Params(self):
        pars_file = open("/home/cryo/lab/code/tt-gui/params.yaml", 'r')
        PARAMS = yaml.safe_load(pars_file)
        self.tag = TT(PARAMS)
        self.newMeasurement()

    def dumpTextField(self):
        self.tag.setDumpPath(self.sender().text())
        self.m_ui.saveToggle.setChecked(False)

    def newMeasurement(self):
        self.tag.tagger.clearOverflows()
        print(self.tag.currentChan)
        self.tag.hist_1 = Histogram(self.tag.tagger, self.tag.currentChan[0], self.tag.trigChans[0], self.tag.binWidth, self.tag.numBins)

        self.tag.virtChannel.setDelay(self.tag.delayTimes[8])
        self.tag.hist_2 = Histogram(self.tag.tagger, self.tag.gated_channel_1.getChannel(), self.tag.trigChans[0], self.tag.binWidth, self.tag.numBins)#Histogram(self.tag.tagger, virtChannel, self.tag.trigChans[0], self.tag.binWidth2, self.tag.numBins2)
        
        self.tag.corr_1 = Correlation(self.tag.tagger, 1, 3, self.tag.binWidth, self.tag.numBins)
        self.tag.corr_2 = Correlation(self.tag.tagger, self.tag.corr_channels_1, self.tag.corr_channels_2, self.tag.binWidth, self.tag.numBins)

        self.tag.counter = Counter(self.tag.tagger, [self.tag.gated_channel_1.getChannel()], self.tag.binWidthCounter, self.tag.numBinsCounter)
        region = self.m_ui.lr41.getRegion()

        self.init_params_ui()

        print("channel", self.tag.currentChan[0], "trig", self.tag.trigChans[0])
        print("width", 1e6*abs(region[1] - region[0])/(self.tag.numBins * self.tag.binWidth), "ns")
        self.m_ui.freezeWindowSize.setText(str(round(1e-6*abs(region[1] - region[0])*(self.tag.numBins * self.tag.binWidth))) + ' ns')
        print("New Measurement")
        print(f"Delays: {self.tag.delayTimes}")
        print(f"Current path: {self.tag.saveDir}")

    def get_trig_len(self, data_times, data_channels):
        sh_ch = np.roll(data_channels[data_channels == self.tag.trigChans[0]], -1)
        sh_time = np.roll(data_times[data_channels == self.tag.trigChans[0]], -1)
        tr = sh_time[sh_ch == self.tag.trigChans[0]] - data_times[data_channels == self.tag.trigChans[0]]
        tr = tr[tr>0]
        return tr[tr//np.min(tr) == 1].mean()/1000 # in ns

    def correlate_chs_start(self, sender):
        self.tag.corr_apdChans_start[int(self.sender().objectName())] = sender

    def correlate_chs_stop(self, sender):
        print(sender)
        self.tag.corr_apdChans_stop[int(self.sender().objectName())] = sender

    def howIsTheDump(self):
        try:
            if self.tag.dump.isRunning():
                print("", f"Data being dumped to: {self.tag.dumpPath}",
                      f"Size: {getsize(self.tag.dumpPath)/1024**2} MB",
                      sep='\n')
            else:
                print("", "Dump not running.",
                      f"Current dump file: {self.tag.dumpPath}",
                      sep='\n')
        except AttributeError:
            print("No Dump yet!")

    def init_params_ui(self):
        self.m_ui.refreshTextField.setText(str(self.tag.refreshTime))
        self.m_ui.refreshTextField2.setText(str(self.tag.refreshTime2))
        self.m_ui.binsTextField.setText(str(self.tag.numBins))
        self.m_ui.binsTextField2.setText(str(self.tag.numBins2))
        self.m_ui.binsWidthTextField.setText(str(self.tag.binWidth))
        self.m_ui.binsWidthTextField2.setText(str(self.tag.binWidth2))
        self.m_ui.delayTextField.setText(str(self.tag.delayTimes[self.tag.currentChan[0]-1]))
        self.m_ui.delayTextField2.setText(str(self.tag.delayTimes[self.tag.currentChan2[0]-1]))

    def update(self):
        def plot_histog_1():
            self.curve_hist_1.setData(self.tag.hist_1.getData())
        def plot_histog_2():
            self.curve_hist_2.setData(self.tag.hist_2.getData())

        def plot_correlation_1():
            self.curve_corr_1.setData(self.tag.corr_1.getData())
        def plot_correlation_2():
            self.curve_corr_2.setData(self.tag.corr_2.getData())

        def plot_counter():
            data = self.tag.counter.getData()
            self.tag.dataCount.append(data[0][0])
            self.tag.dataCount = self.tag.dataCount[-500:]            
            self.curve_count_rate_2.setData(data[0]/1000)

        def plot_freeze():
            if self.freeze:
                self.curve_freeze_1.setData(self.tag.hist_1.getData())
            else:
                self.curve_freeze_2.setData(self.tag.hist_1.getData())
        #TODO: plot depending on what tab is open
        graphs_1 = [plot_histog_1, plot_correlation_1, plot_freeze]
        graphs_2 = [plot_histog_2, plot_correlation_2, plot_counter]

        graphs_1[self.m_ui.tabWidget_1.currentIndex()]()
        graphs_2[self.m_ui.tabWidget_2.currentIndex()]()

        if self.m_ui.saveToggle.isChecked():
            if self.loop_dump // 20 == 1:
                try:
                    if self.tag.dump.isRunning():
                        self.m_ui.dumpSize.setText(f"{round(getsize(self.tag.dumpPath)/1024**2)} MB")
                except AttributeError:
                    print("No Dump yet!")
                self.loop_dump = 0
            self.loop_dump+=1

        if self.moving_average_upper:
            if not self.sec % self.moving_average_upper:
                hist_buffer = self.tag.hist_1.getData()
                # print("Hist length: ",hist_buffer.shape, hist_buffer[:20], )
                # print(f"Tick counter {self.tick_counter} \t Seconds passed: {self.sec}")

        if self.tag.refreshTime > 0:
            if self.loop_refresh[0] // (20*self.tag.refreshTime)  == 1:
                self.tag.hist_1.clear()
                self.loop_refresh[0] = 0
            self.loop_refresh[0]+=1

        if self.tag.refreshTime2 > 0:
            if self.loop_refresh[1] // (20*self.tag.refreshTime2)  == 1:
                self.tag.hist_2.clear()
                self.loop_refresh[1] = 0
            self.loop_refresh[1]+=1
        

        self.tick_counter = (self.tick_counter + 1) % UPDATE_INTERVALL
        if self.tick_counter == 0:
            self.sec += 1



class TT:
    def __init__(self, parameters):
        self.__dict__.update(parameters)

        try:
            self.tagger = createTimeTagger()
            self.tagger.reset()
            print(f"Tagger initialization successful: {self.tagger.getSerial()}")
        except RuntimeError:
            print(f"\nCheck if the TimeTagger device is being used by another instance.")
            sys.exit()

        if False: 
            print("RUNNING WITH TEST SIGNAL!")
            self.tagger.setTestSignal(3, True)
            self.tagger.setTestSignal(1, True)
            self.tagger.setTestSignal(2, True)
            self.tagger.setTestSignal(4, True)
            self.tagger.setTestSignal(5, True)

        for idx, delay_t in enumerate(self.delayTimes):
                if delay_t != 0:
                    self.tagger.setInputDelay(delay=delay_t, channel = idx+1)

        self.dataCount = []

        self.virtChannel = DelayedChannel(self.tagger, input_channel=5, delay= self.delayTimes[8])
        self.gated_channel_1 = GatedChannel(self.tagger, input_channel=4, gate_start_channel = self.trigChans[0], gate_stop_channel = self.virtChannel.getChannel())
        print("\n virtual_channel \n", self.virtChannel)
        
        
        print("\n gated_channel \n", self.gated_channel_1.getChannel())
        self.corr_channels_1 = Combiner(self.tagger, [1, 2]).getChannel()
        self.corr_channels_2 = Combiner(self.tagger, [3, 4]).getChannel()

        self.comb_ch = Combiner(self.tagger, [1,2,3,4]).getChannel()
        self.tagger.sync()

        self.hist_1 = Histogram(self.tagger, self.currentChan[0], self.trigChans[0], self.binWidth, self.numBins)
        self.hist_2 = Histogram(self.tagger, self.gated_channel_1.getChannel(), self.trigChans[0], self.binWidth2, self.numBins2)
        
        self.corr_1 = Correlation(self.tagger, self.corr_channels_1, self.corr_channels_2, self.binWidth, self.numBins)
        self.corr_2 = Correlation(self.tagger, self.corr_channels_1, self.corr_channels_2, self.binWidth2, self.numBins2)

        self.counter = Counter(self.tagger,[self.gated_channel_1.getChannel()], self.binWidthCounter, self.numBinsCounter)
        
        #self.stream = TimeTagStream(self.tagger, self.maxStream, self.allChans)
        #self.buf = TimeTagStreamBuffer()
        #self.stream.start()
       
        # self.trig_counter.stop()
        # print(self.trig_length)

    def setDumpPath(self, ident=None):
        if not ident:
            ident = '_default'
        counter = 0
        fname = ident + '_' + str(counter) + '.dump'
        fpath = join(self.saveDir, fname)

        while isfile(fpath):
            counter += 1
            fname = ident + '_' + str(counter) + '.dump'
            fpath = join(self.saveDir, fname)
        self.dumpPath = fpath


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())