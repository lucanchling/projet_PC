# Simulation d'un Déplacement d'un robot
# Juin 2021

#------------------------------------------------

CLEARSCR="\x1B[2J\x1B[;H"        #  Clear SCReen
CLEAREOS = "\x1B[J"                #  Clear End Of Screen
CLEARELN = "\x1B[2K"               #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"               #  Clear Curseur UP
GOTOYX   = "\x1B[%.2d;%.2dH"       #  Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"
CRLF  = "\r\n"                  #  Retour à la ligne

# VT100 : Actions sur le curseur
CURSON   = "\x1B[?25h"             #  Curseur visible
CURSOFF  = "\x1B[?25l"             #  Curseur invisible

# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m"                  #  Normal
BOLD = "\x1B[1m"                    #  Gras
UNDERLINE = "\x1B[4m"               #  Souligné


# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m"                  #  Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m"                    #  Rouge
CL_GREEN="\033[22;32m"                  #  Vert
CL_BROWN = "\033[22;33m"                #  Brun
CL_BLUE="\033[22;34m"                   #  Bleu
CL_MAGENTA="\033[22;35m"                #  Magenta
CL_CYAN="\033[22;36m"                   #  Cyan
CL_GRAY="\033[22;37m"                   #  Gris

# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m"               #  Gris foncé
CL_LIGHTRED="\033[01;31m"               #  Rouge clair
CL_LIGHTGREEN="\033[01;32m"             #  Vert clair
CL_YELLOW="\033[01;33m"                 #  Jaune
CL_LIGHTBLU= "\033[01;34m"              #  Bleu clair
CL_LIGHTMAGENTA="\033[01;35m"           #  Magenta clair
CL_LIGHTCYAN="\033[01;36m"              #  Cyan clair
CL_WHITE="\033[01;37m"                  #  Blanc

#-------------------------------------------------------

# Importation des différents modules :

from multiprocessing import Process, Value, Lock, Array
import os, time,math, random, sys
from enum import Enum
from typing import ValuesView
import SharedArray as sa 
#------------------------------------------------


lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY, CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, \
             CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

def effacer_ecran() : print(CLEARSCR,end='')
    # for n in range(0, 64, 1): print("\r\n",end='')

def erase_line_from_beg_to_curs() :
    print("\033[1K",end='')

def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')

def move_to(lig, col) : # No work print("\033[%i;%if"%(lig, col)) # print(GOTOYX%(x,y))
    print("\033[" + str(lig) + ";" + str(col) + "f",end='')

def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='')

#------------------------------------------------
# Enumeration pour de la clarté dans le code 
# Utilisation en name_of_class.{}

# Pour les commandes :
class Cmd(Enum):
    Front = 1
    Right = 2
    Left = 3
    Back = 4

# Pour les différentes valeurs dans la grille :
class Case(Enum):
    Blank = 0
    Obstacle = 1
    Robot = 2

# Pour la direction du déplacement du robot :
class Direction(Enum):
    Up = 0
    Down = 1
    Right = 2
    Left = 3
#------------------------------------------------

##################
# Les Constantes #
##################

#------------------------------------------------
temps_Ecran = Value('d',.25) # Initialisation du temps pour la fonction écran
temps_Ir = Value('d',.25) # Initialisation du temps pour la fonction ir
temps_Controleur = Value('i',1) # Pour le controleur
temps_US = Value('d',.25) # Pour le capteur US
temps_BU = Value('d',0.001) # Pour le bumper
#------------------------------------------------

#################
# Les Fonctions #
#################

#------------------------------------------------
# Permet la construction de la grille
def grille(n):
    # Initialisation d'une grille partagée de taille n^2
    try :
        grille = sa.create("shm://grille", dtype=int,shape=(n,n))
    except FileExistsError:
        sa.delete("grille")
        grille = sa.create("shm://grille", dtype=int,shape=(n,n))
    # Mise en place des obstacles :
    for i in range(n):
        j = random.randint(0,n-1)
        grille[i][j]=Case.Obstacle.value
    # Positionnement du robot sur une case vide
    i,j=random.randint(0,taille_grille-1),n//2
    while grille[i][j] == Case.Obstacle.value:
        i=(i+1)%taille_grille  # Modulo pour éviter un out_of_bounds
        j=(j+1)%taille_grille
    grille[i][j] = Case.Robot.value

    return grille

