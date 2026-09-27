import serial
import threading
import numpy as np
import time
import sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <serial_port>")
    sys.exit(1)

ser = serial.Serial(sys.argv[1], 115200)
data_chunk = b''

def worker():
    global data_chunk
    while True:
        # encode the target value as a 16-bit integer, little-endian
        if len(data_chunk) > 1024:
            ser.write(data_chunk)
            ser.flush()
            data_chunk = b''
        

thread = threading.Thread(target=worker)
thread.start()

# generate a 440Hz sine wave for 1 second
fs = 44100  # sample rate
f = 1000.0  # frequency
samples = (np.sin(2 * np.pi * np.arange(fs) * f / fs)).astype(np.float32)

while True:
    for sample in samples:
        target_value = sample * 0.5 + 0.5  # scale to [0, 1]
        data_chunk += int(target_value * 65535).to_bytes(2, byteorder='little')
        time.sleep(1/fs)  # wait for the next sample