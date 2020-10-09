import numpy as np
from scipy.ndimage import gaussian_filter
from labtools.tools import get_trig_len
from labtools.time_freq_scan import align_spectra
from scipy.optimize import curve_fit

def get_channel_shifts(data, trig, estimation = None):
    """
    Get the shifts by finding the rising edge of ONE pulse for different channels
    Only for the cases that pulse rising time smaller than 15ns.

    """	
    # __int__
    shifts = np.zeros(4)
    bins_wid = 100
    bins = int(trig / bins_wid)
    # histogram the data
    for ch in [1,2,3,4]:
        y, x = np.histogram(data['time_from_trig'][data['channel']==ch], bins = bins, range=(0, trig))
        # smooth out noise
        smoothed = gaussian_filter(y, 3.)
        # find a 10ns period base
        y_firstpeak = np.where(y == np.max(y))[0][0]
        # shift range estimation
        if estimation != None:
            y_firstpeak = np.where(y == np.max(y[:round(estimation/bins_wid)+250]))[0][0]
        base_start = int(y_firstpeak - 250) % bins 
        base_stop = int(y_firstpeak - 150) % bins
        base = np.mean(y[base_start:base_stop])
        # Determine the rising by 3std over base
        std = (y[base_start:base_stop] - base).std()
        not_base = smoothed > (base + 3 * std) 
        # finding the rising edge in the range of 15ns before the peak
        shifts[ch-1] = x[np.where(not_base==True)[0][(np.where(not_base == True)[0] - base_stop) % bins < 150][0]]
    return shifts


