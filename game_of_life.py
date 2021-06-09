import multiprocessing as mp
from random import randint
from math import floor
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


def voisins(taille_Grille,grille,position):
    nbVoisin=0
    iVoisin=[1,-1,long_horiz,-long_horiz,long_horiz+1,long_horiz-1,-long_horiz-1,-long_horiz+1]



def Death_Or_Alive(nbVoisin,position,taille_Grille):
    ma_Grille=[]



if (long_horiz%2)==0:
    long_partag==long_horiz*0.5
else:
    long_partag==floor(long_horiz*0.5)
    long_partag2==long_partag+1


grille=mp.Array('i',[randint(0,1) for i in range(nb_cellule)])

affiche_Grille(long_horiz,grille)

for i in range (nb_proc):
        tab_pid[i]=mp.Process(target=Death_Or_Alive,args=(nbVoisin,position,taille_Grille)) 
        tab_pid[i].start()


