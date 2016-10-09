# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 16:19:17 2014

@author: beilin
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import script.latitude_iso as Li

d2r = math.pi / 180
g2r = math.pi / 200

class Lambert():
    """
    
    """
    def __init__(self):
        pass
    
    def print(self):
       for s in self.__dict__:
            print('%-35s : ' % (s), self.__dict__.get(s))  
    
    def geo2EN(self,lon,lat):
        """Transform geographic to planimetric coordinates"""
        L = Li.lat2latiso(lat,self.e)
        R = self.C * np.exp(-self.n * L)
        gamma = self.n*(lon-self.lambda0)
        X = self.Xp + R * np.sin(gamma)
        Y = self.Yp - R * np.cos(gamma)   
        
        return X,Y
        
    def EN2geo(self,E,N):
        """Transform planimetric to geographic coordinates"""
        DE = E-self.Xp
        DN = N-self.Yp
        Rsingamma = DE
        Rcosgamma = -DN
        
        R = (Rsingamma**2 + Rcosgamma**2)**0.5
        L = -np.log(R / self.C) / self.n
        lat = Li.latiso2lat(L)
        gamma = math.atan(Rsingamma / Rcosgamma)
        lon = gamma / self.n + self.lambda0
        
        return lon,lat
        
        
    def mod_lin(self,lat):
        """ Calcul du module lineaire """
        L = Li.lat2latiso(lat,self.e)
        R = self.C * np.exp(-self.n * L)
        N = gde_normale(lat,self.a,self.e)
        mu = self.n * R / N / np.cos(lat)
        return mu
        
    def plot_mod_lin(self,couleur = 'r'):
        Vphi = np.linspace(self.phi_min,self.phi_max,100)
        Vmu = self.mod_lin(Vphi) 
        plt.plot(Vphi/d2r,Vmu,couleur)

class Lambert_secant(Lambert):
    def __init__(self):
        """ """
        
    def set_constantes_definition(self,
                                  nom,
                                  X0,
                                  Y0,
                                  phi1,
                                  phi2,
                                  phi0,
                                  lambda0,
                                  a,
                                  e,
                                  phi_min=41*d2r,
                                  phi_max=52*d2r):
        self.nom = nom
        self.X0 = X0
        self.Y0 = Y0
        self.phi1 = phi1
        self.phi2 = phi2
        self.phi0 = phi0
        self.lambda0 = lambda0
        self.a = a
        self.e = e
        self.phi_min = phi_min
        self.phi_max = phi_max
        
        
    def calc_constantes_derivees(self):
        """
        Fonction qui calcule les constantes du Lambert secant
        Entrées
         	X0,Y0 : Coordonnées planes du point-origine p0, exprimées en mètres
          	phi1,phi2 : Latitudes des parallèles automécoïques, exprimées en radians
           lambda0,phi0 : Coordonnées géographiques du point-origine P0, exprimées en radians
           a : Demi grand axe de l'éllipsoïde, exprimé en mètres
           e : Première excentricité de l'éllipsoïde
        """
             
        #------------- Calcul de n----------------------------
        
        N1 = gde_normale(self.phi1,self.a,self.e)
        N2 = gde_normale(self.phi2,self.a,self.e)
        
        # Calcul de la latitude isométrique, appel à la fonction latiso
        L1 = Li.lat2latiso(self.phi1,self.e)
        L2 = Li.lat2latiso(self.phi2,self.e)
        
        # Application de la formule de la constante n
        n = math.log((N2*math.cos(self.phi2))/(N1*math.cos(self.phi1))) / (L1-L2)
        
        #------------- Calcul de C----------------------------
        C = (N1 * math.cos(self.phi1)/n)*math.exp(n*L1)
        
        #------------- Calcul de R0----------------------------
        L0 = Li.lat2latiso(self.phi0,self.e)
        R0 = C*math.exp(-n*L0)
        
        #------------- Calcul de Xp----------------------------
        Xp = self.X0;
        
        #------------- Calcul de Yp----------------------------
        Yp = self.Y0 + R0
        
        self.C = C
        self.n = n
        self.Xp = Xp
        self.Yp = Yp
        
    def set_CC(self,num):
        """ fixation des constantes CC42 """
        d2r = math.pi / 180
        self.X0 = 1700000
        self.Y0 = (num-41) * 1e6 + 2e5
        self.phi0 = num * d2r
        self.phi1 = self.phi0 - 0.75 * d2r
        self.phi2 = self.phi0 + 0.75 * d2r 
        self.lambda0 = 3 * d2r
        
        self.phi_min = self.phi0 - 1 * d2r
        self.phi_max = self.phi0 + 1 * d2r
        
        self.a = 6378137.0
        self.e = 0.081819191043
        
        self.nom = 'CC%2d' % (num)
        
        
class Lambert_tangentk0(Lambert):
    def __init__(self):
        """ """
        
    def set_constantes_definition(self,
                                  nom,
                                  X0,
                                  Y0,
                                  phi0,
                                  k0,
                                  lambda0,
                                  a,
                                  e,
                                  phi_min=41*d2r,
                                  phi_max=52*d2r):
        self.nom = nom
        self.X0 = X0
        self.Y0 = Y0
        self.k0 = k0
        self.phi0 = phi0
        self.lambda0 = lambda0
        self.a = a
        self.e = e
        self.e2 = self.e**2
        self.phi_min = phi_min
        self.phi_max = phi_max        
        
    def calc_constantes_derivees(self):
        """
         Fonction qui calcule les constantes du Lambert tg + k0
         Entrées
         	X0,Y0 : Coordonnées planes du point-origine p0, exprimées en mètres
        	lambda0,phi0 : Coordonnées géographiques du point-origine P0, exprimées en radians
             k0 : facteur d'échelle
             a : Demi grand axe de l'éllipsoïde, exprimé en mètres
             e : Première excentricité de l'éllipsoïde
        """
        n = math.sin(self.phi0);self.n = n
        N0=gde_normale(self.phi0,self.a,self.e)
        R0 = N0 * self.k0 / math.tan(self.phi0)
        L0 = Li.lat2latiso(self.phi0,self.e)
        self.C = R0 * math.exp(n*L0)
        self.Xp = self.X0
        self.Yp = self.Y0 + R0
        
    
            
    
