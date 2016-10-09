# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 09:56:47 2016

@author: ogustin
"""
import numpy as np

"""
Ce script permet de convertir les fichiers txt obtenus par CloudCompare 
en fichier csv lisible par le super script GNSS

Il ne faut l'utiliser que sur des fichiers de points généré automatiquement par CLoudCompare
"""

def convert(filename,output):
    """
    Fonction de conversion de fichier
    Argument:
        -filename: nom du fichier d'entrée (.txt)
        -putput: nom du fichier de sortie (.csv)
    """
    in_file = open(filename,'r')
    out_file = open(output,'w')
    
    lines = in_file.readlines()
    out_file.write('Seconde,Est,Nord,Hauteur,Vitesse,Vitesse_p,Vitesse_a,Acceleration\n')
    
    t = []
    E = []
    N = []
    h = []
    v = []
    v_plani = []
    v_alti = []
    a = []
    
    for l in lines:         #affectation des valeurs présentent dans le fichier texte
        temp = l.split(",")
        E.append(float(temp[0]))
        N.append(float(temp[1]))
        h.append(float(temp[2]))
        t.append(float(temp[3]))
        
    m = np.min(t)
    for i in range(len(t)): t[i] -= m
    
    v.append(0)             #calcul des valeurs de vitesses et d'accélération
    v_plani.append(0)
    v_alti.append(0)
    for j in range(1,len(E)):
        dist = np.sqrt( (E[j]-E[j-1])**2 + (N[j]-N[j-1])**2 + (h[j]-h[j-1])**2 )
        dist_plani = np.sqrt( (E[j]-E[j-1])**2 + (N[j]-N[j-1])**2 )
        dist_alti = np.sqrt( (h[j]-h[j-1])**2 )
        
        v.append(dist/(t[j]-t[j-1]))
        v_plani.append(dist_plani/(t[j]-t[j-1]))
        v_alti.append(dist_alti/(t[j]-t[j-1]))
        
    a.append(0)
    for k in range(1,len(v)):
        a.append((v[k]-v[k-1])/(t[k]-t[k-1]))
        
    for i in range(len(t)):
        out_file.write(str(t[i])+","+str(E[i])+","+str(N[i])+","+str(h[i])+","+str(v[i])+","+str(v_plani[i])+","+str(v_alti[i])+","+str(a[i])+"\n")
        
        
        
#convert('data/txt/tst_bon_aller.txt','data/csv/tst_bon_aller.csv')
#convert('data/txt/tst_bon_retour.txt','data/csv/tst_bon_retour.csv')
#convert('data/txt/tst_mauvais_aller.txt','data/csv/tst_mauvais_aller.csv')
#convert('data/txt/tst_mauvais_retour.txt','data/csv/tst_mauvais_retour.csv')