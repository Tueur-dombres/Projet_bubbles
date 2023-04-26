import pygame as pg
from pygame.locals import *
from random import choice, randint
from math import sqrt


pg.init()

size_screen = w, h = (1280,720)
w_gameover, h_gameover = 600,300
screen = pg.display.set_mode(size_screen)
horloge = pg.time.Clock()
col = {"BLACK":(0,0,0), "BLUE":(0,0,255), "RED":(255,0,0), "GREEN":(0,255,0), "MAGENTA":(255,0,255), "JAUNE":(255,255,0), "CYAN":(0,255,255), "WHITE":(255,255,255)}
couleurs = [*col.values()][:-1]
font_very_big = pg.font.SysFont("arial", 100)
font_big = pg.font.SysFont("arial", 48)
font = pg.font.SysFont("arial", 36)
font_petit = pg.font.SysFont("arial", 24)
record = 0

def start():
    global bubbles, spawn_bubbles, score, vies, tempo_bubbles
    bubbles = []
    spawn_bubbles = 0
    score = 0
    vies = 3
    tempo_bubbles = []
start()

button_restart_gameover = Rect(w/2-170, h/2+60, 128, 36)
button_menu_gameover = Rect(w/2+60, h/2+60, 90, 36)
button_start_menu = Rect(w/2-344/2, h/2-50, 344, 112)
button_credits_menu = Rect(w/2-314, h/2+200, 174, 60)
button_regle_menu = Rect(w/2+140, h/2+200, 170, 60)
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
        
gamemode = "gameover"
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
            if gamemode == "play":
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
                    tempo_bubbles += [[bubbles[i],0] for i in range(len(bubbles)) if i in suppr]
                    bubbles = [bubbles[i] for i in range(len(bubbles)) if i not in suppr]
            elif gamemode == "gameover":
                if event.button == 1:
                    if button_restart_gameover.collidepoint(x,y):
                        gamemode = "play"
                        start()
                    elif button_menu_gameover.collidepoint(x,y):
                        gamemode = "menu"
            elif gamemode == "menu":
                if event.button == 1:
                    if button_start_menu.collidepoint(x,y):
                        gamemode = "play"
                        start()



    screen.fill(col["WHITE"])

    if gamemode == "play":
        spawn_bubbles += 1
        colours_count = {i:[] for i in couleurs[1:]}

        for i in range(len(bubbles)):
            bubble = bubbles[i]
            bubble.radius += .05
            if bubble.colour != col["BLACK"]:
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

        if spawn_bubbles >= 240:
            bubbles += [Circle(randint(100, w-100), randint(100, h-100), 10, choice(couleurs))]
            spawn_bubbles = 0
    
    if gamemode in ["play","gameover"]:   
        suppr = []
        for i in range(len(tempo_bubbles)):
            bubble,size = tempo_bubbles[i][0],tempo_bubbles[i][1]
            pg.draw.circle(screen, bubble.colour, (bubble.x, bubble.y), bubble.radius)
            if bubble.colour == col["BLACK"]:
                pg.draw.polygon(screen, col["WHITE"], [(bubble.x,bubble.y-size),(bubble.x+size,bubble.y),(bubble.x,bubble.y+size),(bubble.x-size,bubble.y)])
            else:
                pg.draw.circle(screen, col["WHITE"], (bubble.x, bubble.y), size)
            tempo_bubbles[i][1]+=.5
            if tempo_bubbles[i][1] == round(bubble.radius,0):
                suppr += [i]
        tempo_bubbles = [tempo_bubbles[i] for i in range(len(tempo_bubbles)) if i not in suppr]

        for bubble in bubbles :
            pg.draw.circle(screen, bubble.colour, (bubble.x, bubble.y), bubble.radius)

        text_score = font.render("score : "+str(score), 1, col["BLACK"])
        screen.blit(text_score, (20, 20))

        text_vies = font.render("vies restantes : "+str(vies), 1, col["BLACK"])
        screen.blit(text_vies, (980, 20))

    if gamemode == "gameover":
        pg.draw.rect(screen, col["BLACK"], Rect(w/2-w_gameover/2, h/2-h_gameover/2, w_gameover, h_gameover))
        text_gameover = font.render("GAMEOVER", 1, col["WHITE"])
        screen.blit(text_gameover, (w/2-105, h/2-h_gameover/2+50))

        #affichage du score
        text_score_base = font_petit.render(f"Score = {score}", 1, col["WHITE"])
        screen.blit(text_score_base, (w/2-60,h/2-35))
        text_score_vies = font_petit.render(f"Vies restantes = {vies}", 1, col["WHITE"])
        screen.blit(text_score_vies, (w/2-105,h/2-10))
        text_score_total = font_petit.render(f"Score total = {score} + 5 x {vies} = {score+5*vies}", 1, col["WHITE"])
        screen.blit(text_score_total, (w/2-150,h/2+15))
        
        #affichage des boutons
        text_restart = font_petit.render("RESTART", 1, col["WHITE"])
        screen.blit(text_restart, (button_restart_gameover.x+10, button_restart_gameover.y+5))
        pg.draw.rect(screen, col["WHITE"], button_restart_gameover, width = 4)
        text_menu = font_petit.render("MENU", 1, col["WHITE"])
        screen.blit(text_menu, (button_menu_gameover.x+10, button_menu_gameover.y+5))
        pg.draw.rect(screen, col["WHITE"], button_menu_gameover, width = 4)

    elif gamemode == "menu":
        screen.fill(col["BLACK"])
        text_menu = font_big.render("MENU PRINCIPAL", 1, col["WHITE"])
        screen.blit(text_menu, (w/2-205, 150))

        #affichage du record
        text_record = font.render(f"Record : {record}", 1, col["WHITE"])
        screen.blit(text_record, (1000, 80))

        #affichage des boutton
        text_start = font_very_big.render("START", 1, col["WHITE"])
        screen.blit(text_start, (button_start_menu.x+10, button_start_menu.y+5))
        pg.draw.rect(screen, col["WHITE"], button_start_menu, width = 4)
        text_credits = font_big.render("Crédits", 1, col["WHITE"])
        screen.blit(text_credits, (button_credits_menu.x+10, button_credits_menu.y+5))
        pg.draw.rect(screen, col["WHITE"], button_credits_menu, width = 4)
        text_regles = font_big.render("Règles", 1, col["WHITE"])
        screen.blit(text_regles, (button_regle_menu.x+10, button_regle_menu.y+5))
        pg.draw.rect(screen, col["WHITE"], button_regle_menu, width = 4)
        
    if vies <= 0 and gamemode == "play": #si l'on a perdu
        gamemode = "gameover"
        record = max(record, score+5*vies)

    pg.display.flip()
