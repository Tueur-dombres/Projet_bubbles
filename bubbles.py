import pygame as pg
from pygame.locals import *
from random import choice, randint
from math import sqrt, ceil

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
    global bubbles, spawn_bubbles, score, vies, tempo_bubbles, temps_restant, speed_modif
    bubbles = []
    spawn_bubbles = 0
    score = 0
    vies = 3
    tempo_bubbles = []
    temps_restant = 60*240
    speed_modif = 1
start()

button_restart_gameover = Rect(w/2-160, h/2+60, 128, 36)
button_menu_gameover = Rect(w/2+52, h/2+60, 90, 36)
button_start_menu = Rect(w/2-344/2, h/2-50, 344, 112)
button_credits_menu = Rect(w/2-370, h/2+200, 230, 60)
button_regles_menu = Rect(w/2+149, h/2+200, 212, 60)
button_retour_menu = Rect(w/2-143, h-100, 286, 48)
button_quitter_menu = Rect(40, 40, 180, 48)
class Circle:
    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
    
    def collidepoint(self, x, y, size = 0):
        if sqrt((self.x-x)**2+(self.y-y)**2) < (size if size else self.radius):
            return True
        else:
            return False
        
gamemode = "menu"
continuer = True    
while continuer:
    horloge.tick(240)
    for event in pg.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            continuer = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if gamemode == "play":
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
                if button_restart_gameover.collidepoint(x,y):
                    gamemode = "play"
                    start()
                elif button_menu_gameover.collidepoint(x,y):
                    gamemode = "menu"
            elif gamemode == "menu":
                if button_start_menu.collidepoint(x,y):
                    gamemode = "play"
                    start()
                elif button_credits_menu.collidepoint(x,y):
                    gamemode = "credits"
                elif button_regles_menu.collidepoint(x,y):
                    gamemode = "regles"
                elif button_quitter_menu.collidepoint(x,y):
                    continuer = False
            elif gamemode in ["credits","regles"]:
                if button_retour_menu.collidepoint(x,y):
                    gamemode = "menu"



    screen.fill(col["WHITE"])

    if gamemode == "play":
        spawn_bubbles += 1
        temps_restant -= 1
        speed_modif *= 1.00005
        #aggrandissement et comptage des bubbles
        colours_count = {i:[] for i in couleurs[1:]}
        for i in range(len(bubbles)):
            bubble = bubbles[i]
            bubble.radius += .05*speed_modif
            if bubble.colour != col["BLACK"]:
                colours_count[bubble.colour] += [i]

        #suppression des triplets
        suppr = []
        for i,e in colours_count.items():
            if len(e) >= 3:
                suppr += e
                score += 1

        tempo_bubbles += [[bubbles[i],0] for i in range(len(bubbles)) if i in suppr]
        bubbles = [bubbles[i] for i in range(len(bubbles)) if i not in suppr]
        bubbles = [bubble for bubble in bubbles if bubble.radius <= 100]

        #génération
        if spawn_bubbles >= 240/speed_modif:
            #choisir une position pas trop proche d'une autre bubble pour qu'elle ne puisse pas se toucher
            x,y = randint(100, w-100), randint(100, h-100) #une première positon aléatoire
            while sum(1 for bubble in bubbles if bubble.collidepoint(x,y,size=200))!=0: #s'il la position est trop proche d'une bubble
                x,y = randint(100, w-100), randint(100, h-100) #choix d'une nouvelle position aléatoire
            c = choice([couleur for couleur in couleurs[1:] if len(colours_count[couleur]) < 2]) #choix d'une couleur aléatoire parmis celle qui sont présentes une ou deux fois, pour ne pas faire gagner de point automatiquement
            bubbles += [Circle(x,y, 10, c)] #ajout de la nouvelle bubble à la liste
            spawn_bubbles = 0 #reset du timer
    
    if gamemode in ["play","gameover","transition_gameover"]:   
        suppr = []
        for i in range(len(tempo_bubbles)):
            bubble,size = tempo_bubbles[i][0],tempo_bubbles[i][1]
            pg.draw.circle(screen, bubble.colour, (bubble.x, bubble.y), bubble.radius)
            if bubble.colour == col["BLACK"]:
                pg.draw.polygon(screen, col["WHITE"], [(bubble.x,bubble.y-size),(bubble.x+size,bubble.y),(bubble.x,bubble.y+size),(bubble.x-size,bubble.y)])
            else:
                pg.draw.circle(screen, col["WHITE"], (bubble.x, bubble.y), size)
            tempo_bubbles[i][1]+=.5*speed_modif
            if tempo_bubbles[i][1] >= bubble.radius:
                suppr += [i]
        tempo_bubbles = [tempo_bubbles[i] for i in range(len(tempo_bubbles)) if i not in suppr]

        for bubble in bubbles :
            pg.draw.circle(screen, bubble.colour, (bubble.x, bubble.y), bubble.radius)
        
        text_temps_restant = font.render("temps restant : "+str(int(ceil(temps_restant/240))), 1, col["BLACK"])
        screen.blit(text_temps_restant, (965, 20))

        text_score = font.render("score : "+str(score), 1, col["BLACK"])
        screen.blit(text_score, (20, 20))

        text_vies = font.render("vies restantes : "+str(vies), 1, col["BLACK"])
        screen.blit(text_vies, (980, 60))

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
        screen.blit(text_record, (1000, 40))

        #affichage des boutton
        text_start = font_very_big.render("START", 1, col["WHITE"])
        screen.blit(text_start, (button_start_menu.x+10, button_start_menu.y+2))
        pg.draw.rect(screen, col["WHITE"], button_start_menu, width = 7)
        text_credits = font_big.render("CREDITS", 1, col["WHITE"])
        screen.blit(text_credits, (button_credits_menu.x+10, button_credits_menu.y+5))
        pg.draw.rect(screen, col["WHITE"], button_credits_menu, width = 4)
        text_regles = font_big.render("REGLES", 1, col["WHITE"])
        screen.blit(text_regles, (button_regles_menu.x+10, button_regles_menu.y+5))
        pg.draw.rect(screen, col["WHITE"], button_regles_menu, width = 4)
        text_quitter = font.render("QUITTER", 1, col["WHITE"])
        screen.blit(text_quitter, (button_quitter_menu.x+10, button_quitter_menu.y+5))
        pg.draw.rect(screen, col["WHITE"], button_quitter_menu, width = 4)
    
    elif gamemode in ["credits","regles"]:
        screen.fill(col["BLACK"])

        #affichage du bouton retour menu
        text_retour = font.render("RETOUR MENU", 1, col["WHITE"])
        screen.blit(text_retour, (button_retour_menu.x+10,button_retour_menu.y+5))
        pg.draw.rect(screen, col["WHITE"], button_retour_menu, width = 4)

        if gamemode == "credits":
            #titre
            text_titre_credits = font_big.render("Crédits", 1, col["WHITE"])
            screen.blit(text_titre_credits, (w/2-75, 100))

            #crédits
            texts_credits = ["Esteban Sabatier : développeur front-end et back-end",
                            "Alienor Librecht : vidéaste et Testeuse/QA",
                            "Charlotte Samama : écriture et management",
                            "Noelline Knapp-Dubois : scénariste et game designer"]
            
            for i in range(len(texts_credits)):
                screen.blit(font.render(texts_credits[i], 1, col["WHITE"]), (w/2-420, 300 + 45*i))

        elif gamemode == "regles":
            #titre
            text_titre_regles = font_big.render("Règles", 1, col["WHITE"])
            screen.blit(text_titre_regles, (w/2-80, 100))

            #règles
            texts_regles = ["Line 1",
                            "Line 2",
                            "Line 3",
                            "Line 4"]
            
            for i in range(len(texts_regles)):
                screen.blit(font.render(texts_regles[i], 1, col["WHITE"]), (w/2-420, 300 + 45*i))

    elif gamemode == "transition_gameover":
        compte_transition_gameover += 1
        pg.draw.rect(screen, col["BLACK"], Rect(w/2-compte_transition_gameover,h/2-compte_transition_gameover/2,compte_transition_gameover*2,compte_transition_gameover))
        if compte_transition_gameover == w_gameover/2:
            gamemode = "gameover"

    if (vies <= 0 or temps_restant <= 0) and gamemode == "play" and not tempo_bubbles: #si l'on a plus de vie, ou de temps
        gamemode = "transition_gameover"
        compte_transition_gameover = 0
        record = max(record, score+5*vies)

    pg.display.flip()