#!/bin/env python
""" Scanner readout script for labview shit  (c) <gsec 2018> """
import numpy as np
import argparse
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from . import dual_lorentz
import warnings
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def xtract(fname):
    with open(fname, "r") as img:
        whole = img.readlines()
    all_data = [line.rstrip("\n") for line in whole]
    header = all_data[:7]
    data = all_data[8:]
    data_sep = np.array([line.split("\t") for line in data])
    data_trans = data_sep.transpose()
    freq = np.array(data_trans[0]).astype(float)
    data_int = data_trans[1::].astype(float).astype(int)
    return header, data_int, freq


def lorentz(x, intensity, gamma, x0, offset):
    return intensity * gamma ** 2 / ((x - x0) ** 2 + gamma ** 2) + offset


def opt(freq, curve):
    totx = len(freq)
    xd = np.linspace(0, totx, totx)
    popt, pcov = curve_fit(lorentz, xd, curve)  # , sigma=1/np.log(curve+1))
    return popt


def opti_plot(freq, line, count=1):
    p = opt(freq, line)
    x = np.linspace(0, len(line), len(line))

    plt.title(transform(p, freq, count, out="latex"))
    plt.xlabel("Scan range [MHz]")
    plt.ylabel("Accumulated counts [cps]")

    y_fit = lorentz(x, *p)
    error = line - y_fit
    plt.plot(freq, line, "-")
    plt.plot(freq, y_fit, "-r")
    plt.plot(freq, error, "-", color="black", alpha=0.2)
    print("\n[Single Lorentz] Error: ", sum(error ** 2) / 1e9)
    print(transform(p, freq, count=1, out="txt"))


def center(freq, array, collapse=True):
    """
    Takes the frequency range of the xtract and the 2D scan image (array)
    and returns the shifted scan (shifted_scan -- the fourth element of the returned array).
    """
    scan_range = len(freq)
    accu = np.zeros(scan_range)
    counter = 0
    scan_line = []

    for idx, scan in enumerate(array):
        try:
            param = opt(freq, scan)
        except RuntimeError as err:
            if DEBUG:
                print("Failed to fit on: {}\t{}".format(idx, err))
            continue

        # if criteria aren't met, we discard this scan
        #   1) peak is positive, bigger than offset
        #   2) width is smaller than whole range but not zero
        #   3) mid point is inside range
        criteria = (
            (param[0] > abs(param[3]))
            and (0 < abs(param[1]) < scan_range)
            and (0 < param[2] < scan_range)
        )
        if criteria:
            # shift scan to middle and subtract offset
            shifted = np.roll(scan, int(scan_range / 2 - param[2])) - param[3]
            if collapse:
                accu += shifted
            else:
                accu = np.vstack((accu, shifted))
                scan_line.append((idx, param))
            counter += 1
        elif DEBUG:
            print("Omitted:{}\t{}".format(idx, transform(param, out="txt")))
    print("\nIntegrated <{}> of all the {} scans.".format(counter, len(array)))
    shifted_scan = np.vstack(accu)
    return accu, counter, scan_line, shifted_scan


def transform(p, freq=[0, 1], count=1, out=None):
    dfreq = max(freq) - min(freq)
    stretch = dfreq / (len(freq) - 1)

    # map linspace to frequency and average intensities
    q = p[0] / count, stretch * p[1], stretch * p[2] + min(freq), p[3] / count

    if out == "txt":
        return "I={:.2f}   Gamma={:.2f}   Zero={:.2f}   Offset={:.2f}".format(*q)
    elif out == "latex":
        return "$I_0=${:.2f}     $\gamma=${:.2f}    $x_0=${:.2f}\
               $\Delta y=${:.2f}    $\eta=${}".format(
            *q, count
        )
    else:
        return q


def main(ARGS=None):
    parser = argparse.ArgumentParser(prog="Laserscanner")
    parser.add_argument("output", choices=["raw", "stack", "fit"])
    parser.add_argument("--single", "-s", type=int)
    parser.add_argument("files", nargs=argparse.REMAINDER)
    if ARGS is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(ARGS)

    for fname in args.files:
        header, raw, freq = xtract(fname)

        if args.output == "raw":
            plt.title(f"Source:  {fname}")
            plt.contourf(raw)

        elif args.output == "fit":
            if args.single:
                scan, count = raw[args.single], 1
            else:
                scan, count, _ = center(freq, raw, collapse=True)

            opti_plot(freq, scan, count)
            # dual_lorentz.run_fit(freq, scan)

        elif args.output == "stack":
            scan, count, _ = center(freq, raw, collapse=False)
            plt.title(f"{count} of total {len(raw)} scans")
            try:
                plt.contourf(scan)
            except TypeError:
                logger.warn(f"No suitable scans found in {fname}")

        logger.debug("\nScanning parameters for {}:\n{}".format(fname, header))


warnings.filterwarnings("ignore")  # do not print warnings
DEBUG = 0

if __name__ == "__main__":
    main()
    plt.show()
