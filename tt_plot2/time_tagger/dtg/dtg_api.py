import numpy as np
import pyvisa
class DTG:
    def __init__(self, dtg_adress='TCPI .. ::: :: ;::', channels=[1,2,3,4]):
        # rm = pyvisa.ResourceManager()
        # self.dtg = rm.open_resource(dtg_adress)
        self.channels = channels
        self.current_block = 'Block1'
        self.current_sequence = []

    def outputs_ON(self):
        self.dtg.write('OUTP:STAT:ALL ON;*WAI')
        # return self.dtg.query('is OK?')
    def outputs_OFF(self):
        self.dtg.write('OUTP:STAT:ALL OFF;*WAI')
        # return self.dtg.query('is OK?')
    def run_dtg(self):
        self.dtg.write('OUTP:STAT:ALL ON;*WAI')
        self.dtg.write('TBAS:RUN ON')
        state = 0 if int(self.dtg.query('TBAS:RUN?')) == 1 else -1
        return state

    def stop_dtg(self):
        self.dtg.write('OUTP:STAT:ALL OFF;*WAI')
        self.dtg.write('TBAS:RUN OFF')
        state = 0 if int(self.dtg.query('TBAS:RUN?')) == 0 else -1
        return state

    def new_block(self, nameBlock, length):
        block_length = int(self.dtg.query('BLOC:LENG? "{0}"'.format(nameBlock)))
         if block_length != -1:
            self.dtg.write('BLOC:DEL "{0}"'.format(nameBlock))

        self.dtg.write('BLOC:NEW "{0}", {1}'.format(nameBlock, length))
        self.dtg.query('*OPC?')
        self.dtg.write('BLOC:SEL "{0}"'.format(nameBlock))
        return self.dtg.query('*OPC?')

    def select_block(self, nameBlock):
        self.dtg.write('BLOC:SEL "{0}"'.format(nameBlock))
        self.dtg.query('*OPC?')
        return self.dtg.query('*OPC?')

    def get_frequency(self):
        return float(self.dtg.query('TBAS:FREQ?'))

    def set_frequency(self, sample_rate):
        self.dtg.write('TBAS:FREQ {0:e}'.format(sample_rate))
        return self.get_sample_rate()

    def set_channel_binary(self, channel=['A', 1], sequence):
        """
        Mostly taken from the QUDI Uni Ulm
        """
        max_blocksize = 8 * 800
        dlen = len(sequence)
        written = 0
        start = 0
        # when there is more than 1MB of data to transfer, split it up
        while dlen >= max_blocksize - 8:
            end = start + max_blocksize
            # print(channel, '->', c, 'start', start, 'end', end, 'len', dlen, 'packed', len(bytestr))
            self.dtg.write_binary_values(
                'PGEN{0}:CH{1}:BDATA {2},{3},'.format(channel[0], channel[1], start, end - start),
                sequence,
                datatype='B'
            )
            print(self.dtg.query('*OPC?'))
            written += end - start
            dlen -= end - start
            start = end
        return written