# Permet d'utiliser conjointement les différents capteurs afin de contrôler le robot 
def controleur():
    tic = time.time()
    while True:
        # Pour le faire toutes les temps_Ecran secondes
        if (tic-time.time())%temps_Controleur.value == 0:
            Commande = Cmd.Front.value
            Flag = False
            if Flag_IR.value == True:
                Commande = Cmd_IR.value
                Flag = Flag_IR.value
            if Flag_US.value == True:
                Commande = Cmd_US.value
                Flag = Flag_US.value
            if Flag_BU.value == True:
                Commande = Cmd_BU.value
                Flag = Flag_BU.value
            
            Verrou_memory.acquire()
            
            mem_Cmd.value = Commande
            mem_Flag.value = Flag   
            Verrou_memory.release()

# Permet l'affichage sur l'écran (I suppose)
def ecran(n):
    print(grille(n))
    tic = time.time()
    while True:
        # Pour le faire toutes les temps_Ecran secondes
        if (tic-time.time())%temps_Ecran.value == 0:
            grille_loc = sa.attach("shm://grille")
            # Pour connaître la direction du robot :
            

            for ligne in range(taille_grille):
                for colonne in range(taille_grille):
                    if grille_loc[ligne][colonne] == Case.Robot.value:
                        posX,posY = colonne,ligne
            deltaX = Robot_X.value-posX
            deltaY = Robot_Y.value-posY
            
            
            # Pour ignorer lorsque il y a 'téléportation' dans la grille
            if abs(deltaX) == taille_grille-1 or abs(deltaY) == taille_grille-1:
                pass
            else:
                if deltaX == 0 and deltaY > 0:
                    Direction_Robot.value = Direction.Up.value
                if deltaX == 0 and deltaY < 0 :
                        Direction_Robot.value = Direction.Down.value
                if deltaY == 0 and deltaX > 0:
                    Direction_Robot.value = Direction.Left.value
                if deltaY == 0 and deltaX < 0:
                    Direction_Robot.value = Direction.Right.value
            
            Verrou.acquire()
            # Direction : Vers le Haut
            if Direction_Robot.value == Direction.Up.value:
                if mem_Cmd.value == Cmd.Front.value:
                    # Pour aller tout droit
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[(Robot_Y.value-1)%taille_grille][Robot_X.value] = Case.Blank.value,Case.Robot.value
                if mem_Cmd.value == Cmd.Left.value:
                    # Pour aller à droite
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[Robot_Y.value][(Robot_X.value+1)%taille_grille] = Case.Blank.value,Case.Robot.value
                else :
                    # Pour aller à gauche
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[Robot_Y.value][(Robot_X.value-1)%taille_grille] = Case.Blank.value,Case.Robot.value
            
            # Direction : Vers le Bas
            if Direction_Robot.value == Direction.Down.value:
                if mem_Cmd.value == Cmd.Front.value:
                    # Pour aller tout droit
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[(Robot_Y.value+1)%taille_grille][Robot_X.value] = Case.Blank.value,Case.Robot.value
                if mem_Cmd.value == Cmd.Left.value:
                    # Pour aller à droite
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[Robot_Y.value][(Robot_X.value-1)%taille_grille] = Case.Blank.value,Case.Robot.value
                else :
                    # Pour aller à gauche
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[Robot_Y.value][(Robot_X.value+1)%taille_grille] = Case.Blank.value,Case.Robot.value
            
            # Direction : Vers la droite
            if Direction_Robot.value == Direction.Right.value:
                if mem_Cmd.value == Cmd.Front.value:
                    # Pour aller tout droit
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[Robot_Y.value][(Robot_X.value+1)%taille_grille] = Case.Blank.value,Case.Robot.value
                if mem_Cmd.value == Cmd.Left.value:
                    # Pour aller à droite
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[(Robot_Y.value+1)%taille_grille][Robot_X.value] = Case.Blank.value,Case.Robot.value
                else :
                    # Pour aller à gauche
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[(Robot_Y.value-1)%taille_grille][Robot_X.value] = Case.Blank.value,Case.Robot.value
            
            # Direction : Vers la Gauche
            if Direction_Robot.value == Direction.Right.value:
                if mem_Cmd.value == Cmd.Front.value:
                    # Pour aller tout droit
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[Robot_Y.value][(Robot_X.value-1)%taille_grille] = Case.Blank.value,Case.Robot.value
                if mem_Cmd.value == Cmd.Left.value:
                    # Pour aller à droite
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[(Robot_Y.value-1)%taille_grille][Robot_X.value] = Case.Blank.value,Case.Robot.value
                else :
                    # Pour aller à gauche
                    grille_loc[Robot_Y.value][Robot_X.value],grille_loc[(Robot_Y.value+1)%taille_grille][Robot_X.value] = Case.Blank.value,Case.Robot.value
            
            Verrou.release()

            effacer_ecran()
            print(grille_loc)


