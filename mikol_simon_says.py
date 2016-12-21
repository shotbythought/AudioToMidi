#! /usr/bin/env python
import pyaudio
import wave
import numpy as np
from aubio import pitch
import math

CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

# Pitch
tolerance = 0.8
downsample = 1
win_s = 4096 // downsample # fft size
hop_s = 1024  // downsample # hop size
pitch_o = pitch("yinfft", win_s, hop_s, RATE)
pitch_o.set_tolerance(tolerance)

pitches = []
last_pitch = 0
num_hold = 0

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    buffer = stream.read(CHUNK)
    frames.append(buffer)

    signal = np.fromstring(buffer, dtype=np.float32)

    pitch = pitch_o(signal)[0]
    confidence = pitch_o.get_confidence()

    print("Pitch", pitch, confidence, num_hold)

    if pitch != 0 and confidence > 0:
        if abs(last_pitch - pitch) < 15:
            num_hold += 1

            if num_hold > 5 and (len(pitches) == 0 or abs(pitch-pitches[-1]) > 15):
                pitches.append(pitch)

        else:
            num_hold = 0
            last_pitch = pitch
    else: 
        num_hold = 0


print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

#sudo apt-get install python-pyaudio
PyAudio = pyaudio.PyAudio

#See http://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 16000 #number of frames per second/frameset.      

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = BITRATE, 
                output = True)

RATE = 16000


print(pitches)
for frequency in pitches:
    data = ''.join([chr(int(math.sin(x/((RATE/frequency)/math.pi))*127+128)) for x in xrange(RATE)])

    stream.write(data)

stream.stop_stream()
stream.close()
p.terminate()