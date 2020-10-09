## Utilities for photonistas
# Tools that are used in more than one project or analysis

import sys
import yaml
from os import makedirs
from os.path import join
from getpass import getuser
from datetime import datetime
from numpy import array, memmap
import numpy as np

from .constants import CFG_PATH, DUMP_TYPE


def parse_config(config_path=CFG_PATH):
    """ Handles the translation of yaml file to correct paths etc. in `USER` dict.

    Paths are assumed relative to `root` if they are not absolute paths. The `daily`
    directory will be relative to `output`. Its creation can be controlled by the
    `create_daily` option.
    """
    config = check_config(config_path)
    root = config["path"]["root"]

    def rootify(section):
        for key, path in section.items():
            if not path.startswith("/"):
                section[key] = join(root, path)

    rootify(config['path'])

    if config["option"]["create_daily"]:
        daily_parent = config["path"].get("daily", config["path"]["output"])
        config["path"]["daily"] = create_daily(daily_parent)
    else:
        config["path"]["daily"] = config["path"]["output"]

    # make the `code` path available in python
    if not config["path"]["code"] in sys.path:
        sys.path.insert(0, config["path"]["code"])

    return config


def check_config(config_path):
    """ Checks whether config file exists, else create and try again.
    """
    while True:
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            print(f"Config file not found, generating a new one in {config_path}\n")
            gen_default_config(config_path)
            answer = input(
                "Config file created and can now be edited...\n"
                "Is the config set properly? [Y/n]"
            )
            if answer in "Yy":
                continue
            else:
                raise RuntimeError(
                    f"Check config file {config_path} and re-run the config parser."
                )


def gen_default_config(fname):
    """ Generates a default config file if not yet existent.
    """
    name = getuser()
    root = join("/home", name, "lab")
    default_cfg = {
        "name": name,
        "option": {"create_daily": True},
        "path": {"root": root, "code": "code", "data": "data", "output": "output",},
    }

    try:
        with open(fname, "x") as f:
            yaml.dump(default_cfg, f)
    except FileExistsError:
        print(
            f"Config file <{fname}> already exists.\nYou can edit it "
            f"directly or delete the file to create a new one."
        )


def create_daily(path):
    """ Manages creation of date-named directory if necessary.
    """
    TODAY = datetime.now().strftime("%d-%m-%Y")
    daily_path = join(path, TODAY)
    makedirs(daily_path, exist_ok=True)
    return daily_path


def get_dump(fname):
    """ Load a dump file without copying the whole content to disk.

    Read-only mode is to ensure data integrity.
    """
    data = memmap(fname, dtype=DUMP_TYPE, mode="r")
    return data


def get_laserscan(fname):
    """ Loads a frequency scan file from the Coherent 899.

    Returns a tuple: (header, frequency, scanlines)

    header: dict of metadata
    frequency: in MHz of scan range
    scanlines: 2D array of consecutive scans

    Very specific for this labview script etc... breaks if format changes.
    """
    with open(fname, "r") as scanfile:
        all_data = scanfile.read().splitlines()

    raw_data = all_data[5:]
    split_data = array([line.split("\t") for line in raw_data], dtype=float)
    data = split_data.transpose()
    frequency, lines = data[0], data[1::].astype(int)

    head = all_data[:4]
    timestamp = datetime.strptime(head[0], "%d/%m/%Y %I:%M:%S %p")
    header = dict(x.split("= ") for x in head[1:])
    header.update({"Timestamp": timestamp.ctime()})

    return header, frequency, lines

