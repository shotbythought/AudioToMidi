from __future__ import division
import pyaudio
import wave
import numpy as np

import math

from aubio import pitch

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

win_s = 4096
hop_s = 1024

tolerance = 0.8

pitch_o = pitch("yin", win_s, hop_s, RATE)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

# total number of frames read
total_frames = 0
while True:
    data = stream.read(CHUNK, exception_on_overflow = False)

    recording = np.fromstring(data, dtype=np.float32)
    pitch = pitch_o(recording)[0]
    print("Frequency: ", pitch, pitch_o.get_confidence())

print("finished recording")
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()