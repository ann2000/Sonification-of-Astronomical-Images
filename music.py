import numpy as np
from scipy.io import wavfile
import utils, sonification1
import sounddevice as sd
import soundfile as sf

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilenames()
for path in file_path:
    song_freqs, song_amplitudes = sonification1.get_freqandamp(path)
    note_duration = [0.25]*len(song_freqs)

#factor = [0.59, 0.10, 0.13, 0.        , 0.00, 0.02, 0.13] #violin
#factor = [0.89640525, 0.08522547, 0.        , 0.        , 0.01836929] #bass
    factor = [0.73, 0.16, 0.06, 0.0, 0.01 , 0.0, 0.01] #piano
#length = [0.01, 0.6, 0.29, 0.1]
#decay = [0.05,0.02,0.005,0.1]
    sustain_level = 0.1

    right_hand = utils.get_song_data(song_freqs, note_duration, factor, song_amplitudes)
# bar value needed for pedal
    data = right_hand
print(data)
#data = data * (4096/np.max(data))

#sonification1.out_video.release()

wavfile.write('data/sonified_audio.wav', 44100, data.astype(np.int16))
sound, fs = sf.read('data/sonified_audio.wav', dtype='float32')  
#sd.play(sound, fs)
status = sd.wait()


