# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:49:00 2016

@author: Amaury
"""

import numpy as np
import numpy.linalg as lina
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import script.utility as utl

    
def residus_norm(A,B,X):
    """
    Calcul des résidus d'une estimation par moindre carrés
    
    Arguments:
        - A: matrice modèle
        - B: matrice des observation
        - X: matrice résultat
    """
    V = B - np.dot(A,X)         #vecteur résidus
    res_norm = B - np.dot(A,X)
    
    n = len(B)
    p = len(X)
    sigma = np.dot(V.T,V) / (n-p)       #facteur unitaire de variance
    
    N = np.dot(A.T, A)
    N_ = lina.inv(N)
    P = np.eye(n,n)
    P_ = lina.inv(P)
    res_v = sigma * (P_ - np.dot(np.dot(A,N_), A.T))       #résidus du vecteur des résidus
    
    for i in range(len(res_v)):         #normalisation des résidus
        res_norm[i] /= np.sqrt(res_v[i,i])
    return res_norm,V

def lst_square(fname):
    """
    Effectue une régression linéaire d'un ensemble de points en coordonnées planimétriques
    afin de calculer un plan moyen à l'ensemble des hauteurs observées
    La liste des points sont directement issus d'un fichier csv, les matrices modèles et d'observations
    sont automatiquement calculées
    
    Arguments:
        - fname: nom du fichier csv utilisé pour extraire les données
    """
    donnees = utl.read_csv(fname)           #récupération des données du fichier
    utl.redux(*donnees[:4])
    
    B=np.array(donnees[3]).T        #la matrice d'observation contient les hauteurs terrains
    
    les_x=np.array(donnees[1])
    les_y=np.array(donnees[2])
    les_uns=np.ones(np.shape(les_y))
    
    A=np.array([les_x,les_y,les_uns]).T         #la matrice modèle contient les coordonnées Est et Nord
    
    X = lina.lstsq(A,B)[0]          #moindre carré magiques par invocation du module Python
    
    res_norm,residus = residus_norm(A,B,X)      #calcul des résidus et résidus normalisés
    
    std,e = calc_stats(residus)         #calcul de l'écart type et de la différence maximale
    
    return X,res_norm,std,e
    
        
def calc_stats(serie):
    """
    Calculs statistiques sur des résidus de moindre carré
    """
    n = len(serie)
#    m = np.mean(residus)
    
    var = 0                 #calcul de l'écart-type des résidus
    for i in range(len(serie)):
        var += (serie[i])**2
    result = np.sqrt(var/n)
    
    mx = np.max(serie)            #calcul de la valeur crête à crête
    mn = np.min(serie)
    ecart = mx-mn
    
    return result,ecart
    
    
    
def draw(data,X,residus):
    """
    Affiche dans une même fenêtre deux graphiques: un pour la représentation en 3D des points de données
    et du plan moyen, et l'autre pour les résidus normalisés de l'estimation par moindre carré
    
    Arguments:
        - data: liste de valeurs
        - x: liste au format [a,b,c] qui représente l'équation du plan
        - résidus: vecteur des résidus
    """
    E = data[1]
    N = data[2]
    h = data[3]
    
    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_xlabel('Est')
    ax1.set_ylabel('Nord')
    ax1.set_zlabel('Hauteur')
    ax1.plot(E,N,h)                 #affiche les données
    ax1.plot(E,N,func([E,N],*X))    #affiche les points selon l'estimation X
    
    ax2 = fig.add_subplot(122)
    ax2.hist(residus,20)            #ffiche les résidus
    ax2.set_xlabel('Valeur des résidus')
    ax2.set_ylabel('Fréquence')
    
    plt.show()
    
    
def func(x,a,b,c):
    """
    Cette fonction calcul le plan d'équation z = ax + by + c, pour tout les points (x,y)
    
    Arguments:
        - x: liste des coordonnées planimétriques, au format x = [[e1,e2...],[n1,n2,...]]
        - a,b,c: paramètres du plan
    """
    result = []
    for i in range(len(x[0])):
        result.append(a*x[0][i] + b*x[1][i] + c)
    return result
    
