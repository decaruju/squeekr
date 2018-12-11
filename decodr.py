import pyaudio
import numpy as np

import bitarray


CHUNK = 96 # number of data points to read at a time
RATE = 96000 # time resolution of the recording device (Hz)

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK) #uses default input device

while True:
    last = 0
    num = 0
    bits = ''
    skips = 0
    read = False

    # create a numpy array holding a single read of audio data
    while True:
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        fft = np.fft.fft(data)
        abs_fft = np.abs(fft)
        current = str(int(abs_fft[15] < abs_fft[16]))
        if current == last:
            num += 1
        else:
            last = current
            num = 0
            skips += 1
        if num == 48:
            bits = bits + str(last)
            num = 0
            read = True
            skips = 0
        if skips == 99 and read:
            break

    ba = bitarray.bitarray(bits).tobytes().decode('utf8')
    print(ba)

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()
