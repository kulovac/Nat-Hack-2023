"""
Given the Muse S, the program will read data
from a csv file OR directly from the Muse S 
and convert the data into the frequency domain 
while filtering out frequencies higher than 50Hz
"""

from brainflow.data_filter import (
    DataFilter,
    FilterTypes,
    AggOperations,
    WindowFunctions,
    DetrendOperations,
)
import numpy as np
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from Board import Board, get_board_id

SAMPLES_PER_SECOND = 256  # 256Hz sample rate
board = None


def FFT_Filter(signal):
    """
    Computes the FFT of the signal
    and removes the upper frequency
    Return: 4 fft's of the waves
    and the 3 most prominent frequencies
    of the brain wave
    """
    global SAMPLES_PER_SECOND
    CUTOFF_FREQ = 50
    TOLERANCE = 2

    fft_signal = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(signal), 1 / SAMPLES_PER_SECOND)
    peak_freq = np.array([])

    fft_signal = fft_signal[1:len(signal)//2]
    freq = freq[1:len(freq)//2]

    # cutoff at 50Hz as beta waves do not go past this value
    cutoff_index = np.abs(freq - CUTOFF_FREQ).argmin()

    freq = freq[1:cutoff_index]
    fft_signal = fft_signal[1:cutoff_index]

    temporary = fft_signal.copy()
    for _ in range(3):
        index = temporary.argmax()
        peak_freq = np.append(peak_freq, freq[index])
        temporary[index-TOLERANCE: index+TOLERANCE] = 0

    return (fft_signal, peak_freq)


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


def read_live(interval):
    """
    reads voltage values from the Muse S
    in some time interval
    """
    board_id = 39
    global SAMPLES_PER_SECOND
    global board

    if board == None:
        board = Board(board_id=board_id)
        time.sleep(2)

    data = board.get_data_quantity(int(interval*SAMPLES_PER_SECOND))
    exg_channels = board.get_exg_channels()

    return data[exg_channels, :]


def normalize(w1, w2, w3, w4):
    aw1, aw2, aw3, aw4 = abs(w1), abs(w2), abs(w3), abs(w4)
    max1, max2, max3, max4 = max(aw1), max(aw2), max(aw3), max(aw4)
    for i in range(len(w1)):
        w1[i] = w1[i]/max1
        w2[i] = w2[i]/max2
        w3[i] = w3[i]/max3
        w4[i] = w4[i]/max4
    return (w1, w2, w3, w4)


def process_waveform(start, end, live=False, filename="./EEG Data/sample3-awake.csv"):
    """
    process the waveforms from start time
    to end time.
    Returns four np arrays containing voltage
    as a function of time containing only
    the frequencies in the interval (0Hz, 50Hz].
    """
    if live:
        wave1, wave2, wave3, wave4 = read_live(end-start)
    else:
        wave1, wave2, wave3, wave4 = read(filename, start, end)

    fft1, freq1 = FFT_Filter(wave1)
    fft2, freq2 = FFT_Filter(wave2)
    fft3, freq3 = FFT_Filter(wave3)
    fft4, freq4 = FFT_Filter(wave4)

    filt_wave1 = np.fft.ifft(fft1)
    filt_wave2 = np.fft.ifft(fft2)
    filt_wave3 = np.fft.ifft(fft3)
    filt_wave4 = np.fft.ifft(fft4)

    return (normalize(filt_wave1, filt_wave2, filt_wave3, filt_wave4), (freq1, freq2, freq3, freq4))
