from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
import csv
import os
import time
from random import randint



# Nom du fichier CSV à remplacer maybe
FILENAME = r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\scores.csv"


def gameplay() :
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
        mon_image = PhotoImage(file=os.path.join(current_directory, "images", "doggo_sprite.png"))
        personnage = Label(image=mon_image, bg="sky blue")
        personnage.image = mon_image
        personnage.place(x=xt, y=500)
        # Placement des plateformes
        n = 0
        platform_showed = []
        for i in game_platforms:
            mon_image = PhotoImage(file=os.path.join(current_directory, "images", "platform_sprite.png"))
            platform_showed.append(n)
            platform_showed[n] = Label(image=mon_image, bg="sky blue")
            platform_showed[n].image = mon_image
            platform_showed[n].place(x=i[0], y=i[1] + yt)
            n += 1

        # Actualisation de la page
        root.update()
        label.pack_forget()
        for i in platform_showed:
            i.destroy()
        personnage.destroy()
        platform_destroy(yt, platform_showed)

    # Fin de la boucle de jeu et fermeture de la page
    root.destroy()
    root.mainloop()

    # Affiche le temps écoulé entre le début et la fin du programme
    fin = time.time()

def create_csv_file(FILENAME):
    # Crée le fichier CSV avec les colonnes id, username et score
    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "username", "score"])
    print(f"Fichier CSV '{FILENAME}' créé avec succès.")

def add_score(username, score):
    # Ajoute un score au fichier CSV
    if not os.path.exists(FILENAME):
        create_csv_file(FILENAME)
    
    scores = get_scores()
    new_id = len(scores) + 1  # Génère un nouvel ID basé sur le nombre de lignes existantes
    scores.append([new_id, username, score])
    
    # Trie les scores en fonction du score de manière décroissante
    scores = sorted(scores, key=lambda x: int(x[2]), reverse=True)
    
    # Écrit les scores triés dans le fichier CSV
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "username", "score"])  # Écrit l'en-tête
        for i, row in enumerate(scores):
            writer.writerow([i + 1, row[1], row[2]])  # Réécrit chaque ligne avec le nouvel ID
    print(f"Score ajouté : {username}, {score}")

def get_scores():
    # Récupère les scores du fichier CSV
    scores = []
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            scores = [row for row in reader]
    return scores

def display_scores():
    # Affiche les scores
    scores = get_scores()
    scores = sorted(scores, key=lambda x: int(x[2]), reverse=True)
    print("Classement des scores :")
    for row in scores:
        print(f"Username: {row[1]}, Score: {row[2]}")

def display_scores_in_menu(frame):
    # Récupère et affiche les scores dans le menu
    scores = get_scores()
    scores = sorted(scores, key=lambda x: int(x[2]), reverse=True)
    
    scores_label = Label(frame, text="Podium :", font=("Papyrus", 35), bg='#fe6c90')
    scores_label.pack(pady=10)
    
    for row in scores:
        score_text = f"Username: {row[1]}, Score: {row[2]}"
        score_label = Label(frame, text=score_text, font=("Papyrus", 18), bg='#fe6c90')
        score_label.pack()

def menu():
    root = Tk()
    root.title("Doggo's jump")
    root.attributes('-fullscreen', True)
          
    image_icone = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\images\doggo_sprite.png")
    root.iconphoto(False, image_icone)

    fond_ecran = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\interface_background.png")
    background_label = ttk.Label(root, image=fond_ecran)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
   
    texte_1 = Label(root, text="Doggo's Jump", font=("Papyrus", 45), highlightbackground=root.cget("bg"), borderwidth=0, bg='#93bfe6')
    texte_1.place(relx=0.38, rely=0.1)

    def clic():
        root.destroy()
        gameplay()
        
        
    
    bouton_jouer = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\button_doggos_jump_cool.png")
    bouton_1 = Button(root, image=bouton_jouer, borderwidth=0, highlightthickness=0, relief='flat', command=clic, highlightbackground=root.cget("bg"))
    bouton_1.place(relx=0.475, rely=0.232)
    
    bouton_quitter = PhotoImage(file=r'C:\Users\LucaF\Documents\cours_IPSA\GP_prog\bouton_quit_final.png')
    bouton_2 = Button(root, text='Fermer le jeu', image=bouton_quitter, command=root.destroy, borderwidth=0, highlightthickness=0, relief='flat')
    bouton_2.place(relx=0.475, rely=0.87)

    scores_frame = Frame(root, bg='#fe6c90')
    scores_frame.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.25)
    display_scores_in_menu(scores_frame)

    root.mainloop()

def create():
    root2 = Tk()
    root2.title("Doggo's jump : le jeu")
    root2.config(width=700, height=900)
    
    def click():
        root2.destroy()
        game()
    
    bouton_perd = ttk.Button(root2, text='perdu', command=click)
    bouton_perd.pack()

    root2.mainloop()

def game():
    root_game = Tk()
    root_game.title("Game Over")
    root_game.attributes('-fullscreen', True)
    ecran = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\interface_background.png")
    background_label = ttk.Label(root_game, image=ecran)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    texte = Label(root_game, text='Game Over !', font=('Papyrus', 50), bg='#93bfe6')
    texte.place(relx=0.38, rely=0.1)

    bouton_quitter = PhotoImage(file=r'C:\Users\LucaF\Documents\cours_IPSA\GP_prog\bouton_quit_final.png')
    bouton_1 = Button(root_game, image=bouton_quitter, text='Ragequit', command=root_game.destroy, borderwidth=0, highlightthickness=0, relief='flat')
    bouton_1.place(relx=0.47, rely=0.82)

    score = Label(root_game, text='Votre score : ', font=('Papyrus', 30), bg='#fe6c90')
    score.place(relx=0.39, rely=0.45)

    def sarcozy():
        root_game.destroy()
        menu()
    
    bouton_jouer = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\button_doggos_jump_cool.png")
    bouton_2 = Button(root_game, text='Rejouer', command=sarcozy, image=bouton_jouer, borderwidth=0, highlightthickness=0, relief='flat')
    bouton_2.place(relx=0.47, rely=0.32)

    def register():
        contenu = name.get()
        add_score(contenu, 75)  # Remplacer 69 par le score réel du joueur
                         
    name = Entry(root_game)
    name.place(relx=0.48, rely=0.55)
    
    enregistrer = Button(root_game, text='Enregistrer', command=register)
    enregistrer.place(relx=0.3, rely=0.5)
    root_game.mainloop()

menu()

