import sys
import time
import serial
import json

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <serial_port> <json_file>")
    sys.exit(1)

ser = serial.Serial(sys.argv[1], 115200)
json_data = json.load(open(sys.argv[2]))
delay = json_data['delta']

while True:
    for value in json_data['data']:
        freq_a, freq_b = int(value[0]), int(value[1])
        print(f"Setting frequency to {freq_a} Hz & {freq_b} Hz")
        ser.write(f'set dtmf {freq_a} {freq_b}\n'.encode())
        time.sleep(delay)