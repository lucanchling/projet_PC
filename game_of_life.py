import multiprocessing as mp
from random import randint
import time
import os


CL_WHITE="\033[01;37m"                  #  Blanc
CL_BLACK="\033[22;30m"                  #  Noir
CLEARSCR="\x1B[2J\x1B[;H"        #  Clear SCReen

nb_proc=4
long_horiz=20
nb_cellule=long_horiz**2
def affiche_Grille(taille_Grille,Grille):
    os.system('clear')
    for i in range(taille_Grille):
        for j in range(taille_Grille):
            if [j+(i*taille_Grille)]==0:
                couleur = CL_WHITE
            else:
                couleur = CL_BLACK
            color(couleur)
        print(' A ',end='')



def color(couleur):
    print(couleur,end='')


grille=mp.Array('i',[randint(0,1) for i in range(nb_cellule)])

affiche_Grille(long_horiz,grille)