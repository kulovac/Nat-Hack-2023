"""
Given the Muse S, the program will read data
into a csv file and convert the data into the
frequency domain while filtering out the 60Hz
powerline frequency
"""

from brainflow.data_filter import (
    DataFilter,
    FilterTypes,
    AggOperations,
    WindowFunctions,
    DetrendOperations,
)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from Board import Board, get_board_id

SAMPLES_PER_SECOND = 256  # 256Hz sample rate
board = None


def FFT_Filter(signal):
    """
    Computes the FFT of the signal
    and removes the upper frequency
    """
    global SAMPLES_PER_SECOND
    CUTOFF_FREQ = 50

    fft_signal = np.fft.fft(signal)
    freq = np.fft.fftfreq(len(signal), 1 / SAMPLES_PER_SECOND)

    fft_signal = fft_signal[1:len(signal)//2]
    freq = freq[1:len(freq)//2]

    # cutoff at 50Hz as beta waves do not go past this value
    max_freq = np.abs(freq - CUTOFF_FREQ).argmin()

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


def read_live(interval, filename="sample.csv", debug=False):
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


def process_waveform(start, end, live=False, filename="./EEG Data/sample3-awake.csv", debug=False):
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
    filt_wave1 = np.fft.ifft(fft1)
    filt_wave2 = np.fft.ifft(fft2)
    filt_wave3 = np.fft.ifft(fft3)
    filt_wave4 = np.fft.ifft(fft4)

    if debug:
        plt.plot(filt_wave1)
        plt.show()

    return (normalize(filt_wave1, filt_wave2, filt_wave3, filt_wave4))


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = np.array([])
ys = np.array([])


# TEMP DEBUGGING FUNCTION
def animate(i, xs, ys):
    w1 = process_waveform(1, 1.1, live=True, debug=False)[0]

    # Add x and y to lists
    # xs = np.concatenate((xs, np.linspace()))
    ys = np.concatenate((ys, w1))

    # Limit x and y lists to 20 items
    # xs = xs[-1000:]
    ys = ys[-1000:]

    # Draw x and y lists
    ax.clear()
    ax.plot(ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')


if __name__ == "__main__":
    # w1 = np.array([])
    # w2 = np.array([])
    # w3 = np.array([])
    # w4 = np.array([])

    # index = 0
    # while index < 5:
    #     index += 1
    #     update = process_waveform(1, 2, live=True, debug=False)
    #     w1 = np.append(w1, update[0])
    #     w2 = np.append(w2, update[1])
    #     w3 = np.append(w3, update[2])
    #     w4 = np.append(w4, update[3])
    # plt.plot(w1)
    # plt.show()
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
    plt.show()
