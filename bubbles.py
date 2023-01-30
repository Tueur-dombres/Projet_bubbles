import pygame as pg
from pygame.locals import *
from random import *

size_screen = w, h = (1280,720)
screen = pg.display.set_mode(size_screen)
horloge = pg.time.Clock()
col = {"BLACK":(0,0,0), "BLUE":(0,0,255), "RED":(255,0,0), "GREEN":(0,255,0), "WHITE":(255,255,255)}
couleurs = [col["BLACK"], col["BLUE"], col["RED"], col["GREEN"]]
bubbles = []
spawn_bubbles = 0

continuer = True    
while continuer:
    horloge.tick(240)
    for event in pg.event.get():
        if event.type == QUIT:
            continuer = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False

    screen.fill(col["WHITE"])
    spawn_bubbles += 1

    colours_count = {i:[] for i in couleurs}

    for i in range(len(bubbles)):
        bubble = bubbles[i]
        bubble["radius"] += .05
        colours_count[bubble["colour"]] += [i]

    suppr = []
    for i,e in colours_count.items():
        if len(e) >= 3:
            suppr += e

    bubbles = [bubbles[i] for i in range(len(bubbles)) if i not in suppr]
    bubbles = [bubble for bubble in bubbles if bubble["radius"] <= 100]


    if spawn_bubbles >= 240:
        bubbles += [{"x" : randint(100, w-100), "y" : randint(100, h-100), "radius" : 10, "colour" : choice(couleurs)}]
        spawn_bubbles = 0
    
    for bubble in bubbles :
        pg.draw.circle(screen, bubble["colour"], (bubble["x"], bubble["y"]), bubble["radius"])
    pg.display.flip()
