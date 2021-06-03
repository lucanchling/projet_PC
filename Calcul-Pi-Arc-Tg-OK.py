# Calcul de PI par la loi Normale
import multiprocessing as mp
import random, time
# calculer le nbr de hits dans un cercle unitaire (utilisé par les différentes méthodes)
start_time = time.time()
from math import *
 
def arc_tangente(n):
    pi = 0
    for i in range(n):
        pi += 4/(1+ ((i+0.5)/n)**2)
    return (1/n)*pi


def chacun_chez_soi(numero,iteration,nombre_proc,integrale):
    ma_part=0
    for j in range(0,iteration,nombre_proc):
        ma_part+=4/(1+((j+0.5)/iteration)**2)
    integrale[numero]=(1/iteration)*ma_part
    

if __name__ == "__main__" :
    # Nombre d’essai pour l’estimation
    iteration = 1000000
    nombre_proc=4
    integrale=mp.Array('f',nombre_proc)
    tab_pid=[0 for i in range (nombre_proc)]
    for i in range (nombre_proc):
        tab_pid[i]=mp.Process(target=chacun_chez_soi,args=(numero,iteration,nombre_proc,integrale))
        tab_pid[i].start()
    for i in range (nombre_proc):
        tab_pid[i].join()
    
    resultat=
    #nb_hits=frequence_de_hits_pour_n_essais(nb_total_iteration)
    #result = arc_tangente(nb_total_iteration)
    
    print("Valeur estimée Pi par la méthode Tangente : ", result)
    print("Temps d'execution : ", time.time() - start_time)



