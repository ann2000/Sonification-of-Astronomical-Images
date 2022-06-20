import cv2
import numpy as np
from scipy.io import wavfile
import utils, sonification, merge
import sounddevice as sd
import soundfile as sf
from moviepy.editor import *

import tkinter as tk
from tkinter import filedialog

import os

def get_music():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilenames()
    source_coordinate_list = []

    for i in range (len(file_path)):

        file_name = os.path.basename(file_path[i])

        if (file_name.startswith('ir')):
            print(file_name)
            factor = [0.89, 0.08, 0.        , 0.        , 0.018] #bass
            fl, fh = 33, 523
        elif (file_name.startswith('optical')):
            print(file_name)
            #factor = [0.59, 0.10, 0.13, 0.        , 0.00, 0.02, 0.13] #violin
            #factor = [0.62, 0.098, 0.13, 0.        , 0.011, 0.007, 0.11, 0.012]
            factor = [1.0, 0.286699025, 0.150079537, 0.042909002, 0.203797365, 0.229228698, 0.156931925, 0.115470898, 0.0, 0.097401803, 0.087653465, 0.052331036, 0.052922462, 0.038850593, 0.053554676, 0.053697434, 0.022270261, 0.013072562, 0.008585879, 0.005771505,0.004343925, 0.002141371, 0.005343231, 0.000530244, 0.004711017, 0.009014153]
            fl, fh = 196, 600
        elif (file_name.startswith('xray')):
            print(file_name)
            factor = [0.73, 0.16, 0.06, 0.0, 0.01 , 0.0, 0.01] #piano
            fl, fh = 28, 4186 

        source_positions = {}
        song_freqs, song_amplitudes, source_positions = sonification.get_freqandamp(file_path[i], fl, fh)
        source_coordinate_list.append(source_positions)

        note_duration = [0.25]*len(song_freqs)
    #length = [0.01, 0.6, 0.29, 0.1]
    #decay = [0.05,0.02,0.005,0.1]

        sustain_level = 0.1

        if i==0:
            data = utils.get_song_data(song_freqs, note_duration, factor, song_amplitudes)
        else:
            data += utils.get_song_data(song_freqs, note_duration, factor, song_amplitudes)
    # bar value needed for pedal

    source_coordinates = {}

    for dict in source_coordinate_list:
        for list in dict:
            if list in source_coordinates:
                source_coordinates[list] += (dict[list])
            else:
                source_coordinates[list] = dict[list]

    merge.merge_images(file_path)
    image = cv2.imread('blended_image.jpg')
    clip = utils.get_video(image, source_coordinates)

    print(data)
    #data = data * (4096/np.max(data))

    #sonification1.out_video.release()

    wavfile.write('data/sonified_audio.wav', 44100, data.astype(np.int16))

    sound, fs = sf.read('data/sonified_audio.wav', dtype='float32')  
    #sd.play(sound, fs)
    status = sd.wait()

    # loading audio file
    audioclip = AudioFileClip("data/sonified_audio.wav")
    
    # adding audio to the video clip
    videoclip = clip.set_audio(audioclip)
    videoclip.write_videofile("video2.avi", codec="libx264")