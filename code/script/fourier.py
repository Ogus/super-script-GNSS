# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 08:57:45 2016

@author: Amaury
"""

import scipy.fftpack as fft
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import script.utility as utl


def fourier(fname,attr,rot=False):
    """
    Effectue l'analyse de Fourier d'un fichier de points, selon l'attributs considéré
    
    Argument:
        - fname: nom du fichier csv
        - attr: indice de l'attribut à analyser dans les colonnes du fichier csv
            (0: Est, 1: Nord, 2: hauteur, etc.)
    """
    
    donnees = utl.read_csv(fname)
    utl.redux(*donnees[:4])
    
    
    if(rot):        #effectue la rotation du nuage de points vers un plan moyen        
        
#        R_e = [[1.,0,0],
#               [0,np.cos(alpha),-np.sin(alpha)],
#               [0,np.sin(alpha),np.cos(alpha)]]
#               
#        R_n = [[np.cos(beta),0,np.sin(beta)],
#               [0,1.,0],
#               [-np.sin(beta),0,np.cos(beta)]]
              
        alpha = -np.arctan( (donnees[3][-1] - donnees[3][0])/(donnees[1][-1] - donnees[1][0]) )      #H/E
        for i in range(len(donnees[0])):
            x = donnees[1][i] - donnees[1][0]
            y = donnees[2][i] - donnees[2][0]
            z = donnees[3][i] - donnees[3][0]
#            temp = [[donnees[1][i]],[y],[z]]
#            result = np.dot(np.dot(R_n,R_e),temp)
#            result = np.dot(R_e,temp)
            donnees[1][i] = donnees[1][0] + np.cos(alpha)*x - np.sin(alpha)*z
            donnees[2][i] = donnees[2][0] + y
            donnees[3][i] = donnees[3][0] + np.sin(alpha)*x + np.cos(alpha)*z
            
        alpha = -np.arctan( (donnees[3][-1] - donnees[3][0])/(donnees[2][-1] - donnees[2][0]) )      #H/N
        for i in range(1,len(donnees[0])):
            x = donnees[1][i] - donnees[1][0]
            y = donnees[2][i] - donnees[2][0]
            z = donnees[3][i] - donnees[3][0]
            donnees[1][i] = donnees[1][0] + x
            donnees[2][i] = donnees[2][0] + np.cos(alpha)*y - np.sin(alpha)*z
            donnees[3][i] = np.sin(alpha)*y + np.cos(alpha)*z
            
        donnees[3][0] = 0
    
    liste_hauteurs=donnees[attr+1]      #récupère la colonne voulue
#    m = np.mean(liste_hauteurs)
#    for i in range(len(liste_hauteurs)): liste_hauteurs[i] -= m         #recentre les valeurs autour de 0
    
    liste_temps=donnees[0]
    
    fourier=fft.fft(liste_hauteurs)/np.size(liste_hauteurs)
    axe_f=np.arange(0.,len(liste_hauteurs))*20/len(liste_hauteurs)
    
    
    plt.figure()            #initialise le graphique
    plt.subplot(121)
    plt.plot(liste_temps,liste_hauteurs,'-')        #affiche l'attribut en fonction du temps
    plt.xlabel('axe temporel')
    plt.subplot(122)
    plt.plot(axe_f,np.abs(fourier),'x-')            #affiche l'analyse de Fourier
    plt.xlabel('axe frequentiel')
    plt.xlim(xmax=10)
    plt.show()
    
#    fname.close()