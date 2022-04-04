import numpy as np

def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
  
    t = np.linspace(0, duration, int(sample_rate*duration))
    wave = amplitude*np.sin(2*np.pi*frequency*t)
    return wave

def apply_overtones(frequency, duration, factor, amplitude, sample_rate=44100):

    
    frequencies = np.minimum(np.array([frequency*(x+1) for x in range(len(factor))]), sample_rate//2)
    amplitudes = np.array([amplitude*x for x in factor])
    
    fundamental = get_sine_wave(frequencies[0], duration, sample_rate, amplitudes[0])
    for i in range(1, len(factor)):
        overtone = get_sine_wave(frequencies[i], duration, sample_rate, amplitudes[i])
        fundamental += overtone
    return fundamental


def get_song_data(freqs, note_values, factor, amplitudes, sample_rate=44100):
    
    frequencies = freqs
#    new_values = apply_pedal(note_values, bar_value)
    duration = int(sum(note_values)*sample_rate)
    end_idx = np.cumsum(np.array(note_values)*sample_rate).astype(int)
    start_idx = np.concatenate(([0], end_idx[:-1]))
    end_idx = np.array([start_idx[i]+note_values[i]*sample_rate for i in range(len(note_values))]).astype(int)
    
    song = np.zeros((duration,))
    for i in range(len(frequencies)):
        this_note = apply_overtones(frequencies[i], note_values[i], factor, amplitudes[i])
#        weights = get_adsr_weights(frequencies[i], note_values[i], length, decay, sustain_level)
        song[start_idx[i]:end_idx[i]] += this_note

#        song = song*(amplitudes[i]/np.max(song))

    return song