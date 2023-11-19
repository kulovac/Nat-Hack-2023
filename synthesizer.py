# Single-Voice Synthesizer
# input: 4 lists
# output: some sort of sound file
# 40 - 120, 120 - 400, 400-1000, 100 - 5000

import numpy as np
import scipy.io.wavfile as wav
import random
import Muse_S_reader


def mapFreqBounds(map):
    Flow = map[0]
    Fhigh = map[1]
    mapLow = map[2]
    mapHigh = map[3]
    d = Fhigh / Flow
    a = (mapLow**d/mapHigh)**(1/(d-1))
    c = (mapLow / a)**(1/Flow)
    return (a, c)


sampleRate = 44100
map1 = [1, 6, 40, 120]
map2 = [6, 15, 120, 400]
map3 = [15, 30, 400, 1000]
map4 = [30, 50, 1000, 5000]
# C Major
notesList = {'A': [55.0, 110.0, 220.0, 440.0, 880.0, 1760.0, 3520.0],
             'B': [61.74, 123.47, 246.94, 493.88, 987.77, 1975.53, 3951.07],
             'C': [65.41, 130.81, 261.63, 523.25, 1046.5, 2093.0, 4186.01],
             'D': [73.42, 146.83, 293.66, 587.33, 1174.66, 2349.32, 4698.63],
             'E': [41.2, 82.41, 164.81, 329.63, 659.25, 1318.51, 2637.02],
             'F': [43.65, 87.31, 174.61, 349.23, 698.46, 1396.91, 2793.83],
             'G': [49.0, 98.0, 196.0, 392.0, 783.99, 1567.98, 3135.96],
             'A#/Bb': [58.27, 116.54, 233.08, 466.16, 932.33, 1864.66, 3729.31],
             'F#/Gb': [46.25, 92.5, 185.0, 369.99, 739.99, 1479.98, 2959.96],
             'C#/Db': [69.3, 138.59, 277.18, 554.37, 1108.73, 2217.46, 4434.92],
             'D#/Eb': [77.78, 155.56, 311.13, 622.25, 1244.51, 2489.02, 4978.03],
             'G#/Ab': [51.91, 103.83, 207.65, 415.3, 830.61, 1661.22, 3322.44]}
m1 = mapFreqBounds(map1)
m2 = mapFreqBounds(map2)
m3 = mapFreqBounds(map3)
m4 = mapFreqBounds(map4)
prevOutput = np.empty(0)


def chooseMap(freq, keysPressed):
    notes = []
    if keysPressed == []:
        keysPressed = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                       'A#/Bb', 'F#/Gb', 'C#/Db', 'D#/Eb', 'G#/Ab']
    for key in keysPressed:
        notes += notesList[key]
    if map1[0] <= freq and map1[1] >= freq:
        preFreq = m1[0] * m1[1] ** freq
    elif map2[0] <= freq and map2[1] >= freq:
        preFreq = m2[0] * m2[1] ** freq
    elif map3[0] <= freq and map3[1] >= freq:
        preFreq = m3[0] * m3[1] ** freq
    elif map4[0] <= freq and map4[1] >= freq:
        preFreq = m4[0] * m4[1] ** freq
    return (search(preFreq, notes))


def search(freq, notes):
    if freq < notes[0]:
        return notes[0]
    if freq > notes[-1]:
        return notes[-1]

    if freq in notes:
        return freq
    else:
        if len(notes) == 2:
            if (freq - notes[0]) < (freq - notes[1]):
                return notes[0]
            else:
                return notes[1]
        else:
            middle = len(notes) // 2
            if freq < notes[middle]:
                return search(freq, notes[0:middle])
            else:
                return search(freq, notes[middle:])


