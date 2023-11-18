import Muse_S_reader
import synthesizer
import time
import numpy as np

def main():
    startTime = time.time()
    fullOutput = np.empty(0)
    while True:
        refTime = round(time.time() - startTime)
        l1, l2, l3, l4 = Muse_S_reader.process_waveform(i/4,(i+1)/4)
        fullOutput = synthesizer.main([a, a1, a2], [b, b1, b2], [c, c1, c2], [d, d1, d2], l1, l2, l3, l4, 'Audio1', fullOutput)
        time.sleep(10)
        l1, l2, l3, l4 = Muse_S_reader.process_waveform(i/4,(i+1)/4)
        fullOutput = synthesizer.main([a, a1, a2], [b, b1, b2], [c, c1, c2], [d, d1, d2], l1, l2, l3, l4, 'Audio2', fullOutput)


if __name__ == "__main__":
    main()