import numpy as np
from scipy.signal import butter, lfilter, resample

'''
This methods are clearly explained in the .ipynb files
'''

# manteniendo la temporalidad de la señal
def get_slices(signal, freq):
    signals = []

    if freq == 500:
        while len(signal) > 2999:
            signals.append(resample(signal[:3000], 256))
            signal = signal[3001:]

    elif freq == 1000:
        while len(signal) > 5999:
            signals.append(resample(signal[:6000], 256))
            signal = signal[6001:]

    return signals


def bandpass_filter(data, lowcut, highcut, signal_freq, filter_order):

    nyquist_freq = 0.5 * signal_freq
    low = lowcut / nyquist_freq
    high = highcut / nyquist_freq
    b, a = butter(filter_order, [low, high], btype="band")
    y = lfilter(b, a, data)
    y[:5] = y[5]

    return y


def normalize(signal):
    signal -= np.mean(signal)
    minimum = np.amin(signal)
    maximum = np.amax(signal)

    return (signal - minimum) / (maximum - minimum)
