import pygame
import numpy as np
import matplotlib.pyplot as plt

def create_sine_wave(frequency, volume : float = 1.0, harmonics : list[float] = [], duration = 10, sample_rate = 44100):
    number_of_samples = int(sample_rate * duration)


    time = np.linspace(0, duration, number_of_samples)
    
    wave = volume*np.sin(2*np.pi*frequency*time)

    if len(harmonics) > 0:
        for i in range(len(harmonics)):
            wave += volume*harmonics[i]*np.sin(2*(i+2)*np.pi*frequency*time)

    wave *= 1/(max(wave)+0.1)

    return wave

def create_square_wave(frequency, volume : float = 1.0, harmonics : list[float] = [], duration = 10, sample_rate = 44100):
    number_of_samples = int(sample_rate * duration)


    time = np.linspace(0, duration, number_of_samples)
    
    wave = volume*np.sign(np.sin(2*np.pi*frequency*time))

    if len(harmonics) > 0:
        for i in range(len(harmonics)):
            wave += volume*harmonics[i]*np.sign(np.sin(2*(i+2)*np.pi*frequency*time))

    wave *= 1/(max(wave)+0.1)

    return wave

def create_sawtooth_wave(frequency, volume : float = 1.0, harmonics : list[float] = [], duration = 10, sample_rate = 44100):
    number_of_samples = int(sample_rate * duration)


    time = np.linspace(0, duration, number_of_samples)
    
    wave = volume*(2*(time*frequency-np.floor(time*frequency+0.5)))

    if len(harmonics) > 0:
        for i in range(len(harmonics)):
            wave += volume*harmonics[i]*(2*((i+2)*frequency*time-np.floor(time*(i+2)*frequency+0.5)))

    wave *= 1/(max(wave)+0.1)

    return wave

def create_wave(type, frequency, volume : float = 1.0, harmonics : list[float] = [], duration = 10, sample_rate = 44100):
    if type == "sine":
        return create_sine_wave(frequency, volume, harmonics, duration, sample_rate)
    elif type == 'square':
        return create_square_wave(frequency, volume, harmonics, duration, sample_rate)
    elif type == "sawtooth":
        return create_sawtooth_wave(frequency, volume, harmonics, duration, sample_rate)


def create_sound(wave, volume):
    final_wave = wave * volume

    audio = np.column_stack((final_wave * 32767, final_wave * 32767)).astype(np.int16).copy()
    sound = pygame.sndarray.make_sound(audio)

    return sound

if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.plot(create_sine_wave(11))
    plt.show()