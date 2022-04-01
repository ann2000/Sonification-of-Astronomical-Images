import numpy as np
from scipy.io import wavfile
import utils, sonification



right_hand_notes = ['C4', 'C4', 'G4', 'G4',
                   'A4', 'A4', 'G4',
                   'F4', 'F4', 'E4', 'E4',
                   'D4', 'D4', 'C4',
                   'G4', 'G4', 'F4', 'F4',
                   'E4', 'E4', 'D4',
                   'G4', 'G4', 'F4', 'F4',
                   'E4', 'E4', 'D4',
                   'C4', 'C4', 'G4', 'G4',
                   'A4', 'A4', 'G4',
                   'F4', 'F4', 'E4', 'E4',
                   'D4', 'D4', 'C4',]
right_hand_duration = [1]*len(sonification.source_freqs)

#factor = [0.59, 0.10, 0.13, 0.        , 0.00, 0.02, 0.13] #violin
#factor = [0.89640525, 0.08522547, 0.        , 0.        , 0.01836929] #bass
factor = [0.73, 0.16, 0.06, 0.0, 0.01 , 0.0, 0.01] #piano
#length = [0.01, 0.6, 0.29, 0.1]
#decay = [0.05,0.02,0.005,0.1]
sustain_level = 0.1
right_hand = utils.get_song_data(sonification.source_freqs, right_hand_duration, factor, sonification.source_amplitudes)
# bar value needed for pedal
data = right_hand
#data = data * (4096/np.max(data))
wavfile.write('data/sonified_audio.wav', 44100, data.astype(np.int16))