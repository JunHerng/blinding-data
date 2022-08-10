"""
Various calculations involving timestamp data. For plotting,
see `plot_tstamps.py` or `hist_tstamps.py`
"""

import numpy as np
import matplotlib.pyplot as plt

files = ['read7log_b225_10000_0_q500000_b2',
         'read7log_b225_20000_0_q500000_b2',
         'read7log_b225_30000_0_q500000_b2',
         'read7log_b225_40000_0_q500000_b2',
         'read7log_b225_50000_0_q500000_b2',
        ]

files2 = ['read7log_b225_0_10000_q500000_b2',
         'read7log_b225_0_20000_q500000_b2',
         'read7log_b225_0_30000_q500000_b2',
         'read7log_b225_0_40000_q500000_b2',
         'read7log_b225_0_50000_q500000_b2',
        ]

def get_data(file: str, subsample = 1):
    """Returns arrays of filtered timestamps.

    Subsample: subsample every n-th data point. Used if data file is too large.
                Default 1.
    """
    # Read characters
    with open(file) as f:
        data = np.array([row.rstrip("\n") for row in f.readlines()])[::subsample] # Subsample data

    return data

def calc_g2(data, bit5 = False):
    """
    bit5: If True, returns index of all self-test timestamps.
    """
    # Convert data to decimal
    hex2num = lambda v: int(v, base=16)
    dec_ts = np.array(list(map(hex2num, data)), dtype = np.int64)
    # Obtain bit5 idx
    bit5_idx = ((dec_ts & 0b100000)==0b100000).nonzero()[0]
    bit5_idx = bit5_idx[:-1] # throw away last idx to prvent idx error when using np.diff later

    # Truncate irrelevant bit data
    dec_ts = (dec_ts >> 10)/256 # in units of ns

    # Get time difference
    diff_ts = np.diff(dec_ts)
    if bit5: # return timestamp idx with bit 5 on
        diff_ts = diff_ts[bit5_idx]

    unique, counts = np.unique(diff_ts, return_counts=True)

    return unique, counts

data = get_data(files[-1])
diff, counts = calc_g2(data)
data2 = get_data(files2[-1])
diff2, counts2 = calc_g2(data2)

bit5_data = get_data(files[-1])
diff5, counts5 = calc_g2(bit5_data, bit5=True)

plt.plot(diff5, counts5, label='g2')
plt.show()
