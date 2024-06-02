from tkinter import *
from tkinter import ttk
import csv
import os
import time
from random import randint

# Nom du fichier CSV à remplacer peut-être
FILENAME = r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\scores.csv"

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
                # Enregistrement de chaque plateforme
                game_platforms.append((pf_x, pf_y))
                # Séparation des plateformes selon y
                pf_y -= 300 - pf_H

    def platform_inf(character_x, character_y, dydt, y0, obstacle_inf):
        for platform in game_platforms:
            if (character_x >= platform[0] - 70 and character_x <= platform[0] + 200 and
                character_y >= platform[1] - 200 and character_y <= platform[1] - 195 and dydt >= 0):
                obstacle_inf = 1
                y0 = platform[1] - 200
        return obstacle_inf, y0

    def create_character(event=None):
        global character
        x = 20
        y0 = -500
        t = 0
        g = 5
        y = y0
        while True:
            character.place(x=x, y=y)
            root.update()
            x = x(x)
            y, t, dydt, obstacle_inf, y0 = y(x, y, t=t, y0=y0, g=g)
            if y > 700:
                print("Game over")
                add_score('username', randint(0, 100))
                root.quit()
                break

    root = Tk()
    root.title("Doggo's jump")
    root.geometry("1300x700")
    root.bind("<KeyPress>", press)
    root.bind("<KeyRelease>", release)

    # Chargement de l'image de fond
    fond_ecran = PhotoImage(file=os.path.join(current_directory, 'interface_background.png'))
    background_label = Label(root, image=fond_ecran)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    character_image = PhotoImage(file=os.path.join(current_directory, 'doggo_sprite.png'))
    character = Label(root, image=character_image)
    character.place(x=50, y=650)

    create_platform(-500)
    root.after(100, create_character)
    root.mainloop()

if __name__ == "__main__":
    menu()
