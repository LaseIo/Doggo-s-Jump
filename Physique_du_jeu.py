### GP programmation
## Physique du jeu

# Importation de la bibliothèque time et des touches du jeu
import time
from Inputs_du_jeu import game_keys,ready,dir
from Plateformes_du_jeu import platform_inf
# Définition de la fonction qui calcule la coordonnée x
def x(x,augmentx=1):
    if x < 0:
        augmentx = 0
        x = 0
    elif x > 1250 :
        augmentx = 0
        x = 1250
    x += dir()*augmentx
    return x

# Définition de la fonction qui calcule la coordonnée y
def y(x,y,obstacle_inf=0,obstacle_sup=0,t=0,y0=0,g=5):
    # Redéfinition de y et de sa dérivée
    y = ((-(3/4)*g*t**2)*(1-obstacle_inf)+35*g*t*(1-ready(obstacle_inf)))/7+y0+(1-obstacle_sup)*game_keys["Up"]*(1-ready(obstacle_inf))
    dydt = ((-(3/2)*g*t)+35*g)/7
    # Appèle la fct obstacle_inf
    obstacle_inf,y0 = platform_inf(x,y,dydt,y0,obstacle_inf)
    # Réactive la gravité s'il n'y a pas de sol ou s'il y a saut
    if obstacle_inf == 0 or game_keys["Up"]*ready(obstacle_inf) == 1 :
        time.sleep(1/60)
        t+=1
    else :
        t=0
    # Retourne la valeur de y et de t
    return y,t,dydt,obstacle_inf,y0















