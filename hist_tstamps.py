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

def hist(file: str):
    """Returns arrays of filtered timestamps.
    """
    # Read characters
    with open(file) as f:
        data = np.array([row.rstrip("\n") for row in f.readlines()])[::50] # Subsample data

    # Convert to raw bit string
    hex2num = lambda v: int(v, base=16)
    dwords = np.array(list(map(hex2num, data)), dtype = np.int64)

    # 54 MSB timing, 4 LSB detector channel
    # Perform bit shifting for binning
    # >>10 : Full timing info, in units of 1/256 ns
    # >>11 : Truncate last bit, becomes units of 1/128 ns
    # >>18 : 1ns
    # >>28 : ~ 1us
    # >>38 : ~ 1ms
    # >>42 : ~ 16ms, which will get me about 50 histogram bins in a 1 second window
    timings = dwords >> np.int64(42)
    unique, counts = np.unique(timings, return_counts=True) # np.unique returns tuple here

    return unique, counts

unique, counts = hist(files[0])

fig, axs = plt.subplots(2,2)

axs[0,0].plot(*hist(files2[0]))
axs[0,0].set_title('a=10000')

axs[0,1].plot(*hist(files2[1]))
axs[0,1].set_title('a=20000')

axs[1,0].plot(*hist(files2[2]))
axs[1,0].set_title('a=30000')

axs[1,1].plot(*hist(files2[3]))
axs[1,1].set_title('a=40000')

#plt.plot(unique, counts)
plt.show()