def get_trig_len(data, trig_ch = 5):
    """
    Return the length of the trigger.
    """
    tr = np.diff(data['time'][data['channel'] == trig_ch])
    return tr[tr//np.min(tr) == 1].mean()


def assign_trigs_to_clicks(data, channels=[1,2,3,4],trig=None,trig_ch=5, pix_trigs=None, return_trig=False):
    """Assigns trigger times to the corresponding clicks (replaces the field of overflow with time_from_trigger for each click).
    -- takes memmaped data returned by the get_dump(fname) function
    RETURNS: timetags data with times from trigger field:
    For example:

    time_from_trig	channel	      time
        3989	       4	 636522181766531
        77348	       2	 636522192370617
        29343	       4	 636522234085002

    Example for plotting the result:
    --Histogram:

    y, x = np.histogram(data['time_from_trig'][(data['channel']==1)], bins=1000, range=(0, trig))
    plt.plot(x[:-1], y)

    """
    assert np.isin(channels, np.unique(data['channel'])).all(), "Some of the channels aren't present in the tagstream file."

    assert ((len(list(data.dtype.fields))) != 3 & np.isin(['channel', 'time'], list(data.dtype.fields), invert=True).all()), "The dtype should be [('smth..', 'channel', 'time')']"
    if 'time_from_trig' not in list(data.dtype.fields):
        DUMP_TAGTYPE = np.dtype([('time_from_trig', np.dtype('<u4')),
                            ('channel', np.dtype('<i4')),
                            ('time', np.dtype('<u8'))])
        data=np.array(data, dtype=DUMP_TAGTYPE)
    if trig == None:
        trig=get_trig_len(data, trig_ch=trig_ch)
    i=1
    if pix_trigs != None:
        # skip pixel triggers
        data['time_from_trig'][np.isin(data['channel'],pix_trigs)] = 1
    while data[(data['time_from_trig'] == 0) & (data['channel'] != trig_ch)].shape[0] != 0:
        data_shifted = np.roll(data, -i)
        delta = (data_shifted['time'] - data['time'])[(data['time_from_trig'] == 0) & (data_shifted['channel'] == trig_ch) & (np.isin(data['channel'], channels))]
        data['time_from_trig'][(data['time_from_trig'] == 0) & (data_shifted['channel'] == trig_ch) & (np.isin(data['channel'], channels))] \
    = trig - np.mod(delta, trig)
        i+=1
        if i > 50:
            break
    if return_trig:
        return data
    else:
        return data[data['channel'] != trig_ch]

def shift_channels(data, shift, channels):
    '''
        Shift specified channels
    '''
    if not data.flags['WRITEABLE']:
        data=data.copy()
    data['time'][np.isin(data['channel'], channels)] = data['time'][np.isin(data['channel'], channels)] - shift
    data = data[np.argsort(data['time'])]
    return data

def correlation(data, corr_window=300_000, start_chs=[1], stop_chs=[4], trig_ch=5):
    """
    Build g^2 and k-photon probability function from Time Tagger data formated as :
    DUMP_TAGTYPE = np.dtype([('smth...', np.dtype('<u4')),
                                 ('channel', np.dtype('<i4')),
                                 ('time', np.dtype('<u8'))])

    returns autocorr_function and a list of k-photon probability data points

    Example for plotting the result:
    --Autocorrelation:

    autoc_diffs_tot, autoc_diffs = correlation(data)
    y, x = np.histogram(autoc_diffs_tot, bins=1000, range=(-10*trig, 10*trig))
    plt.plot(x[:-1], y)

    -- k-photon probability:

    corr_window=100_000_000
    autoc_diffs_tot, autoc_diffs = correlation(data, corr_window=corr_window)
    for k in autoc_diffs[::2]:
        y, x = np.histogram(k, bins=1000, range=(0, corr_window))
        plt.plot(x[:-1], y)

    """
    autoc_data = data[data['channel'] != 5]
    autoc_diffs = []
    shift=0
    while True:#shift != 20:
        shift += 1
        diffs = autoc_data['time'] - np.roll(autoc_data['time'], shift)
        dif_ch = np.roll(autoc_data['channel'], shift)
        diffs_1 = diffs[(diffs < corr_window) & np.isin(autoc_data['channel'], start_chs) & np.isin(dif_ch, stop_chs)]
        autoc_diffs.append(diffs_1.astype('int32'))
        diffs_2 = diffs[(diffs < corr_window) & np.isin(autoc_data['channel'], stop_chs) & np.isin(dif_ch, start_chs)]
        autoc_diffs.append(-diffs_2.astype('int32'))
        if (len(diffs_1) == 0) and (len(diffs_2) == 0):
            break
    autoc_diffs = np.array(autoc_diffs)
    autoc_diffs_tot = np.concatenate(autoc_diffs)
    return autoc_diffs_tot, autoc_diffs


def get_apds_shifts(data, trig):
    """
    THE FUNCTION IS TO BE DEVELOPED
    Takes data with already asigned triggers and spits out the shifts, which have to be applied to allign the APDs

    """	
    def x_max(y):
        return x[np.where(y == np.max(y))[0][0]]
    shifts = np.zeros(4)
    y, x = np.histogram(data['time_from_trig'][data['channel']==1], bins=1000, range=(0, trig))
    shifts[0] = x_max(y)
    for ch in [2,3,4]:
        y, x = np.histogram(data['time_from_trig'][data['channel']==ch], bins=1000, range=(0, trig))
        shifts[ch-1] = x_max(y) - shifts[0]
    shifts[0]=0
    return shifts


