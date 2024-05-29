from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
import csv
import os
import time
from random import randint

# Nom du fichier CSV à remplacer maybe
FILENAME = r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\scores.csv"

# Création du fichier CSV pour les scores
def create_csv_file(filename):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "username", "score"])
    print(f"Fichier CSV '{filename}' créé avec succès.")

# Ajout d'un score au fichier CSV
def add_score(username, score):
    if not os.path.exists(FILENAME):
        create_csv_file(FILENAME)
    
    scores = get_scores()
    new_id = len(scores) + 1
    scores.append([new_id, username, score])
    
    # Tri des scores
    scores = sorted(scores, key=lambda x: int(x[2]), reverse=True)
    
    # Écriture des scores triés dans le fichier CSV
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "username", "score"])
        for i, row in enumerate(scores):
            writer.writerow([i + 1, row[1], row[2]])
    print(f"Score ajouté : {username}, {score}")

# Récupération des scores depuis le fichier CSV
def get_scores():
    scores = []
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            scores = [row for row in reader]
    return scores

# Affichage des scores dans le terminal
def display_scores():
    scores = get_scores()
    scores = sorted(scores, key=lambda x: int(x[2]), reverse=True)
    print("Classement des scores :")
    for row in scores:
        print(f"Username: {row[1]}, Score: {row[2]}")

# Affichage des scores dans le menu principal
def display_scores_in_menu(frame):
    scores = get_scores()
    scores = sorted(scores, key=lambda x: int(x[2]), reverse=True)
    
    scores_label = Label(frame, text="Classement des scores :", font=("Papyrus", 20), bg='#93bfe6')
    scores_label.pack(pady=10)
    
    for row in scores:
        score_text = f"Username: {row[1]}, Score: {row[2]}"
        score_label = Label(frame, text=score_text, font=("Papyrus", 15), bg='#93bfe6')
        score_label.pack()

# Dictionnaire des touches du jeu
global game_keys
game_keys = {"space": 0, "Left": 0, "Right": 0, "Up": 0}

# Fonction "touche appuyée"
def press(event):
    if event.keysym in game_keys.keys():
        game_keys[event.keysym] = 1

# Fonction "touche relâchée"
def release(event):
    if event.keysym in game_keys.keys():
        game_keys[event.keysym] = 0

# Direction du personnage
def dir():
    if game_keys["Right"] == 1:
        return 1
    elif game_keys["Left"] == 1:
        return -1
    else:
        return 0

# Prêt pour sauter
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
    y = ((-(3 / 4) * g * t ** 2) * (1 - obstacle_inf) + 35 * g * t * (1 - ready(obstacle_inf))) / 7 + y0 + (1 - obstacle_sup) * game_keys["Up"] * (1 - ready(obstacle_inf))
    dydt = ((-(3 / 2) * g * t) + 35 * g) / 7
    obstacle_inf, y0 = platform_inf(x, y, dydt, y0, obstacle_inf)
    if obstacle_inf == 0 or game_keys["Up"] * ready(obstacle_inf) == 1:
        time.sleep(1 / 240)
        t += 1
    else:
        t = 0
    return y, t, dydt, obstacle_inf, y0

# Création de la liste globale des coordonnées de chaque plateforme générée
global game_platforms
game_platforms = []

# Création des plateformes
def create_platform(character_y):
    pf_y = character_y + 800 - 65
    pf_x = randint(0, 1100)
    while pf_y > character_y:
        for i in range(randint(1, 3)):
            pf_x_mem = pf_x
            pf_x = randint(0, 1300 - 300)
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

# Informations sur les plateformes
def platform_inf(xc, yc, dydt, y0, obstacle_inf):
    if yc <= 0 and y0 == 0:
        return 1, 0
    for i in game_platforms:
        if (dydt < 0 and i[1] - 40 < 500 - yc < i[1] and i[0] - 30 < xc < i[0] + 270) or (y0 == i[1] and 1 - ready(obstacle_inf) != 1):
            return 1, 500 - i[1]
    return 0, y0

# Création de la liste globale des plateformes affichées
global platform_showed
platform_showed = []

# Destruction des plateformes en dehors de l'écran
def platform_destroy(yc, platform_showed):
    for i in range(len(game_platforms)):
        if game_platforms[i][1] > 900 - yc:
            game_platforms.pop(i)
            platform_showed.pop(len(game_platforms) - i)
            new_platform()
            break

