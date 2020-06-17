# sudo chmod 666 /dev/ttyUSB0  

import time
import numpy as np 
from matplotlib import pyplot as plt
from  keithley2600 import Keithley2600, ResultTable

k = Keithley2600('ASRL/dev/ttyUSB0::INSTR')
k.read_termination = '\r\n'
k.write_termination = '\r\n'
# create ResultTable with two columns
rt = ResultTable(column_titles=['Voltage', 'Current'], units=['V', 'A'],
                 params={'recorded': time.asctime(), 'sweep_type': 'iv'})

# create live plot which updates as data is added
# rt.plot(live=True)

# measure some currents
for v in np.arange(-20,1):
    k.applyVoltage(k.smua, v)
    i = k.smua.measure.i()
    rt.append_row([v, i])
k.smua.source.levelv = 0

for v in np.arange(-20,1)[::-1]:
    k.applyVoltage(k.smua, v)
    i = k.smua.measure.i()
    rt.append_row([v, i])
k.smua.source.levelv = 0
# save the data
rt.save('iv_curve_cryo_warmer.txt')

