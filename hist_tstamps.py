    """Histogram plots. Shoves timestamps into larger time bins for visualisation.
    Currently not so useful.
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

def hist(data: np.ndarray):
    """Returns arrays of filtered timestamps.
    """

    # 54 MSB timing, 4 LSB detector channel
    # Perform bit shifting for binning
    # >>10 : Full timing info, in units of 1/256 ns
    # >>11 : Truncate last bit, becomes units of 1/128 ns
    # >>18 : 1ns
    # >>28 : ~ 1us
    # >>38 : ~ 1ms
    # >>42 : ~ 16ms, which will get me about 50 histogram bins in a 1 second window
    timings = data >> np.int64(15)
    unique, counts = np.unique(timings, return_counts=True) # np.unique returns tuple here

    return unique, counts


c1,c2,c3,c4 = open_split_channel(files[0])
u1,cs1 = hist(c1)
u2,cs2 = hist(c2)
u3,cs3 = hist(c3)
u4,cs4 = hist(c4)

# unique, counts = hist(files[0])

fig, axs = plt.subplots(2,2)

axs[0,0].plot(*hist(c1))
axs[0,0].set_title('a=10000, c1')

axs[0,1].plot(*hist(c2))
axs[0,1].set_title('c2')

axs[1,0].plot(*hist(c3))
axs[1,0].set_title('c3')

axs[1,1].plot(*hist(c4))
axs[1,1].set_title('c4')

#plt.plot(unique, counts)
plt.tight_layout()
plt.show()