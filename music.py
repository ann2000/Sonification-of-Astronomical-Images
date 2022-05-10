import cv2
import numpy as np
from scipy.io import wavfile
import utils, sonification1, merge
import sounddevice as sd
import soundfile as sf
from moviepy.editor import *

import tkinter as tk
from tkinter import filedialog

import os

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilenames()
source_coordinate_list = []

for i in range (len(file_path)):

    file_name = os.path.basename(file_path[i])
    source_positions = dict()
    song_freqs, song_amplitudes, source_positions = sonification1.get_freqandamp(file_path[i])
    source_coordinate_list.append(source_positions)

    note_duration = [0.25]*len(song_freqs)

    if (file_name.startswith('ir')):
        print(file_name)
        factor = [0.89640525, 0.08522547, 0.        , 0.        , 0.01836929] #bass
    elif (file_name.startswith('optical')):
        print(file_name)
        factor = [0.59, 0.10, 0.13, 0.        , 0.00, 0.02, 0.13] #violin
    elif (file_name.startswith('xray')):
        print(file_name)
        factor = [0.73, 0.16, 0.06, 0.0, 0.01 , 0.0, 0.01] #piano

#length = [0.01, 0.6, 0.29, 0.1]
#decay = [0.05,0.02,0.005,0.1]

    sustain_level = 0.1

    if i==0:
        data = utils.get_song_data(song_freqs, note_duration, factor, song_amplitudes)
    else:
        data += utils.get_song_data(song_freqs, note_duration, factor, song_amplitudes)
# bar value needed for pedal
source_coordinates = dict()

for dict in source_coordinate_list:
    for list in dict:
        if list in source_coordinates:
            source_coordinates[list] += (dict[list])
        else:
            source_coordinates[list] = dict[list]

merge.merge_images(file_path)
image = cv2.imread('numpy_image_alpha_blend.jpg')
clip = utils.get_video(image, source_coordinates)

print(data)
#data = data * (4096/np.max(data))

#sonification1.out_video.release()

wavfile.write('data/sonified_audio.wav', 44100, data.astype(np.int16))

'''
sound, fs = sf.read('data/sonified_audio.wav', dtype='float32')  
#sd.play(sound, fs)
status = sd.wait()
clip = sonification1.clip

# loading audio file
audioclip = AudioFileClip("data/sonified_audio.wav")
  
# adding audio to the video clip
videoclip = clip.set_audio(audioclip)
videoclip.write_videofile("video2.avi", codec="libx264")
'''