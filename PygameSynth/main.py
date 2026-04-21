import pygame
from pygame.locals import (
    K_a,
    K_w,
    K_s,
    K_e,
    K_d,
    K_f,
    K_t,
    K_g,
    K_y,
    K_h,
    K_u,
    K_j,
    K_k,
    K_o,
    K_l,
    K_p,
    K_SEMICOLON
)
from sound_generator import create_wave, create_sound

"""
Eu usei ingles e portugues pra criar esse codigo.
Desculpe a inconsistencia.

Esse programa foi criado majoritariamente por JPB. Dito isso, faca oq quiser com ele (so nao me de os creditos se for fazer merda).
"""

TROMPETE = [0.9, 0.8, 0.75, 0.6, 0.5, 0.4, 0.25, 0.1]
BASE = []
CUSTOMIZADO = [0.8, 0.6, 0.45, 0.35, 0.3]

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("sintetizador")

keys = [
    K_a,
    K_w,
    K_s,
    K_e,
    K_d,
    K_f,
    K_t,
    K_g,
    K_y,
    K_h,
    K_u,
    K_j,
    K_k,
    K_o,
    K_l,
    K_p,
    K_SEMICOLON
]

notes = [32.7*((2**(1/12))**n) for n in range(96)]
notes_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

oitava = 2

harmonicos = TROMPETE # declara o volume de cada harmonico comecando pela oitava. O tamanho da array determina a quantidade de harmonicos (pode ser alterado para mais ou para menos)

tipo_de_onda = "sine" # tipos: 'sine'(seno), 'square'(quadrado), 'sawtooth'(dente de serra)

font = pygame.font.Font(None, 30)

running = True

waves = {}

texts = []

colors = [[-abs(x)+255,-abs(x-255)+255,-abs(x-(2*255))+255] for x in range(0, 255*2,255*2//len(notes))]

tutorial = font.render("notas : teclas a, w, s, e, d, f, t, g, y, h, u, j, k, o, l, p | prairapara a proxima oitava aperte ' ou / para voltar a anterior", True, (255,255,255))

for i in range(len(colors)):
    for j in range(3):
        if colors[i][j] < 0:
            colors[i][j] = 0

for i in range(len(notes)):
    text = font.render(f"{notes_names[i%len(notes_names)]}{i//12+1}", True, colors[i])
    texts.append(text)

notas = {keys[i]:create_wave(tipo_de_onda, notes[i+12*oitava], 0.5, harmonicos) for i in range(len(keys))}

notas_textos = {texts[i+12*oitava]:keys[i] for i in range(len(keys))}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in keys:
                waves[event.key] = create_sound(notas[event.key], 1)
                waves[event.key].play()
            if event.key == pygame.K_QUOTE and oitava < 6:
                oitava += 1
                notas = {keys[i]:create_wave(tipo_de_onda,notes[i+12*oitava], 0.5, harmonicos) for i in range(len(keys))}
                notas_textos = {texts[i+12*oitava]:keys[i] for i in range(len(keys))}
            if event.key == pygame.K_SLASH and oitava > 0:
                oitava -= 1
                notas = {keys[i]:create_wave(tipo_de_onda,notes[i+12*oitava], 0.5, harmonicos) for i in range(len(keys))}
                notas_textos = {texts[i+12*oitava]:keys[i] for i in range(len(keys))}
        if event.type == pygame.KEYUP and event.key in keys:
            waves[event.key].fadeout(100)
            del waves[event.key]
    
    screen.fill((0,0,0))

    if len(waves) > 0:
        final_wave = 0
        
        for key in waves.keys():
            final_wave += notas[key]
        
        compressor = 1/max(final_wave)
        final_wave *= compressor

        points_list = []

        for value in range(0,1200):
            points_list.append((value+50, -round(100*final_wave[value], 0)+720//14*10))
        
        for i in range(len(points_list)-1):
            pygame.draw.line(screen, (255,255,255), points_list[i], points_list[i+1])
        
        for wave in waves.values():
            wave.set_volume(compressor)
    
    pressed_keys = pygame.key.get_pressed()

    for y in range(7):
        if oitava == y:
            # pygame.draw.rect(screen, (255,255,255), (0, 720//14*y+5, 1280//25, 720//28))
            pygame.draw.polygon(screen, (255,255,255), [(0,720//14*y+5), (0,720//14*(y+1)+5), (1280//25-5, (720//14*(y)+16))])
        for x in range(12):
            if x+(y*12) >= len(texts):
                break
            
            elif 0 <= x+(y*12)-12*oitava < len(notas_textos) and x+(y*12) < len(texts):
                key = notas_textos.get(texts[x+(y*12)])
                if key and pressed_keys[key]:
                    pygame.draw.rect(screen, (255, 255, 255), (1280//12*x+45, 720//14*y+5, 1280//12, 720//14))
            
            screen.blit(texts[x+(y*12)], (1280//12*x+50, 720//14*y+10))

    screen.blit(tutorial, (10, 690))

    pygame.display.flip()