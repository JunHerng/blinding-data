#!/usr/bin/env python3

from ast import arg
from subprocess import Popen, PIPE
import numpy as np

def read_file(file):
    """Reads timestamp file and returns contents as list.
    """
    ls = []
    with open(file) as f:
        a = f.read()
        ls = a.rstrip().split("\n")
    return(ls)

def find_bit_5(num):
    """Checks if bit 5 is on, indicating self-seeding.
    """
    a = num & 0b100000
    return(a==0b100000)

def call_readevents(args, logfile):
    """Calls readevents7 with given options.

    args e.g.:
        args = [
            '-a',1,
            '-X',
            ]
    """
    abs_dir = '/home/s-fifteen/programs/usbtmst4/apps/'
    prog = abs_dir + 'readevents7'
    logfile = abs_dir + 'tstamps/' + logfile

    args.extend(['>', '/home/s-fifteen/programs/usbtmst4/apps/tstamps/file2'])
    with open(logfile,'w') as f:
        process = Popen([prog, *list(map(str, args))] , stdout=f, stderr=PIPE)
    stdout, stderr = process.communicate()

def generate_args(bmode: list, num_stamps: int, out_mode: int):
    """Generates options to be called with readevents7.
    """
    arg_list = ['-b', 0, '-q', 0, '-a',0]
    bm_str = (',').join(list(map(str,bmode)))
    arg_list[1] = bm_str
    arg_list[3] = num_stamps
    arg_list[5] = out_mode

    return arg_list

def generate_logfile(bmode: list, num_stamps: int, out_mode: int):
    """Generates logfile name string with given options.

    eg. ['-b', '225,0,30000', '-q', '500000', '-a', '2']

    filename: read7log_b225_0_30000_q500000_a2
    """
    ls = ['read7log', 'b'+str(bmode[0]), str(bmode[1]), str(bmode[2]),\
         'q'+str(num_stamps), 'b'+str(out_mode)]
    return '_'.join(ls)

def main():
    """Call readevents7 with a range of options and outputs timestamps
    to file.
    """
    # Generate b options, each row is a set of options
    b = np.arange(0, 60000, 10000)
    a = np.full((1,len(b)), 225)[0]
    c = np.full((1,len(b)), 0)[0]
    b_opt = np.column_stack((a,b,c))

    # Other options
    num_stamps = 500000
    outmode = 2

    for row in b_opt:
        args = generate_args(row, num_stamps, outmode)
        logfile = generate_logfile(row, num_stamps, outmode)
        call_readevents(args, logfile)

if __name__ == "__main__":
    main() 