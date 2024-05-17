### GP Programmation
## Inputs du jeu


# Définition du dictionnaire des touches du jeu
global game_keys
game_keys={"space":0,"Left":0,"Right":0,"Up":0}

# Définition de la fonction "touche appuyée"
def press(event):
    if event.keysym in game_keys.keys():
        game_keys[event.keysym]=1

# Définition de la fonction "touche relachée"
def release(event):
    if event.keysym in game_keys.keys():
        game_keys[event.keysym]=0

# Definition de la fonction qui donne la direction à x         
def dir():
    if game_keys["Right"]==1:
        return 1
    elif game_keys["Left"]==1:
        return -1
    else :
        return 0

def ready(obstacle_inf=0):
    jump_ready = 1
    if obstacle_inf == 1 and game_keys["Up"]==0 :
        return 1
    else :
        return 0














