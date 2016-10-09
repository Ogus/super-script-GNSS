# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 10:23:58 2016

@author: Augustin
"""

from script import gui
import sys
import PyQt4.QtGui as qtg

def main():
    app = qtg.QApplication(sys.argv)
    frame = gui.App()
    sys.exit(app.exec_())
    

if __name__=='__main__':
    main()
    
"""
Appuyez su 'F5' pour lancer l'application
"""