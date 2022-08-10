from subprocess import Popen, PIPE

_hexfile = "tmp2"

def read_file(file):
    ls = []
    with open(file) as f:
        a = f.read()
        ls = a.rstrip().split(sep="\n")
    return(ls)

def find_bit_5(num: int):
    a = num & 0b100000
    return(a==0b100000)

if __name__ == "__main__":
    foo = read_file(_hexfile)
    print(foo)
    print(f'Length: {len(foo)}')
    ful = [int(ts_hex, 16) for ts_hex in foo]
    mask = [find_bit_5(ts_dec) for ts_dec in ful]
    print(ful)
    print(mask)
    # True == 1, False == 0
    print(sum(mask))
    print(len(ful))
    print(len(foo))

