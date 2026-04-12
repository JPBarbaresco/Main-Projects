import pygame
import random
import math

FONTE = 65
DISSIPACAO = 2
VARIACAO_FONTE = -0

def catenaria(x):
    return int(VARIACAO_FONTE*math.cosh((x-32)/VARIACAO_FONTE)+FONTE-VARIACAO_FONTE)

def parabola(a, x, xv : list[int], yv : list[int]):
    if len(xv) > 1 and len(yv) == len(xv):
        for i in range(len(xv)):
            resoult = int(a*((x-xv[i])**2) + yv[i])
            if resoult >= 0:
                return resoult
        return 0
    elif len(yv) != len(xv):
        for i in range(len(xv)):
            resoult = int(a*((x-xv[i])**2) + yv[0])
            if resoult >= 0:
                return resoult
        return 0
    else:
        return int(a*((x-xv[0])**2) + yv[0])
    
pygame.init()

screen = pygame.display.set_mode((640, 360), pygame.SCALED | pygame.FULLSCREEN)

fogo = [[0 for _ in range(640//5)] for _ in range(360//5+1)] + [[parabola(VARIACAO_FONTE, i, [32], [100]) for i in range(640//5)]]

colors = [(r, 0, 0) for r in range(0, 250, 10)] +  [(250, g, 0) for g in range(0, 200, 10)] + [(250, 200, b) for b in range(0, 200, 10)]
print(len(colors))

running = True
frames = 0

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill((0,0,0))

    for y in range(len(fogo)-1):
        for x in range(len(fogo[y])):
            dissipacao_atual = random.randint(1, DISSIPACAO)
            
            fogo[y][x - int(dissipacao_atual*-1)%len(fogo[y])] = fogo[y+1][x] - dissipacao_atual
            

            if fogo[y][x] < 0:
                fogo[y][x] = 0
            elif fogo[y][x] >= len(colors):
                fogo[y][x] = len(colors) - 1
            
            pygame.draw.rect(screen, colors[fogo[y][x]], (5*x, 5*y, 5, 5))
    
    pygame.display.flip()

    clock.tick(10)

    frames += 1