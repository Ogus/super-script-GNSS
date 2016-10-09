# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 18:01:51 2014

@author: beilin
"""
# 2. Programmation plus avancée

# 2.1 Latitude isométrique

import math 
import numpy as np

e_grs80 = 0.081819191043
    
def lat2latiso(phi, e=e_grs80):
    # Ce programme permet de calculer la latitude isometrique d'un point
    #
    # Usage : lat2latiso(phi)
    # Entrees
    # 	phi : latitude en radian
    #
    # Sorties
    # 	L   : latitude isometrique
    #

    L = (math.log(math.tan(math.pi/4 + phi/2))) - e / 2 * math.log ((1+e*math.sin(phi))/(1-e*math.sin(phi)))
    return L
    
def lat2latiso_list(phi, e=e_grs80):
    """
     Calcul de la latitude isometrique d'un point
    
     Usage : lat2latiso(phi)
     Entrees
     	phi : latitude en radian
      e : excentricité de l'ellipsoïde (par défaut GRS80)
    
     Sorties
     	L   : latitude isometrique
    """
    
    return (np.log(np.tan(np.pi/4 + phi/2))) - e / 2 * np.log ((1+e*np.sin(phi))/(1-e*np.sin(phi)))

    
def  latiso2lat(L, e=e_grs80):
    """Calcul de la latitude d'un point à partir de sa latitude isometrique
    
     Usage : p = latiso2lat(L)
      Entrees
           L   : latitude isometrique
           e : excentricité de l'ellipsoïde (par défaut GRS80)
    
      Sorties
           phi : latitude en radian
    """

    # initialisation du calcul (cas spherique)
    max_iter = 20
    Vphi = np.zeros(max_iter)
    Vphi[0] = 2 * math.atan(math.exp(L)) - math.pi/2
    
    # critère de convergence : au minimum 1e-8 gon soit 1mm sur terre
    # Pour éviter les problèmes d'arrondi on va jusqu'à 1e-12 gons
    epsilon = 1e-12 * math.pi / 200
    
    for i in range(1,max_iter):
        Vphi[i] = 2*math.atan(((1+e*math.sin(Vphi[i-1]))/(1-e*math.sin(Vphi[i-1])))**(0.5*e)*math.exp(L))-math.pi/2    

        if (abs(Vphi[i]-Vphi[i-1])<epsilon): 
            phi = Vphi[i]
            Vphi=Vphi[:i+1]
            break
    
    return phi


def  latiso2lat_list(L, e=e_grs80):
# Calcul de la latitude d'un point à partir de sa latitude isometrique
#
# Usage : p = latiso2lat(L)
#  Entrees
#       L   : latitude isometrique
#
#  Sorties
#       phi : latitude en radian
#

    # initialisation du calcul (cas spherique)
    max_iter = 20
    # critère de convergence : au minimum 1e-8 gon soit 1mm sur terre
    # Pour éviter les problèmes d'arrondi on va jusqu'à 1e-12 gons
    epsilon = 1e-12 * math.pi / 200
    
    rphi = np.zeros(L.shape)
    for j in range(len(L)):    
        Vphi = np.zeros(max_iter)
        Vphi[0] = 2 * math.atan(math.exp(L[j])) - math.pi/2
      
        for i in range(1,max_iter):
            Vphi[i] = 2*math.atan(((1+e*math.sin(Vphi[i-1]))/(1-e*math.sin(Vphi[i-1])))**(0.5*e)*math.exp(L[j]))-math.pi/2    
    
            if (abs(Vphi[i]-Vphi[i-1])<epsilon): 
                phi = Vphi[i]
                Vphi=Vphi[:i+1]
                break
        rphi[j]=phi
    
    return rphi

if __name__ == "__main__":
    
    d2r = math.pi / 180
    phi = np.array([45*d2r,60*d2r])

    L = lat2latiso_list(phi)
    print(L)
    
    p = latiso2lat_list(L)
    print(p*180/np.pi)