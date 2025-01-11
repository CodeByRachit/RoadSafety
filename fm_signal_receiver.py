import numpy as np
import scipy.signal as signal
from rtlsdr import RtlSdr
import matplotlib.pyplot as plt

# Define parameters
sample_rate = 2.048e6  # RTL-SDR default sample rate (2.048 MHz)
center_freq = 100e6    # FM radio frequency to tune to (e.g., 100 MHz for FM)
duration = 10          # Duration of data capture (in seconds)

# Initialize RTL-SDR device
sdr = RtlSdr()
sdr.sample_rate = sample_rate  # Set the sample rate
sdr.center_freq = center_freq  # Set the center frequency to the FM station
sdr.gain = 'auto'  # Automatic gain control
sdr.offset = 0  # No frequency offset

# Capture data
print("Capturing data from FM station...")
samples = sdr.read_samples(duration * sample_rate)

# Close the SDR device
sdr.close()

# Visualize the captured signal (optional)
plt.figure()
plt.plot(np.real(samples[:1000]))  # Plot first 1000 samples for illustration
plt.title('Captured FM Signal')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.show()

# Step 1: Demodulate the FM signal

# Calculate the instantaneous frequency (phase difference)
instantaneous_phase = np.angle(samples[1:] * np.conj(samples[:-1]))  # Phase difference between consecutive samples

# Derive the frequency from phase (in Hz)
demodulated_signal = np.diff(instantaneous_phase) * sample_rate / (2 * np.pi)

# Visualize the demodulated signal (frequency shift)
plt.figure()
plt.plot(demodulated_signal[:1000])  # Plot first 1000 samples of demodulated signal
plt.title('Demodulated Signal')
plt.xlabel('Sample Index')
plt.ylabel('Frequency (Hz)')
plt.show()

# Step 2: Decode binary data from the demodulated signal

# Apply a bandpass filter to isolate the binary data frequency (e.g., BPSK)
low_cut = 500   # Lower bound of the binary data frequency
high_cut = 1500  # Upper bound of the binary data frequency
nyquist = 0.5 * sample_rate
low = low_cut / nyquist
high = high_cut / nyquist
b, a = signal.butter(4, [low, high], btype='band')

filtered_signal = signal.filtfilt(b, a, demodulated_signal)

# Step 3: Detect the binary data
# Apply a threshold to convert the frequency shifts into 0s and 1s
threshold = np.median(filtered_signal)
binary_data = np.where(filtered_signal > threshold, 1, 0)

# Display the decoded binary data
print("Decoded Binary Data:")
print(binary_data[:100])  # Show the first 100 bits of the decoded binary data

# Store and sort binary data in bcd system(0-9)
s = str(binary_data[:100])
def split_string(s, n):
    interval_size = len(s) // n
    print(len(s))
    intervals = []
    start = 0
    for i in range(interval_size):
        end = start + 4
        intervals.append(s[start:end])
        start = end
    return intervals

# Example usage:
s = "abcdefghijklmnopqrstuvwxyzab" # should have 4 multiple characters
n = 4
print(split_string(s, n))  # Output: ['abcd', 'efgh', 'ijkl', 'mnop']


#converting bcd characters to decimal to note car ID and road ID

for i in intervals:
    bin = int(i)
    dec = 0
    result = []
    while bin!=0:
        a = bin%10
        i = 0
        dec += a*(2**i)
        bin = bin//10
        i += 1
    else:
        result.append(dec)

final_result = str(result)

# Optionally, you could now decode this binary data into ASCII characters, or whatever format the original message is in.
