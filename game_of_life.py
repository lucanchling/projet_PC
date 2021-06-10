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


def voisins(taille_Grille,grille):
    nbVoisin=0
    lstvoisinou=[]
    iVoisin=[[1,0],[-1,0],[0,1],[0,-1],[-1,-1],[1,-1],[-1,1],[1,1]]
    for x in range(taille_Grille):
        for y in range(taille_Grille):
            nbVoisin=0
            xr=0+x
            yr=0+y
            for t in iVoisin:
                voisin=[xr+t[0],yr+t[1]]
                if voisin[0]<taille_Grille and voisin[1]<taille_Grille and voisin[0]>=0 and voisin[1]>=0:
                    if grille[voisin[1]+(voisin[0]*taille_Grille)]==1:
                        nbVoisin+=1
            lstvoisinou.append(nbVoisin)
            
    
    #print(lstvoisinou) 
    print(len(lstvoisinou))   
    for i in range(long_horiz)     :
        print(lstvoisinou[i*long_horiz : (i+1)*long_horiz])       




#def Death_Or_Alive(nbVoisin,position,taille_Grille,coordonnées):
 #   for i in coordonnées()
    # ma_Grille=[]
    # état==0
    # if nbVoisin<=2:
    #     état==0
    # elif nbVoisin==2 or nbVoisin==3:
    #     état==1
    # elif nbVoisin>3:
    #     état==0
    

long_partag=0
long_partag2=0
if (long_horiz%2)==0:
    long_partag==long_horiz*0.5
    coordonnées=[[0,0],[long_partag,long_partag],[0,long_partag+1],[long_partag,long_partag*2],[long_partag+1,0],[2*long_partag,long_partag],[long_partag+1,long_partag+1],[2*long_partag,2*long_partag]]
else:
    long_partag==floor(long_horiz*0.5)
    long_partag2=long_partag+1
    coordonnées=[[0,0],[long_partag,long_partag],[0,long_partag+1],[long_partag,long_partag*2],[long_partag+1,0],[2*long_partag,long_partag],[long_partag+1,long_partag+1],[2*long_partag,2*long_partag]]

grille=mp.Array('i',[randint(0,1) for i in range(nb_cellule)])

affiche_Grille(long_horiz,grille)
voisins(long_horiz,grille)
#print(grille[:])



# for i in range (nb_proc):
#         tab_pid[i]=mp.Process(target=Death_Or_Alive,args=(nbVoisin,position,taille_Grille,coordonnées)) 
#         tab_pid[i].start()


