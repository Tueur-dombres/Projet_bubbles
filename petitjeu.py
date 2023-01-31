import pygame as pg
from pygame.locals import *


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
H = 400
L= 400
colour = [RED, BLUE, GREEN]

pg.init()
screen = pg.display.set_mode((L,H))
run = True
zone = pg.Rect((50, 50), (75, 75))
# je créé une surface bleue de la même taille que la zone
surf = pg.Surface(zone.size)
#renvoie la taille de la zone
surf.fill(BLUE)

compteur = 0

while run:
    for event in pg.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if zone.collidepoint(event.pos):
                    print("Touché")
                    compteur += 1
                    compteur = compteur%3
                    surf.fill(colour[compteur])
                print(event.pos)

    screen.fill (0)
    screen.blit(surf, zone)
    pg.display.flip()
pg.quit