import pygame as pg
from pygame.locals import *
from random import choice, randint
from math import sqrt


pg.init()

size_screen = w, h = (1280,720)
screen = pg.display.set_mode(size_screen)
horloge = pg.time.Clock()
col = {"BLACK":(0,0,0), "BLUE":(0,0,255), "RED":(255,0,0), "GREEN":(0,255,0), "MAGENTA":(255,0,255), "JAUNE":(255,255,0), "CYAN":(0,255,255), "WHITE":(255,255,255)}
couleurs = [*col.values()][:-1]
print(couleurs)
font = pg.font.SysFont("arial", 36)

bubbles = []
spawn_bubbles = 0
score = 0
vies = 3
tempo_bubbles = []
class Circle:
    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
    
    def collidepoint(self, x, y):
        if sqrt((bubble.x-x)**2+(bubble.y-y)**2) < bubble.radius:
            return True
        else:
            return False

continuer = True    
while continuer:
    horloge.tick(240)
    for event in pg.event.get():
        if event.type == QUIT:
            continuer = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = False
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if event.button == 1:
                suppr = []
                for i in range(len(bubbles)):
                    bubble = bubbles[i]
                    if bubble.collidepoint(x,y):
                        if bubble.colour == col["BLACK"]:
                            vies -= 1
                            suppr += [i]
                        else:
                            bubble.colour = choice(couleurs)
                bubbles = [bubbles[i] for i in range(len(bubbles)) if i not in suppr]
                
                        


    screen.fill(col["WHITE"])
    spawn_bubbles += 1

    colours_count = {i:[] for i in couleurs}

    for i in range(len(bubbles)):
        bubble = bubbles[i]
        bubble.radius += .05
        colours_count[bubble.colour] += [i]

    suppr = []
    for i,e in colours_count.items():
        if len(e) >= 3:
            suppr += e
            score += 1
            print(score)

    tempo_bubbles += [[bubbles[i],0] for i in range(len(bubbles)) if i in suppr]
    bubbles = [bubbles[i] for i in range(len(bubbles)) if i not in suppr]
    bubbles = [bubble for bubble in bubbles if bubble.radius <= 100]

    text_score = font.render(str(score), 1, col["BLACK"])
    screen.blit(text_score, (20, 20))

    text_vies = font.render(str(vies), 1, col["BLACK"])
    screen.blit(text_vies, (1200, 20))

    if spawn_bubbles >= 240:
        bubbles += [Circle(randint(100, w-100), randint(100, h-100), 10, choice(couleurs))]
        spawn_bubbles = 0
    
    for bubble in bubbles :
        pg.draw.circle(screen, bubble.colour, (bubble.x, bubble.y), bubble.radius)
    
    suppr = []
    for i in range(len(tempo_bubbles)):
        bubble,size = tempo_bubbles[i][0],tempo_bubbles[i][1]
        pg.draw.circle(screen, bubble.colour, (bubble.x, bubble.y), bubble.radius)
        pg.draw.circle(screen, col["WHITE"], (bubble.x, bubble.y), size)
        tempo_bubbles[i][1]+=.5
        if tempo_bubbles[i][1] == round(bubble.radius,0):
            suppr += [i]
    tempo_bubbles = [tempo_bubbles[i] for i in range(len(tempo_bubbles)) if i not in suppr]

    pg.display.flip()
