import multiprocessing as mp
from random import randint
from math import floor
import time
import os


CL_WHITE="\033[01;37m"                  #  Blanc
CL_BLACK="\033[22;30m"                  #  Noir
CLEARSCR="\x1B[2J\x1B[;H"        #  Clear SCReen
CL_RED="\033[22;31m"

nb_proc=4
long_horiz=20
nb_cellule=long_horiz**2

def affiche_Grille(taille_Grille,Grille):
    print(CLEARSCR)
    for i in range(taille_Grille):
        for j in range(taille_Grille):
            couleur=CL_BLACK
            if Grille[j+(i*taille_Grille)]==0:
                couleur = CL_WHITE
            else:
                couleur = CL_BLACK
            color(couleur)
            print(' A ',end='')

        print('')



def color(couleur):
    print(couleur,end='')
 

def nbVoisins(grille,taille_Grille,position):
    nbVoisin=0
    x=(position%taille_Grille)-1
    y=int(position/taille_Grille)
    iVoisin=[[1,0],[-1,0],[0,1],[0,-1],[-1,-1],[1,-1],[-1,1],[1,1]]
    
    for i in iVoisin:
        voisin=[x+i[0],y+i[1]]
        if voisin[0]<taille_Grille and voisin[1]<taille_Grille and voisin[0]>=0 and voisin[1]>=0:
            if grille[voisin[1]+(voisin[0]*taille_Grille)]==1:
                nbVoisin+=1
    return nbVoisin



def Death_Or_Alive(nbVoisin,état,étatn1):
            if état==1:
                if nbVoisin<2:
                    étatn1=0
                elif nbVoisin==2 or nbVoisin==3:
                    étatn1=1
                elif nbVoisin>3:
                    étatn1=0
            else:
                if nbVoisin==3:
                    étatn1=1
            
            return étatn1





    


grille=mp.Array('i',[randint(0,1) for i in range(nb_cellule)])
grillen1=mp.Array('i',range(nb_cellule))



for i in range(nb_cellule):
    nb=nbVoisins(grille,long_horiz,i)
    étatnouveau=Death_Or_Alive(nb,grille[i],0)
    grillen1[i]=étatnouveau


tab_pid=[0 for i in range (nb_proc)]
for i in range (nb_proc):
    for j in [i,i+100]:
        tab_pid[i]=mp.Process(target=nbVoisins,args=(grille,long_horiz,j)) 
        tab_pid[i].start()
affiche_Grille(long_horiz,grille)
#voisins(long_horiz,grille)
#print(grille[:])
affiche_Grille(long_horiz,grillen1)

