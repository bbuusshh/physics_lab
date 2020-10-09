import numpy as np
from scipy import optimize
from scipy import stats
from labtools.tools import get_trig_len

def align_spectra(data, line_trig=8, pix_trig=7):
    d_1=np.split(data, np.where(data['channel'] == line_trig)[0][1:])
    d_lines = np.array(list(map(lambda x: np.split(x, np.where(x['channel'] == pix_trig)[0][1:]),d_1)))
    center = get_trig_len(data, trig_ch=line_trig)/2
    for line in d_lines:
        spectr = [len(px) for px in line]
        t = [px[0]['time'] - line[0][0]['time'] for px in line]
        mx = np.where(spectr == np.max(spectr))[0][0]
        shift = t[mx] - center
        line[0][0]['time'] = line[0][0]['time'] + shift
    data = data[np.argsort(data['time'])]
    return data

def scan3Darray(data, line_trig=7, px_trig=8, binNum=100, d_lines_offset=1):
    """
    Input data is output of assign_clicks_to_trigs from tools
    """

    d_1=np.split(data, np.where(data['channel'] == px_trig)[0][1:])
    d_lines = np.array(list(map(lambda x: np.split(x, np.where(x['channel'] == line_trig)[0][1:]),d_1)))
    
    lines_pxs = int(round(stats.mode([len(i) for i in d_lines])[0][0] - 3))
    #TODO: dont through away broken lines (caused by wrong shift)
    d_lines = list(filter(lambda x: (len(x) > lines_pxs) & (len(x) < lines_pxs*1.05), d_lines))
    print("lines_pxs: ", lines_pxs)
    img = np.zeros((lines_pxs, binNum))

    #TODO:  throw away lines with not full scan
    for line_x in d_lines[d_lines_offset:-d_lines_offset]:
        line = np.zeros(binNum)
        for px in line_x[0:lines_pxs-1]:
            y,x = np.histogram(px['time_from_trig'], bins=binNum)
            line = np.vstack((line, y))
        img = np.dstack((img, line))

    return img
