import pygame
from pygame.locals import *
from random import *

size = w, h = (1280,720)
screen = pygame.display.set_mode(size)
horloge = pygame.time.Clock()

col = {"BLACK":(0,0,0), "BLUE":(0,0,255), "RED":(255,0,0), "GREEN":(0,255,0)}
WHITE = (255,255,255)
bubbles = []
spawn_bubbles = 0

continuer = True    
while continuer:
    horloge.tick(240)
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False
    screen.fill(WHITE)
    spawn_bubbles += 1
    suppr = []
    for i in range(len(bubbles)):
        bubble = bubbles[i]
        bubble["radius"] += .05
    bubbles = [bubble for bubble in bubbles if bubble["radius"] <= 100]


    if spawn_bubbles >= 240:
        bubbles += [{"x" : randint(100, w-100), "y" : randint(100, h-100), "radius" : 10, "colour" : choice(tuple(col.items()))}]
        spawn_bubbles = 0
    
    for bubble in bubbles :
        pygame.draw.circle(screen, bubble["colour"][1], (bubble["x"], bubble["y"]), bubble["radius"])
    pygame.display.flip()

    #sdfse
