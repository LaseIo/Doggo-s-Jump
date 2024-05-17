### GP Programmation
## Plateformes du jeu

import tkinter as tk
from tkinter import*
from random import *
from os import *
from Physique_du_jeu import *
from Inputs_du_jeu import ready
# Obtenir le chemin absolu du répertoire actuel
current_directory = path.dirname(path.abspath(__file__))

pf_W = 300
pf_H = 65

# Création de la liste global des coordonnées de chaques plateformes générées
global game_platforms
game_platforms = []

def create_platform(character_y):
    # Coordonnées telles que la 1er plateforme est générée en bas de l'écran
    pf_y = character_y + 800 - pf_H
    pf_x = randint(0,1100)
    # Les plateformes sont générées de bas en haut jusqu'a atteindre le haut de l'écran + hauteurs du joueur
    while pf_y > character_y :
        # Permet de pouvoir faire apparaitre plusieurs plateformes sur la même coordonnées y
        for i in range(randint(1,3)):
            # pf_x_mem enregistre la coordonnée x de la plateforme précédente 
            pf_x_mem = pf_x
            # La coordonnée x de la plateforme est générée aléatoirement entre chaques cotées de l'écran
            pf_x = randint(0,1300-pf_W)                 
            if i > 1 :
                if pf_x < 550 :
                    pf_x = randint(550,1100)
                elif pf_x > 550 :
                    pf_x = randint(0,550)
            if pf_x_mem + 200 > pf_x > pf_x_mem - 200 :
                pf_y -= randint(150, 200) 
            else :
                pf_y -= randint(80, 200) 
            # Placement de la plateforme générée
            mon_image = PhotoImage(file=path.join(current_directory, "images", "platform_sprite.png"))
            platform = Label(image=mon_image,bg = "sky blue")
            platform.image=mon_image      
            platform.place(x=pf_x,y=pf_y)
            # Affichage des coordonnées
            #print(pf_x,pf_y)
            game_platforms.append((pf_x,pf_y))
        

def platform_inf(xc,yc,dydt,y0,obstacle_inf):
    if yc <= 0 and y0 == 0:
        new_y0 = 0
        obstacle_inf = 1
        return obstacle_inf,new_y0
    else :
        for i in game_platforms :
            if (dydt < 0 and i[1]-40<770-yc<i[1] and i[0]-30<xc<i[0]+270) or (y0 == i[1] and 1-ready(obstacle_inf) != 1 ):
                obstacle_inf = 1
                new_y0 = 770-i[1]
                return obstacle_inf,new_y0
            else :
                obstacle_inf = 0
                new_y0 = y0
        return obstacle_inf,new_y0






























