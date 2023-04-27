import pygame as pg
from pygame.locals import *
from random import choice, randint
from math import sqrt, ceil

pg.init()

#initialisation de la fenêtre
size_screen = w, h = (1280,720)
w_gameover, h_gameover = 600,300
screen = pg.display.set_mode(size_screen)
horloge = pg.time.Clock()
record = 0

#listing des couleurs
col = {"BLACK":(0,0,0), "BLUE":(0,0,255), "RED":(255,0,0), "GREEN":(0,255,0), "MAGENTA":(255,0,255), "JAUNE":(255,255,0), "CYAN":(0,255,255), "WHITE":(255,255,255)}
couleurs = [*col.values()][:-1]

#préparation des polices d'écritures
font_very_big = pg.font.SysFont("arial", 100)
font_big = pg.font.SysFont("arial", 48)
font = pg.font.SysFont("arial", 36)
font_petit = pg.font.SysFont("arial", 24)

#initialisation tailles et positions des boutons
button_restart_gameover = Rect(w/2-160, h/2+60, 128, 36)
button_menu_gameover = Rect(w/2+52, h/2+60, 90, 36)
button_start_menu = Rect(w/2-344/2, h/2-50, 344, 112)
button_credits_menu = Rect(w/2-370, h/2+200, 230, 60)
button_regles_menu = Rect(w/2+149, h/2+200, 212, 60)
button_retour_menu = Rect(w/2-143, h-100, 286, 48)
button_quitter_menu = Rect(40, 40, 180, 48)

#fonction à appeler pour remettre les valeurs à 0
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

#création d'une classe Circle, qui fonctionne comme la classe Rect native de pygame 
class Circle:
    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
    
    #vérifier si un point appartient au cercle, éventuellement si un point est à une certaine distance avec le paramètre optionnel size
    def collidepoint(self, x, y, size = 0):
        if sqrt((self.x-x)**2+(self.y-y)**2) < (size if size else self.radius):
            return True
        else:
            return False

