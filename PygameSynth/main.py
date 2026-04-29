import pygame
import numpy as np
from sound_generator import create_wave, create_sound, adsr_package, create_exponential_sine_freq_decay
from pygame.locals import (
    K_q,
    K_2,
    K_w,
    K_3,
    K_e,
    K_r,
    K_5,
    K_t,
    K_6,
    K_y,
    K_7,
    K_u,
    K_i,
    K_9,
    K_o,
    K_0,
    K_p,

    K_z,
    K_s,
    K_x,
    K_d,
    K_c,
    K_f,
    K_v,
    K_b,
    K_h,
    K_n,
    K_j,
    K_m
)

"""
Eu usei ingles e portugues pra criar esse codigo.
Desculpe a inconsistencia.

Esse programa foi criado majoritariamente por JPB. Dito isso, faca oq quiser com ele (so nao me de os creditos se for fazer merda).
"""

TROMPETE = [0.9, 0.8, 0.75, 0.6, 0.5, 0.4, 0.25, 0.1]
NAN = []
CUSTOMIZADO = [0.8, 0.6, 0.45, 0.35, 0.3]
VIOLAO = [1.2, 0.9, 0.7, 0.5, 0.3, 0.1]
TUDO1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
IA = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
TIRO = [1, 0.8, 0.6, 0.4, 0.2, 0.1]


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("sintetizador")

keys = [
    K_q,
    K_2,
    K_w,
    K_3,
    K_e,
    K_r,
    K_5,
    K_t,
    K_6,
    K_y,
    K_7,
    K_u,
    K_i,
    K_9,
    K_o,
    K_0,
    K_p,

    K_z,
    K_s,
    K_x,
    K_d,
    K_c,
    K_f,
    K_v,
    K_b,
    K_h,
    K_n,
    K_j,
    K_m
]

notes = [32.7*((2**(1/12))**n) for n in range(84)]
notes_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

oitava = 2

harmonicos = TIRO # declara o volume de cada harmonico comecando pela oitava. O tamanho da array determina a quantidade de harmonicos (pode ser alterado para mais ou para menos)

tipo_de_onda = "triangle" # tipos: 'sine'(seno), 'square'(quadrado), 'sawtooth'(dente de serra), 'triangle'(triangulo)

notas_fonte = pygame.font.SysFont('comicsans', 50)

font = pygame.font.SysFont('comicsans', 15)

screen.blit(notas_fonte.render("ESPERE, GERANDO NOTAS", True, (255,255,255)), (720//2-10, 60))
screen.blit(font.render("isso pode demorar um pouco...", True, (255,255,255)), (720//2+10, 120))

pygame.display.flip()

notas_ondas = [adsr_package(0.1, 0.2, 0.5, 0,create_wave(tipo_de_onda, note, 1, harmonicos)) for note in notes]

running = True

waves = {}

texts = []

colors = [(255, g, 0) for g in range(0, 255, 255//(len(notes)//4))] + [(r, 255, 0) for r in range(255, 0, -255//(len(notes)//4))] + [(0,255,b) for b in range(0, 255, 255//(len(notes)//4))] + [(0, g, 255) for g in range(255, 0, -255//(len(notes)//4))]

tutorial = font.render("notas : teclas q, 2, w, 3, e, r, 5, t, 6, y, 7, u, i, 9, o, 0, p, z, s, x, d, c, f, v, b, h, n, j, m | prairapara a proxima oitava aperte ' ou / para voltar a anterior", True, (255,255,255))

for i in range(len(notes)):
    text = notas_fonte.render(f"{notes_names[i%len(notes_names)]}{i//12+1}", True, colors[i])
    texts.append(text)

notas = {keys[i]:notas_ondas[i+12*oitava] for i in range(len(keys))}

notas_textos = {texts[i+12*oitava]:keys[i] for i in range(len(keys))}

last_key = len(keys)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.FULLSCREEN:
            pygame.display.toggle_fullscreen()
        
        if event.type == pygame.KEYDOWN:
            if event.key in keys[:last_key]:
                waves[event.key] = create_sound(notas[event.key], 1)
                waves[event.key].play()
    
            if event.key == pygame.K_QUOTE and oitava < 5:
                oitava += 1
                if oitava >= 5:
                    last_key = len(keys)-5
                notas = {keys[i]:notas_ondas[i+12*oitava] for i in range(last_key)}
                notas_textos = {texts[i+12*oitava]:keys[i] for i in range(last_key)}
            if event.key == pygame.K_SLASH and oitava > 0:
                oitava -= 1
                last_key = len(keys)
                notas = {keys[i]:notas_ondas[i+12*oitava] for i in range(len(keys))}
                notas_textos = {texts[i+12*oitava]:keys[i] for i in range(len(keys))}
    
        if event.type == pygame.KEYUP and event.key in keys[:last_key]:
            waves[event.key].fadeout(100)
            del waves[event.key]

    screen.fill((0,0,0))

    if len(waves) > 0:
        final_wave = 0
    
        for key in waves.keys():
            final_wave += notas[key]
    
        if max(final_wave) > 1:
            compressor = 1/max(final_wave)
            final_wave *= compressor
        else:
            compressor = 1

        points_list = []

        for value in range(5000,6200):
            points_list.append((value-4950, -round(100*final_wave[value], 0)+720//14*10))

        pygame.draw.line(screen, (50,50,50), (0, 720//14*10), (1280, 720//14*10))

        for i in range(len(points_list)-1):
            pygame.draw.line(screen, (255,255,255), points_list[i], points_list[i+1])
    
        for wave in waves.values():
            wave.set_volume(compressor)

    pressed_keys = pygame.key.get_pressed()

    for y in range(7):
        if 6-oitava == y:
            # pygame.draw.rect(screen, (255,255,255), (0, 720//14*y+5, 1280//25, 720//28))
            pygame.draw.polygon(screen, (255,255,255), [(0,(720//14*y)-(720//28)+30), (0,(720//14*(y+1))-(720//28)+30), (30, (720//28*(2*y+1))-(720//28)+30)])
        for x in range(12):
            if x+(y*12) >= len(texts):
                break
        
            elif texts[x-((1+y)*12)] in notas_textos:
                key = notas_textos[texts[x-((1+y)*12)]]
                if key and pressed_keys[key]:
                    pygame.draw.rect(screen, (255, 255, 255), ((1280//12)*x-(1280//12-5)//2+70, ((720//14)*y)-(720//14)//2+30, 1280//12-5, 720//14))
        
            screen.blit(texts[x-((1+y)*12)], texts[x-((1+y)*12)].get_rect(center = ((1280//12)*x+70, (720//14)*y+30)))

    screen.blit(tutorial, (10, 690))

    pygame.display.flip()
