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

    if np.max(np.abs(wave)) > 0:
        wave = wave / np.max(np.abs(wave))

    return wave

def create_square_wave(frequency, volume : float = 1.0, harmonics : list[float] = [], duration = 10, sample_rate = 44100):
    number_of_samples = int(sample_rate * duration)


    time = np.linspace(0, duration, number_of_samples)
    
    wave = volume*np.sign(np.sin(2*np.pi*frequency*time))

    if len(harmonics) > 0:
        for i in range(len(harmonics)):
            wave += volume*harmonics[i]*np.sign(np.sin(2*(i+2)*np.pi*frequency*time))

    if np.max(np.abs(wave)) > 0:
        wave = wave / np.max(np.abs(wave))


    return wave

def create_sawtooth_wave(frequency, volume : float = 1.0, harmonics : list[float] = [], duration = 10, sample_rate = 44100):
    number_of_samples = int(sample_rate * duration)

    time = np.linspace(0, duration, number_of_samples)
    
    wave = volume*(2*(time*frequency-np.floor(time*frequency+0.5)))

    if len(harmonics) > 0:
        for i in range(len(harmonics)):
            wave += volume*harmonics[i]*(2*((i+2)*frequency*time-np.floor(time*(i+2)*frequency+0.5)))

    if np.max(np.abs(wave)) > 0:
        wave = wave / np.max(np.abs(wave))

    return wave

def create_triangle_wave(frequency, volume : float = 1.0, harmonics : list[float] = [], duration = 10, sample_rate = 44100):
    number_of_samples = int(sample_rate * duration)

    time = np.linspace(0, duration, number_of_samples)
    
    wave = volume*np.asin(np.sin(2*np.pi*frequency*time))

    if len(harmonics) > 0:
        for i in range(len(harmonics)):
            wave += volume*harmonics[i]*np.asin(np.sin(2*(i+2)*np.pi*frequency*time))

    if np.max(np.abs(wave)) > 0:
        wave = wave / np.max(np.abs(wave))

    return wave

def create_sine_frequency_sweep(f_start, f_end, duration, volume=1.0, sample_rate=44100):
    number_of_samples = int(sample_rate * duration)
    time = np.linspace(0, duration, number_of_samples)
    
    # Cálculo da fase para frequência variável
    # f(t) linear -> fase quadrática
    phase = 2 * np.pi * (f_start * time + (f_end - f_start) / (2 * duration) * time**2)
    
    wave = volume * np.sin(phase)
    
    # Normalização básica
    wave /= (np.max(np.abs(wave)) + 0.1)
    return wave

def create_exponential_sine_freq_decay(f_start, f_end, duration, volume=1.0, sample_rate=44100):
    number_of_samples = int(sample_rate * duration)
    time = np.linspace(0, duration, number_of_samples)
    
    # Cria uma curva de frequências que cai exponencialmente
    # Usamos o log para calcular a taxa de decaimento
    k = np.log(f_end / f_start) / duration
    # A integral de f_start * exp(k*t) é (f_start/k) * (exp(k*t) - 1)
    phase = 2 * np.pi * (f_start / k) * (np.exp(k * time) - 1)
    
    wave = volume * np.sin(phase)
    return wave

def create_wave(type, frequency, volume : float = 1.0, harmonics : list[float] = [], duration = 5, sample_rate = 44100):
    if type == "sine":
        return create_sine_wave(frequency, volume, harmonics, duration, sample_rate)
    elif type == 'square':
        return create_square_wave(frequency, volume, harmonics, duration, sample_rate)
    elif type == "sawtooth":
        return create_sawtooth_wave(frequency, volume, harmonics, duration, sample_rate)
    elif type == "triangle":
        return create_triangle_wave(frequency, volume, harmonics, duration, sample_rate)

def adsr_package(attack_time, delay_time, delay_end, sustain_end, wave, sample_rate = 44100):
    attack_time = int(sample_rate*attack_time)
    delay_time = int(sample_rate*delay_time)

    for x in range(len(wave)):
        if x <= attack_time:
            wave[x] = attack_package("exponential", x, wave[x], attack_time)
        elif x <= (delay_time+attack_time):
            value = wave[x]
            wave[x] = delay_package("exponential", x-attack_time, value, delay_time, delay_end)
        else:
            wave[x] *= -(x-(attack_time+delay_time))*((delay_end-sustain_end)/(len(wave)-(attack_time+delay_time)))+delay_end
    return wave

def attack_package(type : str, x : int, value : float, attack_time : int):
    if type == "parabolic":
        return value*((-(1/attack_time**2)*((x-attack_time)**2))+1)
    elif type == "exponential":
        return value*((1/attack_time**2)*(x**2))
    elif type == "linear":
        return value*x*(1/attack_time)
    elif type == "logarithmic":
        return value*(2**(10*(x/attack_time-1)))
    else:
        return 1/0

def delay_package(type, x, value, delay_time, delay_end):
    if type == "exponential":
        return value*((((1-delay_end)/(delay_time**2))*((x-delay_time)**2))+delay_end)
    elif type == "parabolic":
        return value*(((-delay_end/delay_time)*(x**2))+1)
    elif type == "linear":
        return value*-x*((1-delay_end)/delay_time)+1
    elif type == "logarithmic":
        return value*(2**(10*(x/delay_time-1)))

def create_sound(wave, volume):
    final_wave = wave * volume

    audio = np.column_stack((final_wave * 32767, final_wave * 32767)).astype(np.int16).copy()
    sound = pygame.sndarray.make_sound(audio)

    return sound

if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.plot(adsr_package(0.1, 0.2, 0.1, 0, create_wave('sine', 110, 1, [], 1)))
    plt.show()
