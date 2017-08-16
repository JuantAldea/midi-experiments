import mido
import sys
import time
import signal, os

from pprint import pprint as pp

#mido.set_backend('mido.backends.rtmidi/LINUX_ALSA')
mido.set_backend('mido.backends.portmidi')

pp(mido.get_output_names())
pp(mido.get_output_names())
pp(mido.backend._get_devices())

inport = mido.open_input(filter(lambda x: 'USB' in x, mido.get_input_names())[0])
outport = mido.open_output(filter(lambda x: 'USB' in x, mido.get_input_names())[0])

mid = mido.MidiFile(sys.argv[1])

def release():
    global outport
    outport.reset()
    outport.close()

def sig_int(signum, frame):
    release()
    exit()

signal.signal(signal.SIGINT, sig_int)

def in_callback(message):
    pp(dir(message))

#inport.callback = in_callback 

'''
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)
'''

for msg in mid:
    time.sleep(msg.time)
    if not msg.is_meta:
        pp(msg)
        outport.send(msg)

