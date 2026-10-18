import sys
import serial
import json
import time

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <serial_port> <json_file>")
    sys.exit(1)

ser = serial.Serial(sys.argv[1], 115200)
json_data = json.load(open(sys.argv[2]))
prog_delay = 0.05

def enable_spi_write():
    ser.write(b"CS 0\n");ser.flush();time.sleep(prog_delay)
    ser.write(b"SPI send 06\n");ser.flush();time.sleep(prog_delay) # enable write
    ser.write(b"CS 1\n");ser.flush();time.sleep(prog_delay)
    ser.write(b"CS 0\n");ser.flush();time.sleep(prog_delay)
    ser.write(b"SPI send 05\n");ser.flush();time.sleep(prog_delay) # query status
    ser.reset_input_buffer() # clear serial read buffer
    ser.write(b"SPI recv\n");ser.flush();time.sleep(prog_delay)
    result = ser.readline()
    ser.write(b"CS 1\n");ser.flush();time.sleep(prog_delay)
    if result != b'SPI received: 02\n':
        print(f"Error: SPI flash write enable failed, error: {result}")
        sys.exit(1)
    print("SPI flash write enabled")

def wait_for_spi_ready():
    result = b''
    while result != b'SPI received: 00\n':
        print(f"Waiting for SPI flash operation to complete, status: {result}")
        time.sleep(1)
        ser.write(b"CS 0\n");ser.flush();time.sleep(prog_delay)
        ser.write(b"SPI send 05\n");ser.flush();time.sleep(prog_delay) # query status
        ser.reset_input_buffer() # clear serial read buffer
        ser.write(b"SPI recv\n");ser.flush();time.sleep(prog_delay)
        result = ser.readline()
        ser.write(b"CS 1\n");ser.flush();time.sleep(prog_delay)

# step 0. check dtmf size
tone_size = len(json_data['data']) * 4 # two uint16_t per tone
print(f"Tone size: {tone_size} bytes")
tone_pages = tone_size // 256 + 1
print(f"Tone pages: {tone_pages}")

# step 1. chk SPI flash info
ser.write(b"\n");ser.flush();time.sleep(prog_delay)
ser.write(b"CS 1\n");ser.flush();time.sleep(prog_delay)
ser.write(b"CS 0\n");ser.flush();time.sleep(prog_delay)
ser.write(b"SPI send 9F\n");ser.flush();time.sleep(prog_delay)
ser.reset_input_buffer() # clear serial read buffer
ser.write(b"SPI recv\n");ser.flush();time.sleep(prog_delay)
result = ser.readline()
ser.write(b"CS 1\n");ser.flush();time.sleep(prog_delay)
if result != b'SPI received: EF\n':
    print(f"Error: SPI flash not detected, error: {result}")
    sys.exit(1)
print("SPI flash detected")

# step 2. erase flash
enable_spi_write()
ser.write(b"CS 0\n");ser.flush();time.sleep(prog_delay)
ser.write(b"SPI send C7\n");ser.flush();time.sleep(prog_delay)
ser.write(b"CS 1\n");ser.flush();time.sleep(prog_delay)
wait_for_spi_ready()
print("SPI flash erased")

# step 3. write flash
for page in range(tone_pages):
    page_addr_hex = f"{(page * 256):06X}"
    print(f"Writing page {page}/{tone_pages}, address: {page_addr_hex}")
    enable_spi_write() # we need to enable write for each page write
    ser.write(b"CS 0\n");ser.flush();time.sleep(prog_delay)
    ser.write(b"SPI send 02\n");ser.flush();time.sleep(prog_delay) # write command
    ser.write(f"SPI send {page_addr_hex[0:2]}\n".encode());ser.flush();time.sleep(prog_delay) # address byte 1
    ser.write(f"SPI send {page_addr_hex[2:4]}\n".encode());ser.flush();time.sleep(prog_delay) # address byte 2
    ser.write(f"SPI send {page_addr_hex[4:6]}\n".encode());ser.flush();time.sleep(prog_delay) # address byte 3
    tone_chuck = json_data['data'][page*64:(page+1)*64] # 64 tones per page
    for tone in tone_chuck:
        freq_a, freq_b = int(tone[0]), int(tone[1])
        print(f"Store frequency to {freq_a} Hz & {freq_b} Hz")
        ser.write(f'store dtmf {freq_a} {freq_b}\n'.encode());ser.flush();time.sleep(prog_delay)
        ser.reset_input_buffer() # clear serial read buffer
    ser.write(b"CS 1\n");ser.flush();time.sleep(prog_delay)
    wait_for_spi_ready()
print("SPI flash write complete")