# Permet de rechercher la position du robot dans la grille
def position_robot():
    while True:
        grille = sa.attach("shm://grille")
        for ligne in range(0,taille_grille):
            for colonne in range(0,taille_grille):
                if grille[ligne][colonne] == Case.Robot.value:
                    Verrou_Position.acquire()
                    Robot_X.value = colonne
                    Robot_Y.value = ligne
                    Verrou_Position.release()

# Permet la gestion des capteurs (Left & Right)
def ir():
    tic = time.time()
    while True :
        # Pour le faire toutes les temps_Ir secondes
        if (tic-time.time())%temps_Ir.value == 0:
            grille = sa.attach("shm://grille")
            # Différents cas pour chacune des directions possibles du robot :
            # Direction : Vers le Haut
            if Direction_Robot.value == Direction.Up.value:
                # Capteur gauche                                                        # Capteur Droit :
                if grille[(Robot_Y.value-1)%taille_grille][Robot_X.value] == Case.Obstacle.value or grille[(Robot_Y.value+1)%taille_grille][Robot_X.value] == Case.Obstacle.value:
                    Flag_IR.value = True
                    if grille[(Robot_Y.value-1)%taille_grille][Robot_X.value] == Case.Obstacle.value and grille[(Robot_Y.value+1)%taille_grille][Robot_X.value] == Case.Obstacle.value:
                        Cmd_IR.value = Cmd.Back.value
                    elif grille[(Robot_Y.value-1)%taille_grille][Robot_X.value] == Case.Obstacle.value :
                        Cmd_IR.value = Cmd.Left.value
                    else:
                        Cmd_IR.value = Cmd.Right.value
                else:
                    Flag_IR.value = False
            # DIrection : Vers le Bas
            if Direction_Robot.value == Direction.Down.value:
                # Capteur gauche                                                        # Capteur Droit :
                if grille[(Robot_Y.value+1)%taille_grille][Robot_X.value] == Case.Obstacle.value or grille[Robot_Y.value-1][Robot_X.value] == Case.Obstacle.value:
                    Flag_IR.value = True
                    if grille[(Robot_Y.value+1)%taille_grille][Robot_X.value] == Case.Obstacle.value and grille[(Robot_Y.value-1)%taille_grille][Robot_X.value] == Case.Obstacle.value:
                        Cmd_IR.value = Cmd.Back.value
                    elif grille[(Robot_Y.value+1)%taille_grille][Robot_X.value] == Case.Obstacle.value :
                        Cmd_IR.value = Cmd.Left.value
                    else:
                        Cmd_IR.value = Cmd.Right.value
                else:
                    Flag_IR.value = False
            # Direction : Vers la Gauche
            if Direction_Robot.value == Direction.Left.value:
                # Capteur gauche                                                        # Capteur Droit :
                if grille[Robot_Y.value][(Robot_X.value+1)%taille_grille] == Case.Obstacle.value or grille[Robot_Y.value][(Robot_X.value-1)%taille_grille] == Case.Obstacle.value:
                    Flag_IR.value = True
                    if grille[Robot_Y.value][(Robot_X.value+1)%taille_grille] == Case.Obstacle.value and grille[Robot_Y.value][(Robot_X.value-1)%taille_grille] == Case.Obstacle.value:
                        Cmd_IR.value = Cmd.Back.value
                    elif grille[Robot_Y.value][(Robot_X.value+1)%taille_grille] == Case.Obstacle.value :
                        Cmd_IR.value = Cmd.Left.value
                    else:
                        Cmd_IR.value = Cmd.Right.value
                else:
                    Flag_IR.value = False
            # Direction : Vers la Droite
            if Direction_Robot.value == Direction.Right.value:
                # Capteur gauche                                                        # Capteur Droit :
                if grille[Robot_Y.value][(Robot_X.value-1)%taille_grille] == Case.Obstacle.value or grille[Robot_Y.value][(Robot_X.value+1)%taille_grille] == Case.Obstacle.value:
                    Flag_IR.value = True
                    if grille[Robot_Y.value][(Robot_X.value-1)%taille_grille] == Case.Obstacle.value and grille[Robot_Y.value][(Robot_X.value+1)%taille_grille] == Case.Obstacle.value:
                        Cmd_IR.value = Cmd.Back.value
                    elif grille[Robot_Y.value][(Robot_X.value-1)%taille_grille] == Case.Obstacle.value :
                        Cmd_IR.value = Cmd.Left.value
                    else:
                        Cmd_IR.value = Cmd.Right.value
                else:
                    Flag_IR.value = False

