import Muse_S_reader
import synthesizer
import time
import numpy as np

def main():
    fullOutput = np.empty(0)
    i = 0
    while i < 3:
        startTime = time.time()
        fullOutput = synthesizer.main('UIPackage/Audio1.wav', fullOutput)
        fullOutput = synthesizer.main('UIPackage/Audio2.wav', fullOutput)
        print(time.time() - startTime)
        i += 1

if __name__ == "__main__":
    main()