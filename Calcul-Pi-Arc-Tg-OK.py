# Calcul de PI par la loi Normale
import multiprocessing as mp
import random, time
# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
start_time = time.time()
from math import *

#fonction permettant de calculer pi en séquentielle pas utile puisque nous utilisons les process
"""def arc_tangente(n):                                      
    pi = 0
    for i in range(n):
        pi += 4/(1+ ((i+0.5)/n)**2)
    return (1/n)*pi"""

#cette fonction est associée aux processus fils qui vont effectuer chacun une partie de calcul en parallèle
#numero correspond au numéro du processus fils, iteration au nombre d'iteration, nombre_proc est le nombre de process fils, integrale est un tableau partagée qui nous permet de recupérer les valeurs des sommes locales de chaque fils
def chacun_chez_soi(numero,iteration,nombre_proc,integrale):    
    ma_part=0                                                           #on initialise la somme local 
    for j in range(0,iteration,nombre_proc):                            #on calcule ensuite la somme, j+0.5 nous permet de se considérer au milieu des bâtons, on prend un pas de nombre_proc pour équilibrer plus équitablement
        ma_part+=4/(1+(((j+0.5)/iteration)**2))
    integrale[numero]=(1/iteration)*ma_part                             #on pense bien à diviser par le nombre d'itérations, puis on le stocke dans le tableau integrale
    

if __name__ == "__main__" :
    # Nombre d’essai pour l’estimation
    iteration = 1000000
    nombre_proc=4
    resultat=0                                                          #somme globale finale, résultat de pi
    integrale=mp.Array('f',[0 for i in range(nombre_proc)])             #création du tableau partagé par tous les fils 
    num=mp.Array('i',[i for i in range(nombre_proc)])                   #ce tableau permet par la suite de donner un numéro à chaque fils en train de calculer
    
    
    tab_pid=[0 for i in range (nombre_proc)]
    for i in range (nombre_proc):
        tab_pid[i]=mp.Process(target=chacun_chez_soi,args=(i,iteration,nombre_proc,integrale))   #ici je créé mes fils en fonction du nombre de processus qu'on veut utiliser
        tab_pid[i].start()
    for i in range (nombre_proc):
        tab_pid[i].join()
    for i in range(nombre_proc):                                                                 #On calcule ici la somme globale finale en sommant les résultats de chaque process
        resultat+=integrale[i]

    #nb_hits=frequence_de_hits_pour_n_essais(nb_total_iteration)
    #result = arc_tangente(iteration)
    
    print("Valeur estimée Pi par la méthode Tangente : ", resultat)                              #on affiche le résultat final de pi
    #print("Valeur estimée Pi par la méthode Tangente : ", result)  
    print("Temps d'execution : ", time.time() - start_time)                                      #on affiche le temps d'execution