def synthesize(time: float, sampleRate: int, gain: int, frequency: int, wavetable: np.ndarray):
    # Main Function
    waveform = np.sin

    wavetableLength = wavetable.size

    output = np.empty(int(time*sampleRate))

    index = 0
    indexIncrement = frequency * wavetableLength / sampleRate

    for n in range(output.shape[0]):
        output[n] = wavetable[int(np.floor(index))]
        index += indexIncrement
        index %= wavetableLength

    # ADSR ENVELOPE SETTINGS
    # Attack, Decay, Sustain are 10% increments of clip
    # Attack at 2 means peak volume at 20%, etc.
    attack = 1  # How long until volume peaks
    decay = 4  # How long until sustain is reached
    sustain = 5  # How long until volume decreases
    release = 4  # How fast volume drops (exponential)

    volume = 10 ** (-gain / 20)
    for n in range(output.shape[0]):
        if n < (44100 / 10) * attack:
            output[n] *= volume * (((n)/(4410 * attack)))
        elif n < (44100 / 10) * decay:
            newVolume = volume / (((n)/(4410 * attack)))
            if newVolume >= volume * 0.7:
                output[n] *= newVolume
            else:
                output[n] *= volume * 0.7
        elif n < (44100 / 10) * sustain:
            output[n] *= volume * 0.7
        else:
            newVolume = volume / ((((n)/(4410 * sustain)))**release)
            if newVolume <= volume * 0.7:
                output[n] *= newVolume
            else:
                output[n] *= volume * 0.7

    # END ADSR ENVELOPE SETTINGS
    # TO REVERT, REPLACE ABOVE LOOP WITH: output *= volume

    return output


def main2(inFreqList1, inFreqList2, inFreqList3, inFreqList4, waveTable1, waveTable2, waveTable3, waveTable4, filename, fullOutput, keysPressed):
    time = 1
    volumeReduction = 20
    for freq in inFreqList1:
        if freq == inFreqList1[0]:
            output = synthesize(time, sampleRate, volumeReduction, chooseMap(
                freq, keysPressed), waveTable1)
        else:
            output += synthesize(time, sampleRate, volumeReduction,
                                 chooseMap(freq, keysPressed), waveTable1)
    for freq in inFreqList2:
        output += synthesize(time, sampleRate, volumeReduction,
                             chooseMap(freq, keysPressed), waveTable2)
    for freq in inFreqList3:
        output += synthesize(time, sampleRate, volumeReduction,
                             chooseMap(freq, keysPressed), waveTable3)
    for freq in inFreqList4:
        output += synthesize(time, sampleRate, volumeReduction,
                             chooseMap(freq, keysPressed), waveTable4)
    global prevOutput
    if fullOutput.size == 0:
        fullOutput = output
    else:
        fullOutput = np.append(fullOutput, output)
    if prevOutput.size == 0:
        prevOutput = output
    else:
        prevOutput = np.append(prevOutput, output)
    wav.write('Audio.wav', sampleRate, fullOutput.astype(np.float32))
    wav.write(filename, sampleRate, prevOutput.astype(np.float32))
    return (fullOutput)


def main(filename, fullOutput):
    global prevOutput
    prevOutput = np.empty(0)
    keysPressed = ['D', 'F', 'A', 'A#/Bb', 'D', 'D', 'G']
    for i in range(5):
        # a = random.randint(4,8)
        # a1 = random.randint(4,8)
        # a2 = random.randint(4,8)
        # b = random.randint(10,20)
        # b1 = random.randint(10,20)
        # b2 = random.randint(10,20)
        # c = random.randint(30,40)
        # c1 = random.randint(30,40)
        # c2 = random.randint(30,40)
        # d = random.randint(60,70)
        # d1 = random.randint(60,70)
        # d2 = random.randint(60,70)
        # l1, l2, l3, l4 = Muse_S_reader.process_waveform(i/4,(i+1)/4)
        a, a1, a2 = Muse_S_reader.process_waveform(i, i+1, live=True)[1][0]
        b, b1, b2 = Muse_S_reader.process_waveform(i, i+1, live=True)[1][1]
        c, c1, c2 = Muse_S_reader.process_waveform(i, i+1, live=True)[1][2]
        d, d1, d2 = Muse_S_reader.process_waveform(i, i+1, live=True)[1][3]
        l1, l2, l3, l4 = Muse_S_reader.process_waveform(i, i + 1, live=True)[0]
        fullOutput = main2([a, a1, a2], [b, b1, b2], [c, c1, c2], [
                           d, d1, d2], l1, l2, l3, l4, filename, fullOutput, keysPressed)
    return (fullOutput)


if __name__ == "__main__":
    a = main('audio1.wav', np.empty(0))
