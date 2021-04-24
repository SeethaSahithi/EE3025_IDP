import numpy as np
import soundfile as sf
from scipy import signal
import matplotlib.pyplot as plt

def  plot_fft(signal, title, fs):
    plt.figure(figsize=(6,4))
    N = len(signal)
    T = 1/fs
    fft  = np.abs(np.fft.fft(signal))
    fft = fft[0:N//2]
    freq = np.fft.fftfreq(signal.size, d=T)
    freq = freq[:N//2]
    return freq, fft;
    plt.plot(freq, fft)
    return fft, freq

input_signal, fs = sf.read('Sound_Noise.wav')
np.savetxt("Sound_Noise.dat",input_signal)
sample_freq = fs 

cutoff_freq=2750
print('cutoff_freq is',cutoff_freq)
order=4
Wn = 2.4*cutoff_freq/sample_freq

b, a = signal.butter(order, Wn, 'low')
temp = input_signal.copy()

#cascading filter
for i in range(20):
    temp = signal.filtfilt(b, a, temp)

plt.figure(1)
original_fft, freq = plot_fft(input_signal, 'before', fs)
plt.plot(original_fft,freq)
plt.xlim([0,5000])
plt.title("origianl")
plt.savefig('es18btech11015_Original.eps')
plt.savefig('es18btech11015_Original.png')

plt.figure(2)  
filtered_fft, freq = plot_fft(temp, 'after-1', fs)
plt.plot(filtered_fft,freq)
plt.xlim([0,5000])
plt.title("filtered")
plt.savefig('es18btech11015_filtered.eps')
plt.savefig('es18btech11015_filtered.png')
plt.show()

sf.write('BetterreducedNoise.wav', temp , fs) 
np.savetxt("BetterreducedNoise.dat",temp)

original_beforecutoff = 0
filtered_beforecutoff = 0
original_aftercutoff= 0
filtered_aftercutoff = 0

for i in range(len(freq)):
    if freq[i]<cutoff_freq:
        original_beforecutoff += original_fft[i]
        filtered_beforecutoff += filtered_fft[i]
    else:
        original_aftercutoff += original_fft[i]
        filtered_aftercutoff += filtered_fft[i]
        
print('Pre fraction: ', original_beforecutoff/original_fft.sum(), filtered_beforecutoff/filtered_fft.sum())
print('Post fraction: ', original_aftercutoff/original_fft.sum(), filtered_aftercutoff/filtered_fft.sum())