# Création de nouvelles plateformes
def new_platform():
    pf_x_mem = game_platforms[-1][0]
    pf_y = game_platforms[-1][1] - randint(0, 120)
    if 0 > pf_x_mem > 333:
        pf_x = randint(0, 750)
    elif 333 > pf_x_mem > 667:
        pf_x = randint(0, 1000)
    else:
        pf_x = randint(250, 1000)
    if pf_x_mem + 200 > pf_x > pf_x_mem - 200:
        pf_y -= randint(140, 180)
    else:
        pf_y -= randint(80, 180)
    game_platforms.append((pf_x, pf_y))

# Interface du menu principal
def menu():
    root = Tk()
    root.title("Doggo's jump")
    root.attributes('-fullscreen', True)
    
    image_icone = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\doggo.png")
    root.iconphoto(False, image_icone)

    fond_ecran = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\interface_background.png")
    background_label = ttk.Label(root, image=fond_ecran)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
   
    texte_1 = Label(root, text="Doggo's Jump", font=("Papyrus", 45), highlightbackground=root.cget("bg"), borderwidth=0, bg='#93bfe6')
    texte_1.place(relx=0.38, rely=0.1)

    def clic():
        root.destroy()
        create()
    
    bouton_jouer = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\button_doggos_jump_cool.png")
    bouton_1 = Button(root, image=bouton_jouer, command=clic)
    bouton_1.place(relx=0.42, rely=0.45)

    def clic_2():
        new_window = Toplevel(root)
        new_window.title("Scores")
        new_window.geometry("300x400")
        
        frame = Frame(new_window, bg='#93bfe6')
        frame.pack(fill=BOTH, expand=True)
        
        display_scores_in_menu(frame)

    bouton_scores = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\button_doggos_jump_cool_2.png")
    bouton_2 = Button(root, image=bouton_scores, command=clic_2)
    bouton_2.place(relx=0.42, rely=0.65)
    
    texte_2 = Label(root, text="A game by Luca Fontanella, Yacine Tighlit, Axel et Matthieu from IPSA 2023-2024", font=("Papyrus", 10), highlightbackground=root.cget("bg"), borderwidth=0, bg='#93bfe6')
    texte_2.place(relx=0.38, rely=0.95)
    
    root.mainloop()

# Interface du jeu
def create():
    global player_name
    player_name = "DefaultPlayer"  # Mettre le nom du joueur ici ou à récupérer d'une entrée utilisateur

    fenetre = Tk()
    fenetre.title("Doggo's jump")
    fenetre.attributes('-fullscreen', True)
    
    canvas = Canvas(fenetre, width=1300, height=900, bg="white")
    canvas.pack()
    
    photo = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\doggo.png")
    joueur = canvas.create_image(650, 450, image=photo)
    
    platform()
    
    fenetre.bind("<KeyPress>", press)
    fenetre.bind("<KeyRelease>", release)

    t = 0
    y0 = 0
    g = 5
    score = 0
    
    while True:
        x_coords = canvas.coords(joueur)[0]
        y_coords = canvas.coords(joueur)[1]
        
        x_coords = x(x_coords)
        y_coords, t, dydt, obstacle_inf, y0 = y(x_coords, y_coords, obstacle_inf=0, obstacle_sup=0, t=t, y0=y0, g=g)
        
        canvas.coords(joueur, x_coords, y_coords)
        
        if y_coords > 900:
            break
        
        platform_destroy(y_coords, platform_showed)
        
        for i in platform_showed:
            canvas.move(i, 0, g)
        
        fenetre.update()
        time.sleep(0.01)
        
        score += 1
    
    canvas.destroy()
    add_score(player_name, score)
    display_scores()
    
    game_over_label = Label(fenetre, text="Game Over", font=("Papyrus", 30), bg="white")
    game_over_label.pack(pady=20)
    
    fenetre.mainloop()

def platform():
    create_platform(0)
    for i in game_platforms:
        x1, y1 = i
        x2, y2 = x1 + 300, y1 + 20
        platform_showed.append(Canvas.create_rectangle(x1, y1, x2, y2, fill="green"))

if __name__ == "__main__":
    menu()
