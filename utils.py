import numpy as np

def get_sine_wave(frequency, duration, amplitude, sample_rate=44100):
  
    t = np.linspace(0, duration, int(sample_rate*duration))
    wave = amplitude*np.sin(2*np.pi*frequency*t)
    return wave

def apply_overtones(frequency, duration, factor, amplitude, sample_rate=44100):

    
    frequencies = np.minimum(np.array([frequency*(x+1) for x in range(len(factor))]), sample_rate//2)
    amplitudes = np.array([amplitude*x for x in factor])
    
    fundamental = get_sine_wave(frequencies[0], duration, amplitudes[0], sample_rate)
    for i in range(1, len(factor)):
        overtone = get_sine_wave(frequencies[i], duration, amplitudes[i], sample_rate)
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
    
    for freq in range(len(frequencies)):
        this_note =  apply_overtones(frequencies[freq][0], note_values[freq], factor, amplitudes[freq][0])
        for i in range(len(frequencies[freq])):
            this_note += apply_overtones(frequencies[freq][i], note_values[freq], factor, amplitudes[freq][i])
#        weights = get_adsr_weights(frequencies[i], note_values[i], length, decay, sustain_level)
        song[start_idx[freq]:end_idx[freq]] += this_note
#        song = song*(amplitudes[i]/np.max(song))

    return song


def insidetriangle(x1,x2,x3,y1,y2,y3):

    xs=np.array((x1,x2,x3),dtype=float)
    ys=np.array((y1,y2,y3),dtype=float)

    # The possible range of coordinates that can be returned
    x_range=np.arange(np.min(xs),np.max(xs)+1)
    y_range=np.arange(np.min(ys),np.max(ys)+1)

    # Set the grid of coordinates on which the triangle lies. The centre of the
    # triangle serves as a criterion for what is inside or outside the triangle.
    X,Y=np.meshgrid( x_range,y_range )
    xc=np.mean(xs)
    yc=np.mean(ys)

    # From the array 'triangle', points that lie outside the triangle will be
    # set to 'False'.
    triangle = np.ones(X.shape,dtype=bool)
    for i in range(3):
        ii=(i+1)%3
        if xs[i]==xs[ii]:
            include = X *(xc-xs[i])/abs(xc-xs[i]) > xs[i] *(xc-xs[i])/abs(xc-xs[i])
        else:
            poly=np.poly1d([(ys[ii]-ys[i])/(xs[ii]-xs[i]),ys[i]-xs[i]*(ys[ii]-ys[i])/(xs[ii]-xs[i])])
            include = Y *(yc-poly(xc))/abs(yc-poly(xc)) > poly(X) *(yc-poly(xc))/abs(yc-poly(xc))
        triangle*=include

    # Output: 2 arrays with the x- and y- coordinates of the points inside the
    # triangle.
    return X[triangle],Y[triangle]