
# Justin, 2022-07-31
# Read S15 timestamp outmode -a0 data
#
# See:
# - readevents outmode code: https://github.com/s-fifteen-instruments/qcrypto/blob/43edb80d5f331fac3e2fe931628920e1b539d951/timestamp7/readevents5.c#L255
# - timing specification: https://github.com/s-fifteen-instruments/qcrypto/blob/Documentation/docs/source/file%20specification.rst
#
# Raw event in outmode -a1 has the following code:
#     rawevent = rbbuffer[i] | (((uint64_t)rbbuffer[i+1])<<32);
# i.e. low word is followed by high word and concatenated
#
# Raw event in outmode -a0 writes directly from buffer:
#     fprintf(outfile, "%08x\n",rbbuffer[i]);
# i.e. second word is high word

    """Generic timestamp processing and plotting functions.
    See other files for more specific plots.
    """

import numpy as np
import matplotlib.pyplot as plt

TIMESTAMP_DATA = "read7log_b225_50000_0_q500000_b2"

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

def foo(file: str):
    # Read characters
    with open(file) as f:
        data = np.array([row.rstrip("\n") for row in f.readlines()])#[::50] # Subsample data

    # Convert to raw bit string
    hex2num = lambda v: int(v, base=16)
    # words_low = np.array(list(map(hex2num, data[0::2])), dtype=np.int64) # 1 word = 2 bytes = 16 bits
    # words_high = np.array(list(map(hex2num, data[1::2])), dtype=np.int64)  # second word is high word
    # dwords = (words_high << np.int64(64)) + words_low
    dwords = np.array(list(map(hex2num, data)), dtype = np.int64)

    # 54 MSB timing, 4 LSB detector channel
    timings = dwords >> np.int64(10)
    channels = dwords & 0b1111

    return timings[(channels & 0b0001).astype(bool)], timings[(channels & 0b0010).astype(bool)], (dwords & 0b100000).astype(bool), len(data)

def blinded_frac(file: str):
    """Returns the fraction of blinded timestamps.

    Args:
        file (str): filename

    Returns:
        float: fraction of blinded bits
    """
    blinded = sum(foo(file)[-2])
    total = foo(file)[-1]
    print(blinded)
    print(total)
    print(blinded/total)
    
    return blinded/total

print(blinded_frac(files2[0]))
print(blinded_frac(files2[1]))
print(blinded_frac(files2[2]))
print(blinded_frac(files2[3]))
print(blinded_frac(files2[4]))

# plt.plot(foo(TIMESTAMP_DATA)[0], ".", markersize=1, label="Channel 1")
# plt.plot(foo(TIMESTAMP_DATA)[1], ".", markersize=1, label="Channel 2")
# plt.plot(foo(files[0])[0], ".", markersize=1, label="a = 10000")
# plt.plot(foo(files[1])[0], ".", markersize=1, label="a = 20000")
# plt.plot(foo(files[2])[0], ".", markersize=1, label="a = 30000")
# plt.plot(foo(files[3])[0], ".", markersize=1, label="a = 40000")
# plt.plot(foo(files[4])[0], ".", markersize=1, label="a = 50000")
# plt.plot(foo(TIMESTAMP_DATA)[-1], ".", markersize=1, label="blind mode")

# plt.show()

'''

fig, axs = plt.subplots(2,5)
# region levela
axs[0,0].plot(foo(files[0])[0])
axs[0,0].set_title('a = 10000')

axs[0,1].plot(foo(files[1])[0])
axs[0,1].set_title('a = 20000')

axs[0,2].plot(foo(files[2])[0])
axs[0,2].set_title('a = 30000')

axs[0,3].plot(foo(files[3])[0])
axs[0,3].set_title('a = 40000')

axs[0,4].plot(foo(files[4])[0])
axs[0,4].set_title('a = 50000')
#endregion

#region levelb
# axs[0,0].plot(foo(files2[0])[0])
# axs[0,0].set_title('a = 10000')

# axs[0,1].plot(foo(files2[1])[0])
# axs[0,1].set_title('a = 20000')

# axs[0,2].plot(foo(files2[2])[0])
# axs[0,2].set_title('a = 30000')

# axs[0,3].plot(foo(files2[3])[0])
# axs[0,3].set_title('a = 40000')

# axs[0,4].plot(foo(files2[4])[0])
# axs[0,4].set_title('a = 50000')
#endregion

axs[1,0].plot(foo(files[0])[-1], ".", markersize=1)
axs[1,0].set_title('a = 10000')

axs[1,1].plot(foo(files[1])[-1], ".", markersize=1)
axs[1,1].set_title('a = 20000')

axs[1,2].plot(foo(files[2])[-1], ".", markersize=1)
axs[1,2].set_title('a = 30000')

axs[1,3].plot(foo(files[3])[-1], ".", markersize=1)
axs[1,3].set_title('a = 40000')

axs[1,4].plot(foo(files[4])[-1], ".", markersize=1)
axs[1,4].set_title('a = 50000')
'''

# plt.tight_layout() # Prevent overlapping titles
# plt.legend(loc='upper left')
# plt.show()