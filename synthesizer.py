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
    return (a,c)

sampleRate = 44100
map1 = [4, 8 , 40, 120]
map2 = [10, 20, 120, 400]
map3 = [30, 40, 400, 1000]
map4 = [60, 70, 1000, 5000]
notes = [41.2, 43.65, 46.25, 49.0, 51.91, 55.0, 58.27, 61.74, 65.41, 69.3, 73.42, 77.78, 82.41, 87.31, 92.5, 98.0, 103.83, 110.0, 116.54, 123.47, 130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.0, 196.0, 207.65, 220.0, 233.08, 246.94, 261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.0, 415.3, 440.0, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.0, 932.33, 987.77, 1046.5, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.0, 1864.66, 1975.53, 2093.0, 2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.0, 3729.31, 3951.07, 4186.01, 4434.92, 4698.63, 4978.03]
m1= mapFreqBounds(map1)
m2 = mapFreqBounds(map2)
m3 = mapFreqBounds(map3)
m4 = mapFreqBounds(map4)
prevOutput = np.empty(0)

def chooseMap(freq):
    if map1[0] <= freq and map1[1] >= freq:
        preFreq = m1[0] * m1[1] ** freq
    elif map2[0] <= freq and map2[1] >= freq:
        preFreq = m2[0] * m2[1] ** freq
    elif map3[0] <= freq and map3[1] >= freq:
        preFreq = m3[0] * m3[1] ** freq
    elif map4[0] <= freq and map4[1] >= freq:
        preFreq = m4[0] * m4[1] ** freq
    return(search(preFreq))

def search(freq):

def synthesize(time: float, sampleRate: int, gain: int, frequency: int, wavetable : np.ndarray):
    #Main Function
    waveform = np.sin

    wavetableLength = wavetable.size

    output = np.empty(int(time*sampleRate))

    index = 0
    indexIncrement = frequency * wavetableLength / sampleRate
    
    for n in range(output.shape[0]):
        output[n] = wavetable[int(np.floor(index))]
        index += indexIncrement
        index %= wavetableLength

    ### ADSR ENVELOPE SETTINGS
    #Attack, Decay, Sustain are 10% increments of clip
    # Attack at 2 means peak volume at 20%, etc.
    attack = 1 # How long until volume peaks
    decay = 4 # How long until sustain is reached
    sustain = 5 # How long until volume decreases
    release = 4 # How fast volume drops (exponential)

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

    ### END ADSR ENVELOPE SETTINGS
    #TO REVERT, REPLACE ABOVE LOOP WITH: output *= volume

    return output

def main(inFreqList1, inFreqList2, inFreqList3, inFreqList4, waveTable1, waveTable2, waveTable3, waveTable4, filename, fullOutput):
    time = 0.8
    volumeReduction = 20
    for freq in inFreqList1:
        if freq == inFreqList1[0]:
            output = synthesize(time, sampleRate, volumeReduction, chooseMap(freq), waveTable1)
        else:
            output += synthesize(time, sampleRate, volumeReduction, chooseMap(freq), waveTable1)
    for freq in inFreqList2:
        output += synthesize(time, sampleRate, volumeReduction, chooseMap(freq), waveTable2)
    for freq in inFreqList3:
        output += synthesize(time, sampleRate, volumeReduction, chooseMap(freq), waveTable3)
    for freq in inFreqList4:
        output += synthesize(time, sampleRate, volumeReduction, chooseMap(freq), waveTable4)
    global prevOutput
    if fullOutput.size == 0:
        fullOutput = output
    if prevOutput.size == 0:
        prevOutput = output
    else:
        prevOutput = np.append(prevOutput,output)
    wav.write('Audio', sampleRate, fullOutput.astype(np.float32))
    wav.write(filename, sampleRate, prevOutput.astype(np.float32))
    return (fullOutput)


if __name__ == "__main__":
    for i in range(20):
        a = random.randint(4,8)
        a1 = random.randint(4,8)
        a2 = random.randint(4,8)
        b = random.randint(10,20)
        b1 = random.randint(10,20)
        b2 = random.randint(10,20)
        c = random.randint(30,40)
        c1 = random.randint(30,40)
        c2 = random.randint(30,40)
        d = random.randint(60,70)
        d1 = random.randint(60,70)
        d2 = random.randint(60,70)
        l1, l2, l3, l4 = Muse_S_reader.process_waveform(i/4,(i+1)/4)
        main([a, a1, a2], [b, b1, b2], [c, c1, c2], [d, d1, d2], l1, l2, l3, l4)
