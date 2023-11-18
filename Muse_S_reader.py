"""
Given the Muse S, the program will read data
into a csv file and convert the data into the
frequency domain while filtering out the 60Hz
powerline frequency
"""

import numpy as np
import matplotlib.pyplot as plt

SAMPLES_PER_SECOND = 256  # 256Hz sample rate


def FFT_Filter(signal):
    """
    Computes the FFT of the signal
    and removes the POWERLINE_FREQ
    TODO: 
    """
    global SAMPLES_PER_SECOND

    fft_signal = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(signal), 1 / SAMPLES_PER_SECOND)

    fft_signal = fft_signal[1:len(signal)//2]
    freq = freq[1:len(freq)//2]

    # cutoff at 50Hz as beta waves do not go past this value
    max_freq = np.abs(freq - 50).argmin()

    freq = freq[1:max_freq]
    fft_signal = fft_signal[1:max_freq]

    return (fft_signal, freq)


def read(filename, start, end):
    """
    reads all values from a start time and
    end time where time is dictated by the
    sample rate
    """
    global SAMPLES_PER_SECOND
    wave1 = np.array([])
    wave2 = np.array([])
    wave3 = np.array([])
    wave4 = np.array([])

    start_index = int(start * SAMPLES_PER_SECOND)
    with open(filename, "r") as infile:
        lines = infile.readlines()
        end_index = min(len(lines), int(end * SAMPLES_PER_SECOND))

        for i in range(start_index, end_index):  # reads in the four waves
            values = lines[i].strip().split(",")
            wave1 = np.append(wave1, float(values[0]))
            wave2 = np.append(wave2, float(values[1]))
            wave3 = np.append(wave3, float(values[2]))
            wave4 = np.append(wave4, float(values[3]))

    return (wave1, wave2, wave3, wave4)


def process_waveform(start, end, debug=False):
    """
    process the waveforms from start time
    to end time.
    Returns four np arrays containing voltage
    as a function of time containing only
    the frequencies in the interval (0Hz, 50Hz].
    """
    wave1, wave2, wave3, wave4 = read(
        "./EEG Data/sample2.csv", start, end)

    if debug:
        plt.plot(wave1)
        plt.show()

    fft1, freq1 = FFT_Filter(wave1)
    fft2, freq2 = FFT_Filter(wave2)
    fft3, freq3 = FFT_Filter(wave3)
    fft4, freq4 = FFT_Filter(wave4)

    if debug:
        plt.plot(freq1, np.sqrt(fft1.real ** 2 + fft1.imag ** 2))
        plt.show()

    filt_wave1 = abs(np.fft.ifft(fft1))
    filt_wave2 = abs(np.fft.ifft(fft2))
    filt_wave3 = abs(np.fft.ifft(fft3))
    filt_wave4 = abs(np.fft.ifft(fft4))

    if debug:
        plt.plot(filt_wave1)
        plt.show()

    return (filt_wave1, filt_wave2, filt_wave3, filt_wave4)


if __name__ == "__main__":
    process_waveform(9, 10, True)
