"""
g2 calculations for timestamps using np.diff. Currently used to check for 1us hold-off time of detector.
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

def open_subsample(file, n):
    with open(file) as f:
        data_str = np.array([row.rstrip("\n") for row in f.readlines()])[::n] # Subsample data
    hex2num = lambda v: int(v, base=16)
    data = np.array(list(map(hex2num, data_str)), dtype = np.int64)

    return data

def open_split_channel(file):
    with open(file) as f:
        data_str = np.array([row.rstrip("\n") for row in f.readlines()])
    hex2num = lambda v: int(v, base=16)
    data = np.array(list(map(hex2num, data_str)), dtype = np.int64)
    ch1_data = data[[(row & 0b0001).astype(bool) for row in data]]
    ch2_data = data[[(row & 0b0010).astype(bool) for row in data]]
    ch3_data = data[[(row & 0b0100).astype(bool) for row in data]]
    ch4_data = data[[(row & 0b1000).astype(bool) for row in data]]

    return ch1_data, ch2_data, ch3_data, ch4_data

def calc_g2(dec_ts: np.ndarray, bit5 = False):
    """
    bit5: If True, returns index of all self-test timestamps.
    """

    # Obtain indexes where bit5 is 1
    bit5_idx = ((dec_ts & 0b100000)==0b100000).nonzero()[0]
    bit5_idx = bit5_idx[:-1] # throw away last idx to prvent idx error when using np.diff later

    # Truncate irrelevant bit data, keep only timing related stuff
    #dec_ts = (dec_ts >> 10)/256 # in units of ns
    dec_ts = (dec_ts >> 15) # in units of 1/8 ns, to account for jitter

    # Get time difference
    diff_ts = np.diff(dec_ts)
    if bit5: # return timestamp idx with bit 5 on
        diff_ts = diff_ts[bit5_idx]

    unique, counts = np.unique(diff_ts, return_counts=True)

    return unique, counts

c1,c2,c3,c4 = open_split_channel(files[-1])
diff1, counts1 = calc_g2(c1)
diff2, counts2 = calc_g2(c2)
diff3, counts3 = calc_g2(c3)
diff4, counts4 = calc_g2(c4)

# data2 = open_split_channel(files2[-1])
# diff2, counts2 = calc_g2(data2)

bit5_data1, bit5_data2, bit5_data3, bit5_data4 = open_split_channel(files[-1])
diff5, counts5 = calc_g2(bit5_data1, bit5=True)
modal_counts = np.unique(counts5)
print(modal_counts)

plt.plot(diff5/8, counts5, label='g2')
plt.xlabel('ns') 
plt.title('levelb = 10000')
plt.show()
