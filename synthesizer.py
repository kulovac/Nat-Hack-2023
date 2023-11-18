# Single-Voice Synthesizer

import numpy as np
import scipy.io.wavfile as wav

def synthesize(time: int, sampleRate: int, gain: int, frequency: int, wavetable : np.ndarray):
    #Main Function

    time = 5
    waveform = np.sin

    wavetableLength = 64
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

def main():
    sampleRate = 44100
    freq = 440
    time = 3
    volumeReduction = 20
    numpyArray = [0] #Placeholder for now
    output = synthesize(time, sampleRate, volumeReduction, freq, numpyArray)
    wav.write('Audio.wav', sampleRate, output.astype(np.float32))


if __name__ == "__main__":
    main()
