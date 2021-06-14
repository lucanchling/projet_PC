import multiprocessing as mp
from random import randint
from math import floor
import time
import os


CL_WHITE="\033[01;37m"                  #  Blanc
CL_BLACK="\033[22;30m"                  #  Noir
CLEARSCR="\x1B[2J\x1B[;H"        #  Clear SCReen
CL_RED="\033[22;31m"

nb_proc=4                                                             #nombre de processus fils que nous allons faire travailler
long_horiz=20                                                         #longueur du côté de notre grille 
nb_cellule=long_horiz**2                                              #nombre de cellules              

def affiche_Grille(taille_Grille,Grille):                             #fonction qui permet d'afficher la grille et de mettre la case en noir si vivant et en blanc si mort                  
    print(CLEARSCR)
    for i in range(taille_Grille):
        for j in range(taille_Grille):
            couleur=CL_BLACK
            if Grille[j+(i*taille_Grille)]==0:                       #on parcourt la grille pour voir l'état de chaque cellule pour voir si on est mort ou en vit       
                couleur = CL_WHITE
            else:
                couleur = CL_BLACK
            color(couleur)
            print(' A ',end='')

        print('')



def color(couleur):                                                 #fonction qui rajoute la couleur et met un espace entre chaque cases pour que ce soit plus visible
    print(couleur,end='')
 

def nbVoisins(grille,taille_Grille,position):                       #fonction qui compte le nombre de voisins vivants pour chaque cellule
    nbVoisin=0                                                    #on initialise le compteur          
    x=(position%taille_Grille)-1                                    #il s'agit de la position en x par rapport à la cellule que nous sommes en train d'étudier (d'indice position)
    y=int(position/taille_Grille)
    iVoisin=[[1,0],[-1,0],[0,1],[0,-1],[-1,-1],[1,-1],[-1,1],[1,1]]  #les indices correspondant aux coordonnées de chaque voisin 
    
    for i in iVoisin:                                               #on parcourt la liste de voisins pour voir si le voisin est bien dans la grille ou non puis si il est vivant on incrémente le compteur nbVoisin
        voisin=[x+i[0],y+i[1]]
        if voisin[0]<taille_Grille and voisin[1]<taille_Grille and voisin[0]>=0 and voisin[1]>=0:
            if grille[voisin[1]+(voisin[0]*taille_Grille)]==1:
                nbVoisin+=1
    return nbVoisin                                                 #on retourne cette valeur pour la fonction suivante



def Death_Or_Alive(nbVoisin,état,étatn1):                   #cette fonction nous permet de déterminer le nouvel état de la cellule (étatn1)
            if état==1:                                            #il s'agit des conditions du jeu pour savoir si la cellule va vivre ou mourir
                if nbVoisin<2:
                    étatn1=0
                elif nbVoisin==2 or nbVoisin==3:
                    étatn1=1
                elif nbVoisin>3:
                    étatn1=0
            else:
                if nbVoisin==3:
                    étatn1=1
            
            return étatn1                               #on retourne le nouvel état





    


grille=mp.Array('i',[randint(0,1) for i in range(nb_cellule)])          #on créé la grille partagée d'origine
grillen1=mp.Array('i',range(nb_cellule))                                #il s'agit de la grille à l'instant t+1 soit après la première itération



for i in range(nb_cellule):                                     #dans cette boucle pour chaque cellule, on compte le nombre de voisins vivants
    nb=nbVoisins(grille,long_horiz,i)
    étatnouveau=Death_Or_Alive(nb,grille[i],0)                  #on détermine son nouvel état 
    grillen1[i]=étatnouveau                                     #on recréé notre grille à l'instant t+1 soit après la première itération


tab_pid=[0 for i in range (nb_proc)]
for i in range (nb_proc):                                       #on créé le nombre de processus fils
    for j in [i,i+100]:                                         #on partage la zone de travail pour chaque fils
        tab_pid[i]=mp.Process(target=nbVoisins,args=(grille,long_horiz,j)) 
        tab_pid[i].start()

     
affiche_Grille(long_horiz,grille)                                 #on affiche les grilles
affiche_Grille(long_horiz,grillen1)