def gde_normale(phi,a,e):
    """
    calcul de la grande normale
    phi en rad
    """
    
    e2 = e**2   
    w = np.sqrt( 1-e2 * (np.sin(phi))**2 )
    N = a / w
    return N
        
		
if __name__ == "__main__":

#    tic = time.time()

    a_grs80 = 6378137.0
    e_grs80 = 0.081819191043
    
    Lambert93 = Lambert_secant()
    Lambert93.set_constantes_definition('Lambert93',700000,6600000,44*d2r,49*d2r,46.5*d2r,3*d2r,a_grs80,e_grs80)
    Lambert93.calc_constantes_derivees()
    Lambert93.print()
  
    CC42 = Lambert_secant()
    CC42.set_CC(42)
    CC42.calc_constantes_derivees()
    CC43 = Lambert_secant()
    CC43.set_CC(43)
    CC43.calc_constantes_derivees()
    CC44 = Lambert_secant()
    CC44.set_CC(44)
    CC44.calc_constantes_derivees()
    CC45 = Lambert_secant()
    CC45.set_CC(45)
    CC45.calc_constantes_derivees()
    CC46 = Lambert_secant()
    CC46.set_CC(46)
    CC46.calc_constantes_derivees()
    CC47 = Lambert_secant()
    CC47.set_CC(47)
    CC47.calc_constantes_derivees()
    CC48 = Lambert_secant()
    CC48.set_CC(48)
    CC48.calc_constantes_derivees()
    CC49 = Lambert_secant()
    CC49.set_CC(49)
    CC49.calc_constantes_derivees()
    CC50 = Lambert_secant()
    CC50.set_CC(50)
    CC50.calc_constantes_derivees()
    
    a_clarke80 = 6378249.2
    b_clarke80 = 6356515.0
    e2_clarke80 = (a_clarke80**2 - b_clarke80**2) / a_clarke80**2
    e_clarke80 = math.sqrt(e2_clarke80)
    
    LambertI = Lambert_tangentk0()
    LambertI.set_constantes_definition('Lambert I',600000, 200000, 55*g2r, 0.99987734, 0*g2r, a_clarke80, e_clarke80,53.5*g2r,57*g2r)
    LambertI.calc_constantes_derivees()
    
    LambertII = Lambert_tangentk0()
    LambertII.set_constantes_definition('Lambert II',600000, 200000, 52*g2r, 0.99987742, 0*g2r, a_clarke80, e_clarke80,50.5*g2r,53.5*g2r)
    LambertII.calc_constantes_derivees()
    
    LambertIIet = Lambert_tangentk0()
    LambertIIet.set_constantes_definition('Lambert II étendu',600000, 2200000, 52*g2r, 0.99987742, 0*g2r, a_clarke80, e_clarke80)
    LambertIIet.calc_constantes_derivees()

    LambertIII = Lambert_tangentk0()
    LambertIII.set_constantes_definition('Lambert III',600000, 200000, 49*g2r, 0.99987750, 0*g2r, a_clarke80, e_clarke80,47*g2r,50.5*g2r)
    LambertIII.calc_constantes_derivees()
    
    LambertIV = Lambert_tangentk0()
    LambertIV.set_constantes_definition('Lambert IV',234.358, 185861.369, 46.85*g2r, 0.99994471, 0*g2r, a_clarke80, e_clarke80,45.9*g2r,47.8*g2r)
    LambertIV.calc_constantes_derivees()  


#    plt.figure()
#    plt.grid('on')
#    Lambert93.plot_mod_lin()
#    CC42.plot_mod_lin('r')
#    CC43.plot_mod_lin('g')
#    CC44.plot_mod_lin('b')
#    CC45.plot_mod_lin('r')
#    CC46.plot_mod_lin('g')
#    CC47.plot_mod_lin('b')
#    CC48.plot_mod_lin('r')
#    CC49.plot_mod_lin('g')
#    CC50.plot_mod_lin('b')
#     
#    LambertI.plot_mod_lin('c')     
#    LambertIIet.plot_mod_lin('m') 
#    LambertIII.plot_mod_lin('y')     
#    LambertIV.plot_mod_lin('k')  
#    
#    plt.show()
#    
#    fig = plt.figure()
#    plt.grid('on')
#    CC42.plot_mod_lin('r')
#    CC43.plot_mod_lin('g')
#    CC44.plot_mod_lin('b')
#    CC45.plot_mod_lin('r')
#    CC46.plot_mod_lin('g')
#    CC47.plot_mod_lin('b')
#    CC48.plot_mod_lin('r')
#    CC49.plot_mod_lin('g')
#    CC50.plot_mod_lin('b')
#     
#    LambertI.plot_mod_lin('c')     
#    LambertII.plot_mod_lin('m') 
#    LambertIII.plot_mod_lin('y')     
#    LambertIV.plot_mod_lin('k')  
#
#    plt.show()
#      
#    toc = time.time()
#    print ('%.3f sec elapsed ' % (toc-tic))
