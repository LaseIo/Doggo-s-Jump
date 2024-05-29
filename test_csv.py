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
    
    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Génère un nouvel ID basé sur le nombre de lignes existantes
        new_id = sum(1 for _ in open(FILENAME))  # Cette ligne compte les lignes dans le fichier CSV
        writer.writerow([new_id, username, score])
    print(f"Score ajouté : {username}, {score}")

def get_scores():
    # Récupère les scores du fichier CSV
    scores = []
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            scores = sorted([row for row in reader], key=lambda x: int(x[2]), reverse=True)
    return scores

def display_scores():
    # Affiche les scores
    scores = get_scores()
    print("Classement des scores :")
    for row in scores:
        print(f"Username: {row[1]}, Score: {row[2]}")

# Exemple
if __name__ == "__main__":
    add_score("Player1", 100)
    add_score("Player2", 150)
    add_score("Player3", 120)
    display_scores()
