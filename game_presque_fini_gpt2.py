from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
import csv
import os
import time
from random import randint

# Nom du fichier CSV
FILENAME = r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\scores.csv"

def gameplay():
    # Importation des touches du jeu
    global game_keys
    game_keys = {"space": 0, "Left": 0, "Right": 0, "Up": 0}

    # Obtenir le chemin absolu du répertoire actuel
    current_directory = os.path.dirname(os.path.abspath(__file__))

    pf_W = 300
    pf_H = 65

    # Création de la liste global des coordonnées de chaque plateforme générée
    global game_platforms
    game_platforms = []

    # Définition de la fonction "touche appuyée"
    def press(event):
        if event.keysym in game_keys.keys():
            game_keys[event.keysym] = 1

    # Définition de la fonction "touche relâchée"
    def release(event):
        if event.keysym in game_keys.keys():
            game_keys[event.keysym] = 0

    # Définition de la fonction qui donne la direction à x         
    def dir():
        if game_keys["Right"] == 1:
            return 1
        elif game_keys["Left"] == 1:
            return -1
        else:
            return 0

    def ready(obstacle_inf=0):
        if obstacle_inf == 1 and game_keys["Up"] == 0:
            return 1
        else:
            return 0

    # Définition de la fonction qui calcule la coordonnée x
    def x(x, augmentx=1):
        if x < 0:
            augmentx = 0
            x = 0
        elif x > 1250:
            augmentx = 0
            x = 1250
        x += dir() * augmentx
        return x

    # Définition de la fonction qui calcule la coordonnée y
    def y(x, y, obstacle_inf=0, obstacle_sup=0, t=0, y0=0, g=5):
        # Redéfinition de y et de sa dérivée
        y = ((-(3/4) * g * t**2) * (1 - obstacle_inf) + 35 * g * t * (1 - ready(obstacle_inf))) / 7 + y0 + (1 - obstacle_sup) * game_keys["Up"] * (1 - ready(obstacle_inf))
        dydt = ((-(3/2) * g * t) + 35 * g) / 7
        # Appel de la fonction obstacle_inf
        obstacle_inf, y0 = platform_inf(x, y, dydt, y0, obstacle_inf)
        # Réactive la gravité s'il n'y a pas de sol ou s'il y a saut
        if obstacle_inf == 0 or game_keys["Up"] * ready(obstacle_inf) == 1:
            time.sleep(1/240)
            t += 1
        else:
            t = 0
        # Retourne la valeur de y et de t
        return y, t, dydt, obstacle_inf, y0

    def create_platform(character_y):
        # Coordonnées telles que la 1ère plateforme est générée en bas de l'écran
        pf_y = character_y + 800 - pf_H
        pf_x = randint(0, 1100)
        # Les plateformes sont générées de bas en haut jusqu'à atteindre le haut de l'écran + hauteurs du joueur
        while pf_y > character_y:
            # Permet de pouvoir faire apparaître plusieurs plateformes sur la même coordonnée y
            for i in range(randint(1, 3)):
                # pf_x_mem enregistre la coordonnée x de la plateforme précédente 
                pf_x_mem = pf_x
                # La coordonnée x de la plateforme est générée aléatoirement entre chaque côté de l'écran
                pf_x = randint(0, 1300 - pf_W)
                if i > 1:
                    if pf_x < 550:
                        pf_x = randint(550, 1100)
                    elif pf_x > 550:
                        pf_x = randint(0, 550)
                if pf_x_mem + 200 > pf_x > pf_x_mem - 200:
                    pf_y -= randint(150, 200)
                else:
                    pf_y -= randint(80, 200)
                game_platforms.append((pf_x, pf_y))

    def platform_inf(xc, yc, dydt, y0, obstacle_inf):
        if yc <= 0 and y0 == 0:
            new_y0 = 0
            obstacle_inf = 1
            return obstacle_inf, new_y0
        else:
            for i in game_platforms:
                if (dydt < 0 and i[1] - 40 < 500 - yc < i[1] and i[0] - 30 < xc < i[0] + 270) or (y0 == i[1] and 1 - ready(obstacle_inf) != 1):
                    obstacle_inf = 1
                    new_y0 = 500 - i[1]
                    return obstacle_inf, new_y0
                else:
                    obstacle_inf = 0
                    new_y0 = y0
            return obstacle_inf, new_y0

    # Création de la liste globale des plateformes affichées
    global platform_showed
    platform_showed = []

    def platform_destroy(yc, platform_showed):
        for i in range(len(game_platforms)):
            if game_platforms[i][1] > 900 - yc:
                game_platforms.pop(i)
                platform_showed.pop(len(game_platforms) - i)
                new_platform()
                break

    def new_platform():
        # pf_x_mem enregistre la coordonnée x de la dernière plateforme générée
        pf_x_mem = game_platforms[-1][0]
        # Coordonnées telles que la nouvelle plateforme est générée au-dessus de la dernière plateforme de la liste game_platforms
        pf_y = game_platforms[-1][1] - randint(0, 120)
        # La coordonnée x de la nouvelle plateforme est générée en fonction de la coordonnée x de la dernière plateforme générée
        if 0 > pf_x_mem > 333:
            pf_x = randint(0, 750)
        elif 333 > pf_x_mem > 667:
            pf_x = randint(0, 1000)
        else:
            pf_x = randint(250, 1000)
        # La hauteur de la nouvelle plateforme est plus élevée si elle est générée au-dessus de la dernière plateforme
        if pf_x_mem + 200 > pf_x > pf_x_mem - 200:
            pf_y -= randint(140, 180)
        else:
            pf_y -= randint(80, 180)
        game_platforms.append((pf_x, pf_y))

    # Début de l'exécution du jeu
    debut = time.time()

    # Création de la fenêtre Tkinter
    global root
    root = Tk()
    root.configure(bg="sky blue") 
    root.attributes('-fullscreen', True)
    root.bind_all('<KeyPress>', press)
    root.bind_all('<KeyRelease>', release)

    # Définition des valeurs initiales pour y()
    ty = 0
    xt = 625
    yt = 0
    obstacle_inf = 0
    y0 = 0
    # Apparitions des plateformes 
    yc = 0  
    create_platform(yc)
    print(game_platforms)

    # Début de la boucle de jeu
    while game_keys["space"] != True:
        # Actualisation des coordonnées
        xt = x(xt, 10)
        yt, ty, dydt, obstacle_inf, y0 = y(xt, yt, obstacle_inf, t=ty, y0=y0)
        # Affichage des coordonnées
        texte = xt, yt
        label = Label(root, text=texte, bg="sky blue")
        label.pack()
        # print(xt, round(yt, 0), "", round(dydt, 0), "t =", ty, " obst =", obstacle_inf, " y0 =", round(y0, 0), "readyness :", ready(obstacle_inf))
        # Placement du personnage
        mon_image = PhotoImage(file=os.path.join(current_directory, r"Z:\perso\Code\Pf_Jump.png"))
        w = Label(root, image=mon_image, bd=0)
        w.image = mon_image
        w.place(x=xt, y=500 - yt)
        # Affichage des plateformes
        for i in range(len(game_platforms)):
            platform_image = PhotoImage(file=os.path.join(current_directory, r"Z:\perso\Code\platform.png"))
            pf = Label(root, image=platform_image, bd=0)
            pf.image = platform_image
            pf.place(x=game_platforms[i][0], y=500 - game_platforms[i][1])
            if len(platform_showed) < len(game_platforms):
                platform_showed.append(pf)
        # Destruction des plateformes en dessous de la fenêtre d'affichage
        platform_destroy(yt, platform_showed)
        root.update()
        time.sleep(1/60)

    # Fin de la boucle de jeu
    root.quit()
    root.destroy()

    # Affichage du temps de jeu
    fin = time.time()
    tps = int(fin - debut)
    print("Temps de jeu:", tps)

    # Entrée du nom du joueur
    nom = input("Entrez votre nom: ")

    # Écriture du score dans le fichier CSV
    with open(FILENAME, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([nom, tps])

    # Affichage des scores
    with open(FILENAME, 'r') as csvfile:
        reader = csv.reader(csvfile)
        scores = list(reader)
        print("Scores:")
        for row in scores:
            print(row)

    # Retour à l'écran d'accueil
    accueil()

def accueil():
    # Initialisation de la fenêtre
    root = Tk()
    root.title("Platform Game")
    root.geometry("1200x700")
    root.configure(bg="sky blue")

    # Création d'un frame
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    # Création des boutons
    ttk.Button(mainframe, text="Jouer", command=lambda: [root.destroy(), gameplay()]).grid(column=2, row=1, sticky=W)
    ttk.Button(mainframe, text="Quitter", command=root.quit).grid(column=2, row=2, sticky=W)

    # Création du label
    ttk.Label(mainframe, text="Bienvenue dans le jeu de plateforme").grid(column=1, row=0, sticky=(W, E))

    # Exécution de la fenêtre
    root.mainloop()

# Appel de la fonction accueil pour lancer l'écran d'accueil
accueil()
