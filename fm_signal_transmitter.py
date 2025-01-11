import numpy as np
import sounddevice as sd

#define dec2bin converter

roadId = 234824378
carId = 824733
def dec2bin(n):
    if n ==0:
        return "0"
    elif n==1:
        return "1"
    else:
        remainder = n%2
        return dec2bin(n//2) + str(remainder) 

bin_data_road = dec2bin(roadId)
bin_data_car = dec2bin(carId)


# Define constants
sampling_rate = 44100  # Sampling rate in Hz (standard audio quality)
carrier_frequency = 100000  # Carrier frequency for FM (100 kHz)
modulation_index = 5  # Modulation index for FM
bit_rate = 1000  # Bit rate (bits per second)
duration_per_bit = 1 / bit_rate  # Duration of each bit in seconds
binary_data = "1010101010111100"  # Sample binary data to be transmitted

# Time axis for each bit duration
t_bit = np.arange(0, duration_per_bit, 1 / sampling_rate)

# Create the carrier signal (FM carrier) at the base frequency
def generate_fm_signal(binary_data, carrier_frequency, modulation_index):
    fm_signal = np.array([])  # Empty array to hold the FM signal
    for bit in binary_data:
        # Modulate the carrier frequency based on binary data (0 or 1)
        if bit == '1':
            message_freq = 1000  # High frequency for bit '1'
        else:
            message_freq = 500  # Low frequency for bit '0'
        
        # Generate the message signal for the bit (binary modulation)
        message_signal = np.sin(2 * np.pi * message_freq * t_bit)
        
        # Create FM modulated signal
        fm_wave = np.sin(2 * np.pi * carrier_frequency * t_bit + modulation_index * message_signal)
        
        # Append the FM modulated wave for this bit to the overall signal
        fm_signal = np.concatenate((fm_signal, fm_wave))
        
    return fm_signal

# Generate FM signal for the binary data
fm_signal = generate_fm_signal(binary_data, carrier_frequency, modulation_index)

# Normalize the FM signal to prevent clipping
fm_signal = fm_signal / np.max(np.abs(fm_signal))

# Play the FM signal (simulation, would output sound instead of transmitting via radio)
sd.play(fm_signal, samplerate=sampling_rate)

# Wait for the signal to finish playing
sd.wait()