# Permet la gestion du capteur (US = Front)
def us():
    tic = time.time()
    while True:
        # Pour le faire toutes les temps_Ecran secondes
        if (tic-time.time())%temps_US.value == 0:
            grille = sa.attach("shm://grille")
            # Différents cas pour chacune des directions possibles du robot :
            # Direction : Vers le Haut
            if Direction_Robot.value == Direction.Up.value:
                if grille[(Robot_Y.value-1)%taille_grille][Robot_X.value] == Case.Obstacle.value:
                    Flag_US.value = True
                    Cmd_US.value = Cmd.Back.value
                else:
                    Flag_US.value = False
            # DIrection : Vers le Bas
            if Direction_Robot.value == Direction.Down.value:
                if grille[(Robot_Y.value+1)%taille_grille][Robot_X.value] == Case.Obstacle.value:
                    Flag_US.value = True
                    Cmd_US.value = Cmd.Back.value
                else:
                    Flag_US.value = False
                
            # Direction : Vers la Gauche
            if Direction_Robot.value == Direction.Left.value:
                if grille[Robot_Y.value][(Robot_X.value-1)%taille_grille] == Case.Obstacle.value:
                    Flag_US.value = True
                    Cmd_US.value = Cmd.Back.value
                else:
                    Flag_US.value = False
                
            # Direction : Vers la Droite
            if Direction_Robot.value == Direction.Right.value:
                if grille[Robot_Y.value][(Robot_X.value+1)%taille_grille] == Case.Obstacle.value:
                    Flag_US.value = True
                    Cmd_US.value = Cmd.Back.value
                else:
                    Flag_US.value = False

# Permet la gestion du contact en front
def bumper():
    tic = time.time()
    while True:
        # Pour le faire toutes les temps_Ecran secondes
        if (tic-time.time())%temps_BU.value == 0:
            if grille[Robot_Y.value][Robot_X.value] == Case.Obstacle.value:
                Flag_BU.value = True
                Cmd_BU.value = Cmd.Back.value
            else:
                Flag_BU.value = False

#------------------------------------------------
if __name__ == "__main__" :

    # Déclaration des différentes Variables :
    
    Verrou = Lock()
    Verrou_Position = Lock()
    Verrou_memory = Lock()
    # Position du robot :
    Robot_X = Value('i',0)
    Robot_Y = Value('i',0)
    # Direction du Robot :
    Direction_Robot = Value('i',0)
    # Les différentes distances :
    Dist_Front = Value('d',0.0)
    Dist_Left = Value('d',0.0)
    Dist_Right = Value('d',0.0)
    # Les différents drapeaux :
    Flag_IR = Value('b',False)
    Flag_US = Value('b',False)
    Flag_BU = Value('b',False)
    # Les commandes provenant des capteurs :
    Cmd_IR = Value('i',0)
    Cmd_US = Value('i',0)
    Cmd_BU = Value('i',0)
    # Les mémoires partagées :
    mem_Cmd = Value('i',0)  # Commande à transmettre
    mem_Flag = Value('i',0)  # Flag à transmettre
    
    taille_grille = 5
    # while taille_grille == 0:
    #     try :
    #         taille_grille = int(input("Taille de la grille carrée : "))
    #     except ValueError:
    #         print("Saisir un entier !! ")
    
    Process_Ecran = Process(target=ecran, args=(taille_grille,))
    Process_position = Process(target=position_robot)
    Process_IR = Process(target=ir)
    Process_US = Process(target=us)
    Process_BU = Process(target=bumper)
    Process_Controleur = Process(target=controleur)

    Process_Ecran.start()
    Process_position.start()
    Process_Controleur.start()
    Process_US.start()
    Process_IR.start()
    Process_BU.start()