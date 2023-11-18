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
m1= mapFreqBounds(map1)
m2 = mapFreqBounds(map2)
m3 = mapFreqBounds(map3)
m4 = mapFreqBounds(map4)
prevOutput = np.empty(0)

def chooseMap(freq):
    if map1[0] <= freq and map1[1] >= freq:
        return(m1[0] * m1[1] ** freq)
    elif map2[0] <= freq and map2[1] >= freq:
        return(m2[0] * m2[1] ** freq)
    elif map3[0] <= freq and map3[1] >= freq:
        return(m3[0] * m3[1] ** freq)
    elif map4[0] <= freq and map4[1] >= freq:
        return(m4[0] * m4[1] ** freq)

def synthesize(time: float, sampleRate: int, gain: int, frequency: int, wavetable : np.ndarray):
    #Main Function
    waveform = np.sin

    wavetableLength = 64
    wavetable = np.zeros((wavetableLength,))

    for i in range(wavetableLength):
        wavetable[i] = waveform(2* np.pi * i / wavetableLength)

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
    attack = 3 # How long until volume peaks
    decay = 7 # How long until sustain is reached
    sustain = 9 # How long until volume decreases
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

def main(inFreqList1, inFreqList2, inFreqList3, inFreqList4, waveTable1, waveTable2, waveTable3, waveTable4):
    time = 1
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
    if prevOutput.size == 0:
        prevOutput = output
    else:
        prevOutput = np.append(prevOutput,output)
    wav.write('Audio1.wav', sampleRate, output.astype(np.float32))
    wav.write('Audio.wav', sampleRate, prevOutput.astype(np.float32))


if __name__ == "__main__":
    for i in range(10):
        a = random.randint(4,8)
        b = random.randint(10,20)
        c = random.randint(30,40)
        d = random.randint(60,70)
        l1, l2, l3, l4 = Muse_S_reader.process_waveform(i,i+1)
        main([a], [b], [c], [d], l1, l2, l3, l4)