gamemode = "menu" #on commence au menu principal
continuer = True #initalisation de la boucle de jeu
while continuer:
    horloge.tick(240)
    for event in pg.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE: #pour quitter le jeu avec la touche échap, ou la croix
            continuer = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1: #click gauche
            x, y = event.pos #récupération de la position de la souris
            if gamemode == "play": #si le jeu es lancé
                suppr = []
                for i in range(len(bubbles)): #on parcours la liste des bubbles
                    bubble = bubbles[i]
                    if bubble.collidepoint(x,y): #si la bubble est cliquée
                        if bubble.colour == col["BLACK"]: #pour les noires
                            vies -= 1 #perte d'une vie
                            suppr += [i] #ajout à la liste des futures disparition
                        else: #pour les autres couleurs
                            bubble.colour = choice(couleurs) #changement de couleur 
                tempo_bubbles += [[bubbles[i],0] for i in range(len(bubbles)) if i in suppr] #le temps que la bulle fasse son animation de disparition
                bubbles = [bubbles[i] for i in range(len(bubbles)) if i not in suppr] #suppression des bubbles à supprimer dans la liste principale
            elif gamemode == "gameover": #dans le menu gameover
                if button_restart_gameover.collidepoint(x,y): #relancer le jeu
                    gamemode = "play"
                    start()
                elif button_menu_gameover.collidepoint(x,y): #retour au menu principal
                    gamemode = "menu"
            elif gamemode == "menu": #dans le menu principal
                if button_start_menu.collidepoint(x,y): #lancer le jeu
                    gamemode = "play"
                    start()
                elif button_credits_menu.collidepoint(x,y): #aller dans les crédits
                    gamemode = "credits"
                elif button_regles_menu.collidepoint(x,y): #aller dans les règles
                    gamemode = "regles"
                elif button_quitter_menu.collidepoint(x,y): #quitter le jeu avec le bouton quitter
                    continuer = False
            elif gamemode in ["credits","regles"]: #dans les crédits ou les règles
                if button_retour_menu.collidepoint(x,y): #retour au menu principal
                    gamemode = "menu"



    screen.fill(col["WHITE"]) #fond blanc

    if gamemode == "play": #si le jeu est lancé
        #gestion des timers pour l'apparition, le temp restant, et la vitesse de jeu
        spawn_bubbles += 1
        temps_restant -= 1
        speed_modif *= 1.00005 #la modification de vitesse d'apparition et de croissance varie de manière exponentielle entre 1 et 2 en 60sec

        #aggrandissement des bubbles et comptage des bubbles avec la création d'un dictionnaire qui classe les bubbles par couleur
        colours_count = {i:[] for i in couleurs[1:]} 
        for i in range(len(bubbles)):
            bubble = bubbles[i]
            bubble.radius += .05*speed_modif
            if bubble.colour != col["BLACK"]:
                colours_count[bubble.colour] += [i]

        #recherche des triplets de couleurs
        suppr = []
        for i,e in colours_count.items():
            if len(e) >= 3:
                suppr += e
                score += 1

        tempo_bubbles += [[bubbles[i],0] for i in range(len(bubbles)) if i in suppr] #le temps que la bulle fasse son animation de disparition
        bubbles = [bubbles[i] for i in range(len(bubbles)) if i not in suppr] #suppression des triplets
        bubbles = [bubble for bubble in bubbles if bubble.radius <= 100] #disparition des bubbles trop grande

        #génération
        if spawn_bubbles >= 240/speed_modif: #quand le compteur est assez grand, en fonction de la vitesse
            #choisir une position pas trop proche d'une autre bubble pour qu'elle ne puisse pas se toucher
            x,y = randint(100, w-100), randint(100, h-100) #une première positon aléatoire
            while sum(1 for bubble in bubbles if bubble.collidepoint(x,y,size=200))!=0: #s'il la position est trop proche d'une bubble
                x,y = randint(100, w-100), randint(100, h-100) #choix d'une nouvelle position aléatoire
            c = choice([couleur for couleur in couleurs[1:] if len(colours_count[couleur]) < 2]) #choix d'une couleur aléatoire parmis celle qui sont présentes une ou deux fois, pour ne pas faire gagner de point automatiquement
            bubbles += [Circle(x,y, 10, c)] #ajout de la nouvelle bubble à la liste
            spawn_bubbles = 0 #reset du timer
    
    if gamemode in ["play","gameover","transition_gameover"]: #pour les modes dans lesquels on doit afficher les bubbles

        #dessin des animations de disparition
        suppr = []
        for i in range(len(tempo_bubbles)):
            bubble,size = tempo_bubbles[i][0],tempo_bubbles[i][1]
            pg.draw.circle(screen, bubble.colour, (bubble.x, bubble.y), bubble.radius) #dessin de la bubble originale

            #on dessine l'intérieur de la bubble en blanc
            if bubble.colour == col["BLACK"]:
                pg.draw.polygon(screen, col["WHITE"], [(bubble.x,bubble.y-size),(bubble.x+size,bubble.y),(bubble.x,bubble.y+size),(bubble.x-size,bubble.y)]) #un losange pour les noires
            else:
                pg.draw.circle(screen, col["WHITE"], (bubble.x, bubble.y), size) #un cercle pour les autres couleurs

            tempo_bubbles[i][1]+=.5*speed_modif #agrandissement des formes intérieur en focntion de la vitesse
            if tempo_bubbles[i][1] >= bubble.radius: #recherche des bubbles dont la taille de la forme intérieure atteint la taille de la bubble originale
                suppr += [i]
        tempo_bubbles = [tempo_bubbles[i] for i in range(len(tempo_bubbles)) if i not in suppr] #suppression des bubbles à supprimer

        for bubble in bubbles :
            pg.draw.circle(screen, bubble.colour, (bubble.x, bubble.y), bubble.radius) #dessin des bubbles classiques
        
        #affichage du temps restant
        text_temps_restant = font.render("temps restant : "+str(int(ceil(temps_restant/240))), 1, col["BLACK"])
        screen.blit(text_temps_restant, (965, 20))

        #affichage du score
        text_score = font.render("score : "+str(score), 1, col["BLACK"])
        screen.blit(text_score, (20, 20))

        #affichage des vies restantes
        text_vies = font.render("vies restantes : "+str(vies), 1, col["BLACK"])
        screen.blit(text_vies, (980, 60))

    if gamemode == "transition_gameover": #durant l'apparition de la fenêtre de gameover
        compte_transition_gameover += 1 #timer
        pg.draw.rect(screen, col["BLACK"], Rect(w/2-compte_transition_gameover,h/2-compte_transition_gameover/2,compte_transition_gameover*2,compte_transition_gameover)) #dessin de la fenêtre en fontion avec une taille en fontion du timer
        if compte_transition_gameover == w_gameover/2: #quand la fenêtre à atteint sa taille
            gamemode = "gameover" #passage au menu gameover

    elif gamemode == "gameover": #dans le menu gameover
        #dessin de la fenêtre de gameover avec le titre
        pg.draw.rect(screen, col["BLACK"], Rect(w/2-w_gameover/2, h/2-h_gameover/2, w_gameover, h_gameover))
        text_gameover = font.render("GAMEOVER", 1, col["WHITE"])
        screen.blit(text_gameover, (w/2-105, h/2-h_gameover/2+50))

        #affichage des différentes lignes de calcul du score, centrées
        text_score_base = font_petit.render(f"Score = {score}", 1, col["WHITE"])
        screen.blit(text_score_base, (w/2-60,h/2-35))
        text_score_vies = font_petit.render(f"Vies restantes = {vies}", 1, col["WHITE"])
        screen.blit(text_score_vies, (w/2-105,h/2-10))
        text_score_total = font_petit.render(f"Score total = {score} + 5 x {vies} = {score+5*vies}", 1, col["WHITE"])
        screen.blit(text_score_total, (w/2-150,h/2+15))
        
        #affichage des boutons restart et retour au menu
        text_restart = font_petit.render("RESTART", 1, col["WHITE"])
        screen.blit(text_restart, (button_restart_gameover.x+10, button_restart_gameover.y+5))
        pg.draw.rect(screen, col["WHITE"], button_restart_gameover, width = 4)
        text_menu = font_petit.render("MENU", 1, col["WHITE"])
        screen.blit(text_menu, (button_menu_gameover.x+10, button_menu_gameover.y+5))
        pg.draw.rect(screen, col["WHITE"], button_menu_gameover, width = 4)

    elif gamemode == "menu":
        screen.fill(col["BLACK"]) #fond noir

        #titre
        text_menu = font_big.render("MENU PRINCIPAL", 1, col["WHITE"])
        screen.blit(text_menu, (w/2-205, 150))

        #affichage du record
        text_record = font.render(f"Record : {record}", 1, col["WHITE"])
        screen.blit(text_record, (1000, 40))

        #affichage des boutton start, crédits, règles, et quitter
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
    
    elif gamemode in ["credits","regles"]: #pour les crédits et les règles
        screen.fill(col["BLACK"]) #fond noir

        #affichage du bouton retour menu
        text_retour = font.render("RETOUR MENU", 1, col["WHITE"])
        screen.blit(text_retour, (button_retour_menu.x+10,button_retour_menu.y+5))
        pg.draw.rect(screen, col["WHITE"], button_retour_menu, width = 4)

        if gamemode == "credits": #pour les crédits
            #affichage du titre
            text_titre_credits = font_big.render("Crédits", 1, col["WHITE"])
            screen.blit(text_titre_credits, (w/2-75, 100))

            #affichage de texte des crédits
            texts_credits = ["Esteban Sabatier : développeur front-end et back-end",
                            "Alienor Libbrecht : vidéaste et Testeuse/QA",
                            "Charlotte Samama : écriture et management",
                            "Noelline Knapp--Dubois : scénariste et game designer"]
            
            for i in range(len(texts_credits)):
                screen.blit(font.render(texts_credits[i], 1, col["WHITE"]), (w/2-420, 300 + 45*i))

        elif gamemode == "regles":
            #affichage du titre
            text_titre_regles = font_big.render("Règles", 1, col["WHITE"])
            screen.blit(text_titre_regles, (w/2-80, 100))

            #affichage du texte des règles
            texts_regles = ["Votre objectif : obtenir le plus de point avant la fin de la partie.",
                            "Vous possédez 3 vies et 60 secondes, à vous d'en faire bon usage !",
                            "Lorsque vous cliquez sur une bulle, elle change de couleur.",
                            "Quand vous avez 3 bulles de la même couleur, vous gagnez un point.",
                            "Attention,  les bulles noires, sont des bombes qui font perdre une vie !",
                            "A la fin de la partie, 5 points bonus sont accordés par vie restante.",
                            "La partie s'arrête quand le délai est écoulé, ou que le joueur n'a plus de vies."]
            
            for i in range(len(texts_regles)):
                screen.blit(font.render(texts_regles[i], 1, col["WHITE"]), (w/2-610, 240 + 45*i))

    if (vies <= 0 or temps_restant <= 0) and gamemode == "play" and not tempo_bubbles: #si l'on a plus de vie, ou de temps
        gamemode = "transition_gameover" #on lance la transition
        compte_transition_gameover = 0 #reset du timer de transition
        record = max(record, score+5*vies) #actualisation du record

    pg.display.flip()