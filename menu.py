from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage


def menu():
    root = Tk()
    root.title("Doggo's jump")
    root.attributes('-fullscreen',True)


    image_icone = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\doggo.png")
    root.iconphoto(False,image_icone)

    fond_ecran = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\7.png")
    background_label = ttk.Label(root, image=fond_ecran)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

   


    texte_1=ttk.Label(root,text="Doggo's Jump",font=("papyrus",45))
    texte_1.place(relx=0.38,rely=0.25)

    def clic():
        root.destroy()
        create()
    
    bouton_jouer = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\9.png")
    bouton_1 = ttk.Button(root,text='Jouez!',command=clic,image=bouton_jouer,width=2,)
    bouton_1.place(relx=0.48,rely=0.5)


    bouton_2 = ttk.Button(root,text='Fermer le jeu',command=root.destroy)
    bouton_2.place(relx=0.48,rely=0.75)

    root.mainloop()

def create():
    root2 = Tk()
    root2.title("Doggo's jump : le jeu")
    root2.config(width=700,height=900)

    canvas=Canvas(root2,width=650,height=950)
    
    perso = PhotoImage(file=r"C:\Users\LucaF\Documents\cours_IPSA\GP_prog\doggo.gif")
    chien = ttk.Label(root2,image=perso)
    chien.place(x=300,y=500)
    def move(dx,dy):
        canvas.move(chien,dx,dy)

    def move_up():
        move(0,100)
    
    def move_down():
        move(0,-100)
    
    def move_right():
        move(100,0)
    
    def move_left():
        move(-100,0)
    

    
    
    bouton_haut = ttk.Button(root2,text='haut',command=move_up)
    bouton_haut.pack()
    bouton_bas = ttk.Button(root2, text="bas",command=move_down)
    bouton_bas.pack()
    bouton_droite = ttk.Button(root2,text="droite",command=move_right)
    bouton_droite.pack()
    bouton_gauche = ttk.Button(root2,text="gauche",command=move_left )
    bouton_gauche.pack()

    root2.bind('d',bouton_droite)
    root2.bind('q',bouton_gauche)
    root2.bind('z',bouton_haut)
    root2.bind('s',bouton_bas)

    
    
    root2.mainloop()

menu()









