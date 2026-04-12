import pygame

size = sizex, sizey = 20, 20

SCREEN_SIZE = SCREENX, SCREENY = 640, 360

BG_COLOR = (10,10,20)

pygame.init()

# screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED | pygame.FULLSCREEN)
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)

logo = pygame.surface.Surface(size)

curtain = pygame.surface.Surface(SCREEN_SIZE)
curtain.fill((0,0,0))
curtain.set_alpha(10)

alpha = 10

trail = True

color = 6

colors = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),(255,255,255)]

logo_rect = logo.get_rect(topleft=(1, 0))

running = True

cs = 0

speeds = []
for i in range(1,10):
    speeds.append([i,i])

for i in range(10, 101, 10):
    speeds.append([i,i])

# print(speeds)

dir = speeds[0]

clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_EQUALS:
                cs += 1
                dir = speeds[(cs)%len(speeds)]
            elif event.key == pygame.K_MINUS:
                cs -= 1
                dir = speeds[(cs)%len(speeds)]
            elif event.key == pygame.K_t:
                trail = not trail
            elif event.key == pygame.K_0:
                alpha = (alpha-1)%50
                curtain.set_alpha(alpha)
                print(alpha)
            elif event.key == pygame.K_9:
                alpha = (alpha+1)%50
                curtain.set_alpha(alpha)
                print(alpha)
        if event.type == pygame.WINDOWSIZECHANGED:
            curtain = pygame.surface.Surface(screen.get_size())
            curtain.fill((0,0,0))
            curtain.set_alpha(alpha)


    logo_rect.move_ip((dir[0], dir[1]))

    if logo_rect.left < 0 or logo_rect.right > screen.get_width():
        for speed in speeds:
            speed[0] *= -1
        color = (color+1)%len(colors)
    if logo_rect.top < 0 or logo_rect.bottom > screen.get_height():
        for speed in speeds:
            speed[1] *= -1
        color = (color+1)%len(colors)

    if not trail:
        screen.fill((0,0,0))
    else:
        screen.blit(curtain, (0,0))

    logo.fill((0,0,0))

    pygame.draw.ellipse(logo, colors[color], (0,0, sizex,sizey))

    logo.set_colorkey((0,0,0))

    screen.blit(logo, logo_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()