RAMSEY_PARAMS = {
        "No_of_steps": 100,
        "step_time": 20, #ms
        "back_time": 200, #ms
        "pulse_length": 2100, #ps
        "rabi_pulse_length": 30000, #ps
        "start_tau": 0, #ps
        "stop_tau": 60000, #ps 
        "tau_Inc": 300, #ps
        "blank_time":90000, #ps
        "line_trig": 6,
        "pix_trig": 7
}
class Ramsey_project:
    def __init__(self, data, parameters=RAMSEY_PARAMS):
        self.__dict__.update(parameters)
        self.pixel_number = int(self.back_time / self.step_time + self.No_of_steps)
        self.step_cut = round(round(int(self.back_time / self.step_time + self.No_of_steps)*0.45) / 2)*2

    def funcLorentz(self, w, *params):
        gamma = params[0]
        norm = params[1]
        w_0 = params[2]
        bg = params[3]
        y = bg + gamma * norm/((w - w_0)**2 + gamma**2/4)
        return y

    def decay(self, t, T, a0, b0):
        return a0*np.exp(-t/T) + b0


    def Ramsey_functional(self, tau,  T_2, omegarabi, Delta, A, B):
        T_1 = self.T_1
        pulse_length = round(self.pulse_length / 1000, 1)
        delta = Delta * 2 * np.pi /1000
        c = omegarabi**2 + delta**2
        w1 = np.sqrt(c) * pulse_length / 2
        return np.real( omegarabi**2 / c * ((np.cos(w1)**2*np.sin(w1)**2 + np.sin(w1)**4 *delta**2 /c - np.sin(w1)**4 * omegarabi**2/c)*np.exp(-tau/T_1)
               +(np.cos(w1)**2 * np.sin(w1)**2 + 2j * np.cos(w1) * np.sin(w1)**3 * delta / np.sqrt(c) - np.sin(w1)**4*delta**2/c) *np.exp(-tau/T_2)*np.exp(1j*delta*tau)   
               +(np.cos(w1)**2*np.sin(w1)**2 - 2j * np.cos(w1)*np.sin(w1)**3 * delta / np.sqrt(c) - np.sin(w1)**4*delta**2/c) *np.exp(-tau/T_2)*np.exp(-1j*delta*tau)
               +np.sin(w1)**2*np.cos(w1)**2 +np.sin(w1)**4))*A + B


    def sec_peak_trigger(self,):
        event_num = int((self.stop_tau - self.start_tau)/ self.tau_Inc +1)
        trigger = []
        sec_peak = self.rabi_pulse_length + self.blank_time + 2*self.pulse_length
        trigger.append(sec_peak)
        for i in range(1, event_num):
            sec_peak = sec_peak + self.blank_time + i*self.tau_Inc + 2*self.pulse_length
            trigger.append(sec_peak)
        return trigger

    def ramsey_process(self, data, trigger, channels = [1,2,3,4], tau_0 = 1_500, inte_cut = 60_000):
        event_num = int((self.stop_tau - self.start_tau)/ self.tau_Inc +1)
        start_num = int((tau_0 - self.start_tau) / self.tau_Inc)
        tau = np.zeros(event_num-start_num)
        flu = np.zeros(event_num-start_num)
        for i in range(event_num-start_num):
            tau[i] = (tau_0 + i*self.tau_Inc)/1000 
            flu[i] = np.count_nonzero((data['time_from_trig'][(np.isin(data['channel'], channels)) & (data['time_from_trig'] > 0)] - trigger[i+start_num] > 0) & (data['time_from_trig'][(np.isin(data['channel'],   channels)) & (data['time_from_trig'] > 0)] - trigger[i+start_num] < inte_cut))
        return tau, flu

    def align(self, data):
        """
        Align the spectrum
        """
        d_1=np.split(data, np.where(data['channel'] == self.line_trig)[0][1:])
        d_lines = np.array(list(map(lambda x: np.split(x, np.where(x['channel'] == self.pix_trig)[0][1:]),d_1)))
        d_lines = d_lines[1:]
        pixel_d = 3
        d_lines = list(filter(lambda x: (len(x) > self.pixel_number - pixel_d) & (len(x) < self.pixel_number + pixel_d), d_lines))# Only keep the lines which has right pixel numbers
        grid_spectr = [len(px) for px in d_lines[0]]
        for line in d_lines[1:]:
            spectr = [len(px) for px in line]
            grid_spectr = np.vstack((grid_spectr,spectr))
        mx = [] 
        mx.append(np.where(grid_spectr[0] == np.max(grid_spectr[0]))[0][0])
        for i in range(1,len(grid_spectr)):
            altern = np.where(grid_spectr[i] == np.max(grid_spectr[i]))[0][0]
            if mx[i-1] - altern > 5/6 * self.pixel_number:
                altern = altern + self.pixel_number
            if abs(mx[i-1] - altern) > 1/4 * self.pixel_number:
                altern = mx[i-1]
            mx.append(altern)# find the middle point by determining the maximum point in the spectrum
        for i in range(0, len(grid_spectr)):
            grid_spectr[i] = np.roll(grid_spectr[i],round(self.step_cut/2)-mx[i])
        grid_spectr_cut = []
        for i in range(0, len(grid_spectr)):
            grid_spectr_cut.append(grid_spectr[i][0:self.step_cut])
        lorentzfit_x = np.arange(0,self.step_cut,1)
        popt_Lorentz_spectr = np.zeros((len(grid_spectr_cut),4))
        bounds=[[0, -1e3, -1e3, -1e3],[1e6, 1e10, 1e5, 1e10]]
        for i in range(len(grid_spectr_cut)):
            popt_Lorentz_spectr[i], _ = curve_fit(self.funcLorentz, lorentzfit_x, grid_spectr_cut[i], p0=[20, 5000, round(self.step_cut/2), 1000], bounds=bounds) # fit each line with Lorentzian to get the fine shifts
        fine_shift = []
        for i in range(len(grid_spectr_cut)):
            fine_shift.append(round(popt_Lorentz_spectr[i][2]-round(self.step_cut/2)))
        for i in range(len(grid_spectr_cut)):
            mx[i] = mx[i] + int(fine_shift[i])
        for i in range(0, len(d_lines)):
            d_lines[i] = np.roll(d_lines[i],round(self.step_cut/2)-mx[i])
        d_lines_cut = d_lines[0][0:self.step_cut]
        for i in range(1,len(d_lines)):
            d_lines_cut = np.vstack((d_lines[i][0:self.step_cut],d_lines_cut))
        return d_lines_cut

    def ramsey3darray(self, d_lines_cut):
        line_x = d_lines_cut[0]
        trigger = self.sec_peak_trigger()
        tau, line = self.ramsey_process(line_x[0], trigger)
        for px in line_x[1:]:
            _, y = self.ramsey_process(px,trigger)
            line = np.vstack((line, y)) 
        img = line
        for line_x in d_lines_cut[1:]:
            tau,line = self.ramsey_process(line_x[0],trigger)
            for px in line_x[1:]:
                _, y = self.ramsey_process(px,trigger)
                line = np.vstack((line, y))
            img = np.dstack((img, line))
        return img, tau

    def rabi3darray(self, d_lines_cut, bin_width = 100):
        seq_length = self.rabi_pulse_length + self.blank_time
        bin_Num = int(seq_length / bin_width) - 1
        line_x = d_lines_cut[0]
        line, _ = np.histogram(line_x[0]['time_from_trig'], bins=bin_Num, range=(bin_width,seq_length))
        for px in line_x[1:]:
            y, _ = np.histogram(px['time_from_trig'], bins=bin_Num, range=(bin_width,seq_length))
            line = np.vstack((line, y)) 
        rabi_img = line
        for line_x in d_lines_cut[1:]:
            line, _= np.histogram(line_x[0]['time_from_trig'], bins=bin_Num, range=(bin_width,seq_length))
            for px in line_x[1:]:
                y, _ = np.histogram(px['time_from_trig'], bins=bin_Num, range=(bin_width,seq_length))
                line = np.vstack((line, y))
            rabi_img = np.dstack((rabi_img, line))
        rabi_x = np.linspace(bin_width/1000,seq_length/1000,bin_Num)
        return rabi_img, rabi_x
