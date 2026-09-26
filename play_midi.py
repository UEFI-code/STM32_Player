import mido
import time
import serial

PORT = "/dev/tty.usbserial-1120"
BAUDRATE = 115200
ser = None

def init_serial():
    global ser
    ser = serial.Serial(PORT, BAUDRATE, timeout=2)
    print(f"Listen {PORT}, Baudrate: {BAUDRATE}...")
    ser.write(b"\n");time.sleep(0.01)

# Read MIDI file
def play_midi_beep(file_path):
    mid = mido.MidiFile(file_path)
    tempo = 50000  # Default tempo (microseconds per beat)
    for msg in mid.play():
        if msg.type == 'note_on' and msg.velocity > 0:  # Play note
            freq = int(440 * (2 ** ((msg.note - 69) / 12)))
            ser.write(f"set freq {freq}\n".encode('utf-8'))
            print(f"Set freq: {freq} for note {msg.note} ({freq:.2f} Hz)")
            time.sleep(tempo / 1_000_000)
        elif msg.type == 'set_tempo':  # Update tempo
            tempo = msg.tempo

init_serial()
while True:
    try:
        #play_midi_beep('laputa.mid')
        play_midi_beep('ddlc_main.mid')
        #play_midi_beep('yesterday_once_more.mid')
    except serial.SerialException:
        print('ch340 die, reconnecting...')
        time.sleep(1)
        try: init_serial()
        except: pass