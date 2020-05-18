import numpy as np
import TimeTagger as tt
from TimeTagger import createTimeTagger, Dump, Correlation, Histogram, Counter, TimeTagStream, TimeTagStreamBuffer, GatedChannel, DelayedChannel, Combiner
import yaml
import sys

class TT:
    def __init__(self, parameters, runTest=False):
        self.__dict__.update(parameters)
        try:
            self.tagger = createTimeTagger()
            self.tagger.reset()
            print(f"Tagger initialization successful: {self.tagger.getSerial()}")
        except RuntimeError:
            print(f"\nCheck if the TimeTagger device is being used by another instance.")
            sys.exit()

        if runTest: 
            print("RUNNING WITH TEST SIGNAL!")
            for i in self.testSignals:
                self.tagger.setTestSignal(i, True)

        for idx, delay_t in enumerate(self.delayTimes):
                if delay_t != 0:
                    self.tagger.setInputDelay(delay=delay_t, channel = idx+1)

        self.hist_1 = Histogram(self.tagger, 
                                self.currentChan1[0], 
                                self.trigChans[0], 
                                self.binWidth1, 
                                self.numBins1)

        self.hist_2 = Histogram(self.tagger, 
                                self.currentChan2[0], 
                                self.trigChans[0], 
                                self.binWidth2, 
                                self.numBins2)

        self.virtChannel_start = DelayedChannel(self.tagger, 
                                    input_channel=self.trigChans[0], 
                                    delay=self.gate_delay[0])

        self.virtChannel_end = DelayedChannel(self.tagger, 
                                input_channel=self.trigChans[0], 
                                delay=self.gate_delay[1])

        self.gated_channel = GatedChannel(self.tagger, 
                            input_channel=self.gatedChan[0], 
                            gate_start_channel = self.virtChannel_start.getChannel(), 
                            gate_stop_channel = self.virtChannel_end.getChannel())
        
        g2_start, g2_end = self.combiner_channels(self.g2_channels_start, self.g2_channels_end)
        
        self.corr = Correlation(self.tagger, 
                            g2_start, 
                            g2_end, 
                            self.binWidth1, 
                            self.numBins1)

        self.counter = Counter(self.tagger,
                            self.counter_channels, 
                            self.binWidthCounter, 
                            self.numBinsCounter)
        
    def combiner_channels(self, channels_start, channels_end):
        channels_start = Combiner(self.tagger, channels_start).getChannel()
        channels_end = Combiner(self.tagger, channels_end).getChannel()
        self.tagger.sync()
        return channels_start, channels_end
