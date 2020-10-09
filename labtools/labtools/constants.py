from os.path import join, expanduser
from numpy import dtype

CORR_TYPE = dtype(
    [
        ("time", dtype("<f4")),
        ("counts", dtype("<u4")),
        ("index", dtype("<u4")),
        ("counts2", dtype("<u4")),
    ]
)

DUMP_TYPE = dtype(
    [
        ("time_from_trigger", dtype("<u4")),
        ("channel", dtype("<i4")),
        ("time", dtype("<u8")),
    ]
)

CFG_NAME = ".labrc"
CFG_PATH = join(expanduser('~'), CFG_NAME)
