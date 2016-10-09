# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 10:37:20 2016

@author: ogustin
"""
import numpy as np
import script.convert as cv


def convert_time(line):
    """
    Convertis le temps au format hh:mm:ss,sss en nombre de seconde depuis 00h00
    """
    h = float(line[0:2])
    m = float(line[3:5])
    s = float(line[6:])
    return h*3600 + m*60 + s

def read_file(filename,q=1):
    """
    Récupère un fichier au format .pos calculés avec rtklib et retourne les données des points
    
    Arguments:
        - filename: nom du fichier .pos à convertir
        - q : qualité des points à récupérer, par défaut q = 1  (optionnel)
    """
    result = []
    file = open(filename,'r')
    line = file.readline()
    
    while(len(line) > 1):       #parcours toute les lignes du fichier d'entré
        if(line[0] != "%"):
            temp = line.split()
            if(int(temp[5]) <= q):
                time = convert_time(temp[1])
                x = float(temp[2])
                y = float(temp[3])
                z = float(temp[4])
                result.append([time,x,y,z])         #ajoute les données de chaque ligne au résultat final
        
        line = file.readline()
    
    file.close()
    return result
    
    
    
def extract_data(filename,lambert,q=1):
    """
    Récupère un fichier de points calculés avec rtklib, puis convertis les coordonnées de chaque point
    en projection Lambert et calcul des valeurs supplémentaires (vitesse, vitesse planimétrique, etc.)
    
    Arguments:
        - filename: nom du fichier .pos à convertir
        - lambert: type de projection Lambert à utiliser (cf. module Lambert)
        - q : qualité des points à récupérer, par défaut q = 1  (optionnel)
    """
    temp = read_file(filename,q)
    convert = cv.Converter(lambert)
    t = []
    E = []
    N = []
    h = []
    v = []
    v_plani = []
    v_alti = []
    a=[]
    
    for point in temp:      #convertis les coordonnées
        t.append(point[0])
        r = convert.cart_to_EN(point[1],point[2],point[3])
        E.append(r[0])
        N.append(r[1])
        h.append(r[2])
        
    m = np.min(t)      #modifie l'échele de temps pour qu'lle commence à 0
    for i in range(len(t)): t[i] -= m
    
    v.append(0)
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
        
    return [t,E,N,h,v,v_plani,v_alti,a]
    
    

def create_csv(data,output="toto.csv"):
    """
    Permet de sauvegarder les données calculés à partir d'un fichier pos dans un fichier au format csv
    Le fichier de sortie peut ensuite être utilisé et modifié avec le super script, ou un SIG
    
    Arguments:
        - data: liste de valeurs au format [t,E,N,h,v,v_plani,v_alti,a]
        - output: le nom du fichier de sortie
    """
    file = open(output,'w')
    
    file.write("Seconde,Est,Nord,Hauteur,Vitesse,Vitesse_p,Vitesse_a,Acceleration\n")
    for i in range(len(data[0])-2):
        file.write(str(data[0][i])+","+str(data[1][i])+","+str(data[2][i])+","+str(data[3][i])+","+str(data[4][i])+","+str(data[5][i])+","+str(data[6][i])+","+str(data[7][i])+"\n")

    file.close()
    
def read_csv(filename):
    """
    Récupère les données des points contenus dans un fichier csv
    """
    file = open(filename,'r')
    t = []
    E = []
    N = []
    h = []
    v = []
    v_plani = []
    v_alti = []
    a = []
    lines = file.readlines()
    i = 0
    for l in lines:
        i += 1
        temp = l.split(",")
        if(l[0] != "S"):
            t.append(float(temp[0]))
            E.append(float(temp[1]))
            N.append(float(temp[2]))
            h.append(float(temp[3]))
            v.append(float(temp[4]))
            v_plani.append(float(temp[5]))
            v_alti.append(float(temp[6]))
            a.append(float(temp[7]))
    
    file.close()
    return [t,E,N,h,v,v_plani,v_alti,a]
    
def cut_csv(output,data,start,stop):
    """
    Récupère un extrait d'une série de données selon un intervalle de temps, et le réecrit dans un autre fichier
    
    Argument:
        - output: nom du fichier de sortie
        - data: liste de liste de valeurs au format [t,E,N,h,v,v_plani,v_alti,a] d'où extraire les données
        - start: début de l'intervalle de temps
        - stop: fin de l'intervalle de temps
    """
    file = open(output,'w')
    file.write("Seconde,Est,Nord,Hauteur,Vitesse,Vitesse_p,Vitesse_a,Acceleration\n")
    
    for i in range(len(data[0])):
        if(data[0][i] >= start and data[0][i] <= stop):
            file.write(str(data[0][i])+","+str(data[1][i])+","+str(data[2][i])+","+str(data[3][i])+","+str(data[4][i])+","+str(data[5][i])+","+str(data[6][i])+","+str(data[7][i])+"\n")
            
    file.close()
    
    
    
def redux(t,E,N,h):
    """
    Cette donction permet de moyenner les coordonnées planimétriques afin de les centrer en 0
    """
    m1 = np.min(t)
    m2 = np.mean(E)
    m3 = np.mean(N)
    m4 = np.mean(h)
    for i in range(len(t)):
        t[i] -= m1
        E[i] -= m2
        N[i] -= m3
        h[i] -= m4

