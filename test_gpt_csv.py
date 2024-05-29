import csv
import os

# Nom du fichier CSV à remplacer maybe
FILENAME = 'scores.csv'

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
