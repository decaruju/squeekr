import sys

from pysine import sine
import bitarray


if len(sys.argv) != 2:
    print('Wrong number of arguments')
    print('Expected 1 argument')

ba = bitarray.bitarray()
ba.frombytes(sys.argv[1].encode('utf8'))
for bit in ba:
    sine(frequency=15000 + int(bit)*1000, duration=0.05)
