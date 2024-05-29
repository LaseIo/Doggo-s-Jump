from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
import csv
import os

# Nom du fichier CSV à remplacer maybe
FILENAME = r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\scores.csv"

def create_csv_file(FILENAME):
    # Crée le fichier CSV avec les colonnes id, username et score
    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "username", "score"])
    print(f"Fichier CSV '{FILENAME}' créé avec succès.")

def add_score(username,score):
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
def menu():
    root = Tk()
    root.title("Doggo's jump")
    root.attributes('-fullscreen',True)
    


    image_icone = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\doggo.png")
    root.iconphoto(False,image_icone)

    fond_ecran = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\interface_background.png")
    background_label = ttk.Label(root, image=fond_ecran)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

   


    texte_1=Label(root,text="Doggo's Jump",font=("papyrus",45),highlightbackground=root.cget("bg"),borderwidth=0,bg='#93bfe6')
    texte_1.place(relx=0.38,rely=0.1)

    def clic():
        root.destroy()
        create()
    
    bouton_jouer = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\button_doggos_jump_cool.png")

    bouton_1 = Button(root,image=bouton_jouer,borderwidth=0,highlightthickness=0,relief='flat',command=clic,highlightbackground=root.cget("bg"))
    bouton_1.place(relx=0.475,rely=0.232)
    
    

    bouton_quitter= PhotoImage(file=r'C:\Users\LucaF\Documents\cours_IPSA\GP_prog\bouton_quit_final.png')
    
    bouton_2 = Button(root,text='Fermer le jeu',image=bouton_quitter,command=root.destroy,borderwidth=0,highlightthickness=0,relief='flat')
    bouton_2.place(relx=0.475,rely=0.87)

    root.mainloop()

def create():
    root2 = Tk()
    root2.title("Doggo's jump : le jeu")
    root2.config(width=700,height=900)


    
    def click():
        root2.destroy()
        game()
    
    

    bouton_perd = ttk.Button(root2,text='perdu',command=click)
    bouton_perd.pack()

  
    
    
    root2.mainloop()


def game():

    root_game = Tk()
    root_game.title("Game Over")
    root_game.attributes('-fullscreen',True)
    ecran = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\interface_background.png")
    background_label = ttk.Label(root_game, image=ecran)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    texte=Label(root_game,text='Game Over !',font=('Papyrus',50),bg='#93bfe6')
    texte.place(relx=0.38,rely=0.1)

    bouton_jouer = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\button_doggos_jump_cool.png")
    bouton_quitter= PhotoImage(file=r'C:\Users\LucaF\Documents\cours_IPSA\GP_prog\bouton_quit_final.png')
    bouton_1 = Button(root_game,image=bouton_quitter,text='Ragequit',command=root_game.destroy,borderwidth=0,highlightthickness=0,relief='flat')
    bouton_1.place(relx=0.47,rely=0.82)

    score=Label(root_game,text='Votre score : ',font=('Papyrus',30),bg='#fe6c90')
    score.place(relx=0.39,rely=0.45)

    def sarcozy():
        root_game.destroy()
        menu()
    

    

    bouton_jouer = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\button_doggos_jump_cool.png")
    bouton_2 = Button(root_game,text='Rejouer',command=sarcozy,image=bouton_jouer,borderwidth=0,highlightthickness=0,relief='flat')
    bouton_2.place(relx=0.47,rely=0.32)

    def register():
        contenu=name.get()
        add_score(contenu,69)

        
        

    name=Entry(root_game)
    name.place(relx=0.48,rely=0.55)
    
    enregistrer=Button(root_game,text='enregistrer',command=register)
    enregistrer.place(relx=0.3,rely=0.5)
    root_game.mainloop()


menu()