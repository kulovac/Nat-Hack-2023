# Single-Voice Synthesizer
# input: 4 lists
# output: some sort of sound file
# 40 - 120, 120 - 400, 400-1000, 100 - 5000

import numpy as np
import scipy.io.wavfile as wav
import random

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
m1= mapFreqBounds(map1)
m2 = mapFreqBounds(map2)
m3 = mapFreqBounds(map3)
m4 = mapFreqBounds(map4)

def chooseMap(freq):
    if map1[0] <= freq and map1[1] >= freq:
        return(m1[0] * m1[1] ** freq)
    elif map2[0] <= freq and map2[1] >= freq:
        return(m2[0] * m2[1] ** freq)
    elif map3[0] <= freq and map3[1] >= freq:
        return(m3[0] * m3[1] ** freq)
    elif map4[0] <= freq and map4[1] >= freq:
        return(m4[0] * m4[1] ** freq)

def synthesize(time: int, sampleRate: int, gain: int, frequency: int, wavetable : np.ndarray):
    #Main Function

    time = 5
    waveform = np.sin

    wavetableLength = 8
    wavetable = np.zeros((wavetableLength,))

    for i in range(wavetableLength):
        wavetable[i] = waveform(2* np.pi * i / wavetableLength)

    output = np.zeros((time * sampleRate,))

    index = 0
    indexIncrement = frequency * wavetableLength / sampleRate
    
    for n in range(output.shape[0]):
        output[n] = wavetable[int(np.floor(index))]
        index += indexIncrement
        index %= wavetableLength

    volume = 10 ** (-gain / 20)
    output *= volume

    return output

def main(inFreqList1, inFreqList2, inFreqList3, inFreqList4, waveTable1, waveTable2, waveTable3, waveTable4):
    time = 3
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
    
    wav.write('Audio.wav', sampleRate, output.astype(np.float32))


if __name__ == "__main__":
    random.seed(100)
    l1, l2, l3, l4 = [], [], [], []
    for i in range(8):
        l1.append(random.random())
        l2.append(random.random())
        l3.append(random.random())
        l4.append(random.random())
    print(l1)
    main([5], [15], [35], [65], l1, l2, l3, l4)
