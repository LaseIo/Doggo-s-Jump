### GP Programmation
## Execution du jeu


# Importation de la bibliothèque time et début du chronomètre programme
import time
debut = time.time()
# Importation de la bibliothèque os
import os
# Obtenir le chemin absolu du répertoire actuel
current_directory = os.path.dirname(os.path.abspath(__file__))
# Importation de la physique du jeu
from Physique_du_jeu import x,y
# Importation des plateformes du jeu
from Plateformes_du_jeu import *

# Création de la fenêtre Tkinter
from tkinter import*
global root
root = Tk()
#définir la couleur de la fenêtre
root.configure(bg="sky blue") 
root.attributes('-fullscreen', True)
#root.minsize(1920,1080)

# Importation des contrôle de jeu
from Inputs_du_jeu import *
root.bind_all('<KeyPress>',press)
root.bind_all('<KeyRelease>',release)

# Définition des valeurs initiales pour y()
ty=0
xt=625
yt=0
obstacle_inf = 0
y0=0
# Apparitions des plateformes 
yc=0  
create_platform(yc)
print(game_platforms)
# Début de la boucle de jeu
while game_keys["space"]!=True:
    # Actualisation des coordonées
    xt=x(xt,6)
    yt,ty,dydt,obstacle_inf,y0=y(xt,yt,obstacle_inf,t=ty,y0=y0)
    # Affichage des coordonnées
    texte = xt,yt
    label = Label(root, text=texte, bg="sky blue")
    label.pack()
    # print(xt,round(yt,0),"",round(dydt,0),"t =",ty," obst =",obstacle_inf," y0 = ",round(y0,0),"readyness :",ready(obstacle_inf))
    # Placement du personnage
    mon_image = PhotoImage(file=os.path.join(current_directory, "images", "doggo_sprite.png"))
    personnage = Label(image=mon_image,bg="sky blue")
    personnage.image=mon_image
    personnage.place(x=xt,y=770-yt)
    # Actualisation de la page
    root.update()
    label.pack_forget()
    personnage.destroy()

# Fin de la boucle de jeu et fermeture de la page
root.destroy()
root.mainloop()

# Affiche le temps écoulé entre le début et la fin du programme
fin =time.time()
print(fin-debut)










