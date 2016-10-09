# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 12:01:25 2016

@author: gus
"""

import math
import numpy as np
import script.lambert as lb

class Converter(object):
    """
    Permet de tranformer des coordonnées entre les systèmes suivants:
        - géographiques   (L,l,h)
        - planes (E,N,h)
        - cartésiennes  (X,Y,Z)
    La transformation de coordonnées utilisation une projection Lambert 93
    """
    
    def __init__(self,lambert="L93"):
        """Initialise la projection Lambert
        Options:
            - Lambert 93
            - CC42 -> CC50  (Conique Conforme 42 à 50)
            - Lambert 1 à Lambert 4
            - Lambert 2_e  (Lambert 2 étendu)
        """
        self.a = 6378137.0      # IAG GRS80 constants
        self.e2 = 0.006694380022
        self.lamb = lb.Lambert
        self.set_projection(lambert)
             
             
    def set_projection(self,lambert):
        """
        Construit l'instance de la classe Lambert utilisé pour la projection
        """
        a_grs80 = 6378137.0
        e_grs80 = 0.081819191043
        a_clarke80 = 6378249.2
        b_clarke80 = 6356515.0
        e2_clarke80 = (a_clarke80**2 - b_clarke80**2) / a_clarke80**2
        e_clarke80 = math.sqrt(e2_clarke80)
        d2r = math.pi / 180
        g2r = math.pi / 200
        
        if(lambert == "Lambert 93"):
            self.lamb = lb.Lambert_secant()
            self.lamb.set_constantes_definition('Lambert93',700000,6600000,44*d2r,49*d2r,46.5*d2r,3*d2r,a_grs80,e_grs80)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "CC42"):
            self.lamb = lb.Lambert_secant()
            self.lamb.set_CC(42)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "CC43"):
            self.lamb = lb.Lambert_secant()
            self.lamb.set_CC(43)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "CC44"):
            self.lamb = lb.Lambert_secant()
            self.lamb.set_CC(44)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "CC45"):
            self.lamb = lb.Lambert_secant()
            self.lamb.set_CC(45)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "CC46"):
            self.lamb = lb.Lambert_secant()
            self.lamb.set_CC(46)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "CC47"):
            self.lamb = lb.Lambert_secant()
            self.lamb.set_CC(47)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "CC48"):
            self.lamb = lb.Lambert_secant()
            self.lamb.set_CC(48)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "CC49"):
            self.lamb = lb.Lambert_secant()
            self.lamb.set_CC(49)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "CC50"):
            self.lamb = lb.Lambert_secant()
            self.lamb.set_CC(50)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "Lambert 1"):
            self.lamb = lb.Lambert_tangentk0()
            self.lamb.set_constantes_definition('Lambert I',600000, 200000, 55*g2r, 0.99987734, 0*g2r, a_clarke80, e_clarke80,53.5*g2r,57*g2r)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "Lambert 2"):
            self.lamb = lb.Lambert_tangentk0()
            self.lamb.set_constantes_definition('Lambert II',600000, 200000, 52*g2r, 0.99987742, 0*g2r, a_clarke80, e_clarke80,50.5*g2r,53.5*g2r)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "Lambert 2_e"):    
            self.lamb = lb.Lambert_tangentk0()
            self.lamb.set_constantes_definition('Lambert II étendu',600000, 2200000, 52*g2r, 0.99987742, 0*g2r, a_clarke80, e_clarke80)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "Lambert 3"):
            self.lamb = lb.Lambert_tangentk0()
            self.lamb.set_constantes_definition('Lambert III',600000, 200000, 49*g2r, 0.99987750, 0*g2r, a_clarke80, e_clarke80,47*g2r,50.5*g2r)
            self.lamb.calc_constantes_derivees()
        elif(lambert == "Lambert 4"):
            self.lamb = lb.Lambert_tangentk0()
            self.lamb.set_constantes_definition('Lambert IV',234.358, 185861.369, 46.85*g2r, 0.99994471, 0*g2r, a_clarke80, e_clarke80,45.9*g2r,47.8*g2r)
            self.lamb.calc_constantes_derivees()
        else:
            print("Parameter not valid: lambert \n Default value: Lambert 93")
            self.lamb = lb.Lambert_secant()
            self.lamb.set_constantes_definition('Lambert93',700000,6600000,44*d2r,49*d2r,46.5*d2r,3*d2r,a_grs80,e_grs80)
            self.lamb.calc_constantes_derivees()
            
    
    def cart_to_geo(self,X,Y,Z):
        """
        Conversion de coordonées cartésiennes à géographiques
        
        Arguments : 
            - X, Y, Z : coordonnées cartésiennes
        """
        
        f = 1 - math.sqrt(1-self.e2)
        
        rxy = math.sqrt(X**2 + Y**2)
        r = math.sqrt(X**2 + Y**2 + Z**2)
        mu = math.atan((Z/rxy)*((1-f) + self.a*self.e2/r))
        
        num = Z*(1-f) + self.e2*self.a *(math.sin(mu))**3
        denum = (1-f) * (rxy-self.a * self.e2 * (math.cos(mu))**3)
        lat = math.atan(num/denum)
        
        lon = 2 * math.atan(Y/(X+rxy))
        
        w = math.sqrt(1 - self.e2*math.sin(lat)**2)
        h = rxy*math.cos(lat) + Z*math.sin(lat) - self.a*w
        
        return lon,lat,h


    def geo_to_cart(self,lon,lat,h):
        """
        Conversion de coordonées géographiques à cartésiennes

        Arguments :
            - lon : longitude (rad)
            - lat : latitude (rad)
            - h : hauteur (m)
        """

        N = self.a / math.sqrt(1.0 - self.e2*(math.sin(lat))**2)        # angles in rad
        X = (N+h) * (math.cos(lon)) * (math.cos(lat))
        Y = (N+h) * (math.sin(lon)) * (math.cos(lat))
        Z = (N*(1-self.e2) + h) * (math.sin(lat))
	
        return X,Y,Z
        
        
    def EN_to_geo(self,E,N,h):
        """
        Conversion de coordonées planimétriques à géographiques
        
        Arguments : 
            - E, N : coordonnées planimétriques
            - h: hauteur
        """
        result = self.lamb.EN2geo(E,N)
        
        return result[0],result[1],h
        
        
    def geo_to_EN(self,lon,lat,h):
        """
        Conversion de coordonées géographiques à planimétriques

        Arguments :
            - lon : longitude (rad)
            - lat : latitude (rad)
            - h : hauteur (m)
        """
        result = self.lamb.geo2EN(lon,lat)
        
        return result[0],result[1],h
            
            
    def EN_to_cart(self,E,N,h):
        """
        Conversion de coordonées cartésiennes à cartésiennes
        
        Arguments : 
            - E, N : coordonnées planimétriques
            - h: hauteur
        """
        temp = self.EN_to_geo(E,N,h)
        result = self.geo_to_cart(temp[0],temp[1],temp[2])
        
        return result
        
    
    def cart_to_EN(self,X,Y,Z):
        """
        Conversion de coordonées cartésiennes à planiétriques
        
        Arguments : 
            - X, Y, Z : coordonnées cartésiennes
        """
        temp = self.cart_to_geo(X,Y,Z)
        result = self.geo_to_EN(temp[0],temp[1],temp[2])
        
        return result
            
   
    def rad_to_deg(self,r):
        return (r*180 / np.pi) % 360
        
        
    def deg_to_rad(self,d):
        return (d*np.pi / 180) % 2*np.pi
