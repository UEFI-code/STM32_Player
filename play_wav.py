import serial
import numpy as np
import time
import sys

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <serial_port> <wav_file>")
    sys.exit(1)

ser = serial.Serial(sys.argv[1], 115200)

# load test.wav file
import numpy as np
from scipy.io import wavfile
sr, data = wavfile.read(sys.argv[2])
if data.dtype == np.int16:
    print("16-bit PCM WAV file detected.")
    data = data / 32768.0
elif data.dtype == np.int32:
    print("32-bit PCM WAV file detected.")
    data = data / 2147483648.0
if data.ndim > 1:
    data = data[:, 0]

chunk_pos = 0
while True:
    chunk_data = data[chunk_pos:chunk_pos + 1024] * 0.5 + 0.5
    chunk_data = (chunk_data * 65535).astype(np.uint16)
    ser.write(chunk_data.tobytes())
    ser.flush()
    chunk_pos += 1024
    if chunk_pos >= len(data):
        chunk_pos = 0
    time.sleep(1024 / sr)  # wait for the next chunk