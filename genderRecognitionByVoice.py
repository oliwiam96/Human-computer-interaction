from __future__ import division

import os
import re
import sys

import scipy.io.wavfile
from scipy.fftpack import fft
import wave
import scipy.signal as decim

from scipy.io import wavfile

def testForAll():
    ile_ok = 0
    ile = 0
    for file in os.listdir('./'):
        if re.match('^.*\.wav$', file) and not re.match('err.wav$', file) and not re.match('kopia.wav$', file):
            decision = WhichSex(file)
            name = file
            name = name[:-4]
            name = name[-1]

            if name == decision:
                ile_ok += 1
        ile += 1
    print("ile ok ", ile_ok)
    print("ile  w sumie ", ile)

def WhichSex(nazwa):
    copyName = 'copy.wav'
    if nazwa == copyName:
        copyName = "copy2.wav"
    # fixing opening the file
    waveFile = wave.open(nazwa, 'r')
    copy = wave.open(copyName, 'w')
    copy.setnchannels(waveFile.getnchannels())
    copy.setsampwidth(waveFile.getsampwidth())
    copy.setframerate(waveFile.getframerate())
    copy.setnframes(waveFile.getnframes())
    copy.writeframes(waveFile.readframes(waveFile.getnframes()))
    copy.close()

    w, signal = scipy.io.wavfile.read(copyName) #w- czest probkowania
    if waveFile.getnchannels() > 1:
        signal = [s[0] for s in signal]   #Tylko pierwszy kanał
    f_signal = fft(signal)
    f_signal = abs(f_signal)


    #print(f_signal)
    for i in range(len(f_signal)):
        if i/len(signal)*w < 60:  # for freq < 60 it is definetely not a human voice- set to zero
            f_signal[i] = 0

    f_signal_2 = decim.decimate(x = f_signal, q = 2, zero_phase = True)
    f_signal_3 = decim.decimate(x = f_signal, q = 3, zero_phase = True)
    f_signal_4 = decim.decimate(x = f_signal, q = 4, zero_phase = True)

    f_wynik = f_signal_4
    for i in range(len(f_signal_4)):
        f_wynik[i] = f_signal[i] * f_signal_2[i] * f_signal_3[i] * f_signal_4[i]
    indexOfMaxi = 0
    maxi = f_wynik[0]
    for i in range(len(f_wynik)):
        if f_wynik[i] > maxi:
            maxi = f_wynik[i]
            indexOfMaxi = i

    f_voice = (indexOfMaxi/len(signal))* w #czest glosu (wynik)
    if f_voice < 175: #decyzja
        return 'M'
    else:
        return 'K'

    waveFile.close()

if __name__ == "__main__":
    print(WhichSex(sys.argv[1]))
