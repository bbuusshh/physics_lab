from qutip import *
import numpy as np
from matplotlib import pyplot as plt
import itertools
import imageio

class Pulse:
    def __init__(self):
        self.gamma = 1 # decay rate, sets the overall timescale of the system
        self.global_dt = 0.01 # default time step
        self.minpointsperpulse = 5.0             # minimum time resolution of a pulse
    # define function E(t), a gaussian.
    def pulse_shape(self, t, args):
        width = args['width']
        norm = args['norm']
        offset=args['t0']
        return norm/(2*width*np.sqrt(np.pi)) * np.exp(-((t - offset) / (2.0 * width))**2)

    def pulse_shape_exp(self, t, args):
        width = args['width']
        norm = args['norm']
        offset=args['t0']
        return norm/(2*width*np.sqrt(np.pi)) * np.exp(-np.abs((t - offset) / (2.0 * width)))
    # pulse normalization function
    def pulsenormconst(self, args):
        args['norm'] = 1.0
        tlist = self.tlistfunc(args)
        unnorm_pulse = [self.pulse_shape(t, args) for t in tlist]
        unnorm_pulse_area = np.trapz(unnorm_pulse, tlist)
        return 1/unnorm_pulse_area

    # in order to speed up the simulation for shorter pulses, we take advantage of
    # QuTiP's built in support for variable time steps. This function generates a
    # the list of times for which system dynamics will be calculated.
    def tlistfunc(self, args):
        width = args['width']
        norm = args['norm']
        tmin = args['tmin']
        tmax = args['tmax']
        offset=args['t0']
        tlist = []
        # if the global time resolution satisfies the minimum number of points per
        # pulse, make time list a simple linearly-spaced set of points.
        if width/self.minpointsperpulse > self.global_dt:
            tlist = np.linspace(tmin, tmax, int((tmax - tmin)/self.global_dt))
        # otherwise, increase resolution inside the pulse only.
        else:
            tlist1 = np.linspace(tmin, width*offset*2.0, \
                                 int(self.minpointsperpulse*(offset*2.0 - tmin)))[:-1]
            tlist2 = np.linspace(width*offset*2.0, tmax, \
                                 int((tmax - width*offset*2.0)/self.global_dt))
            tlist = np.append(tlist1, tlist2)
        return np.array(tlist)

    def prepare_pulse(self, width, pulse_area=1, bg_light=0, offset=3, tmin=0.0, tmax=100):
        self.pulse_t_offset = offset
        pulseargs = {'width':width, 'tmin':tmin, 'tmax': tmax, 'bg_light':bg_light, 't0':offset} # define pulse properties
        pulseargs['norm'] = pulse_area# * self.pulsenormconst(pulseargs)    # compute numerically the normalization constant
        tlist = self.tlistfunc(pulseargs)                                  # generate time list
        pulse = np.array([self.pulse_shape(t, pulseargs) for t in tlist])           # generate pulse shape
        return np.array(tlist), np.array(pulse), pulseargs

def remove_key(args, keys):
    args_ = args.copy()
    for key in keys:
        if key in list(args_.keys()):
            del args_[key]
    return args_

def generate_animation_imgs(evolve_delta_k, K_range):
    Deltas = np.linspace(-1,1, 100)
    imgs = []
    for k in K_range:
        results = []
        for Delta in Deltas:
            tlist, result=evolve_delta_k(Delta, k)
            results.append(result)
        img = np.zeros(len(tlist))
        for res in results:
            img = np.vstack((img, np.array(res.expect[0])))
        imgs.append(img.T)
    return imgs


def animate_bloch(expect_sigmas, duration=0.1, name='bloch.gif', save_all=False):
    b = Bloch()

    points = np.vstack(expect_sigmas[2:])
    b.vector_color = ['r']
    b.view = [-40,30]
    images=[]
    b.point_marker = ['o']
    b.point_size = [30]
    b.point_color = ['g']
    for i in range(int(points.shape[1]/100)):
        b.clear()
        b.point_color = ['b']
        b.add_points(expect_sigmas[2:], meth='l')
        b.point_color = ['r']
        b.add_points(points[:,i*100], meth='m')
        if save_all:
            b.save(dirc='tmp') #saving images to tmp directory
            filename="tmp/bloch_%01d.png" % i
        else:
            filename='temp_file.png'
            b.save(filename)
        images.append(imageio.imread(filename))

    imageio.mimsave(name, images, loop=0, duration=duration)


def animate_2d_plots(array_imgs, varying_param, name, duration=0.25, save_all=False):
    images=[]
    for i in range(len(varying_param)):
        plt.figure(figsize=(10, 8))
        plt.imshow(array_imgs[i], aspect='auto')
        if save_all:
             #saving images to tmp directory
            filename="tmp/bloch_%01d.png" % i
            plt.savefig(filename)
        else:
            filename='temp_file.png'
            plt.savefig(filename)
        images.append(imageio.imread(filename))

    imageio.mimsave(name, images, loop=0, duration=duration)

