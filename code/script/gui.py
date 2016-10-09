# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 00:16:48 2016

@author: ogustin
"""
import numpy as np
import PyQt4.QtGui as qtg
import PyQt4.QtCore as qtc
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import script.utility as utl
import script.fourier as fr
import script.moindresC as mc

class App(qtg.QTabWidget):
    """
    Cette classe génère l'interface graphique et l'ensemble des fonctions associées
    """
    
    def __init__(self):
        """
        Créé les différents objets de l'interface
        """
        super(App, self).__init__()
        self.tab_intro = qtg.QWidget()      #créé un onglet
        self.tab_csv = qtg.QWidget()
        self.tab_comp = qtg.QWidget()
        self.tab_3d = qtg.QWidget()
        self.tab_cut = qtg.QWidget()
        self.tab_fourier = qtg.QWidget()
        self.tab_lstsq = qtg.QWidget()
        self.addTab(self.tab_intro,"Introduction")      #ajoute l'onglet à la fenêtre principale
        self.addTab(self.tab_csv,"CSV")
        self.addTab(self.tab_comp,"Comparateur")
        self.addTab(self.tab_3d,"3D")
        self.addTab(self.tab_cut,"Cut")
        self.addTab(self.tab_fourier,"Fourier")
        self.addTab(self.tab_lstsq,"MoindresCarrés")
        
        self.dim = int(qtg.QDesktopWidget().screenGeometry().height() / 2)      #récupère la dimension max de la fenêtre
        self.initUI_intro()
        self.initUI_csv()
        self.initUI_compare()
        self.initUI_3d()
        self.initUI_cut()
        self.initUI_fourier()
        self.initUI_lstsq()
        
        self.resize(self.sizeHint())        #redimensionne la fenêtre
        self.center()                       #centre la fenêtre au milieu de l'écran
        self.setWindowIcon(qtg.QIcon("logo.png"))
        self.setWindowTitle("Super Script GNSS - v2.1")
        self.show()
        
    def initUI_intro(self):
        layout = qtg.QVBoxLayout()      #layout vertical pour ajouter l'ensemble des Widgets
        layout.setSpacing(20)
        
        label_1 = qtg.QLabel()          #widget de texte
        label_1.setText("Ce programme a été développé dans le cadre d'un projet sur les récepteurs GNSS cadencés à 20 Hz \n"\
                        "Il a pour but de faciliter le traitement et l'analyse des données obtenues")
        label_1.setAlignment(qtc.Qt.AlignCenter)
        layout.addWidget(label_1)
        
#        img_name = "logo.png"
        img = qtg.QLabel()
        img.setPixmap(qtg.QPixmap("logo.png"))      #affichage d'une image sur un QLabel vide
        img.setAlignment(qtc.Qt.AlignCenter)
        layout.addWidget(img)
        
        label_2 = qtg.QLabel()
        label_2.setText("Présentation des différents onglets: \n\n"\
                        "\t Crééer CSV: Convertis un ficher .pos en un fichier csv pour l'utiliser et l'analyser ultérieurement.\n\n" \
                        "\t Visionner: Permet de visionner un ou plusieurs fichiers de données afin de les comparer.\n\n" \
                        "\t Modèle 3D: Permet de visualiser en 3D les données d'un unique fichier de données.\n\n" \
                        "\t Couper CSV: Récupère les données d'un fichier csv et en sauvegarde un extrait.\n\n" \
                        "\t Analyse de Fourier: Effectue l'analyse de Fourier des données d'un fichier.\n\n" \
                        "\t Estimation linéaire: Calcule le plan tangent à une suite de points par moindres carrés")
        layout.addWidget(label_2)
        
        self.tab_intro.setLayout(layout)        #définit la layout de l'onglet
        self.setTabText(0,"Présentation")       #ordonne l'onglet et définis sont titre
        
    
    def initUI_csv(self):
        self.file_for_csv = ""
        self.csv_file = ""
        
        grid = qtg.QGridLayout()        #layout sous forme de grille pour placer les Widgets
        grid.setSpacing(20)
        
        open_button = qtg.QPushButton("Fichier d'entrée")           #créé un bouton poussoir
        open_button.clicked.connect(self.open_for_csv)
        open_button.setToolTip("Choisissez le fichier .pos à convertir")
        grid.addWidget(open_button, 0,0)
        self.csv_label = qtg.QLabel("Fichier: ")
        grid.addWidget(self.csv_label, 0,1, 1,2)
        
        save_button = qtg.QPushButton("Fichier de sortie")
        save_button.clicked.connect(self.save_csv)
        save_button.setToolTip("Choisissez le fichier .csv où enregistrer \n les données")
        grid.addWidget(save_button, 1,0)
        self.save_label = qtg.QLabel("Fichier: ")
        grid.addWidget(self.save_label, 1,1, 1,2)
        
        
        lambert_label = qtg.QLabel("Projection:")
        lambert_label.setAlignment(qtc.Qt.AlignCenter)
        lambert_label.setToolTip("Choisissez la projection Lambert \n pour convertir les coordonnées")
        self.lambert_csv = qtg.QComboBox()
        self.lambert_csv.addItems(['Lambert 93','CC42','CC43','CC44','CC45','CC46','CC47','CC48',\
                                'CC49','CC50','Lambert 1','Lambert 2','Lambert 3','Lambert 4'])
        self.lambert_csv.setToolTip("Choisissez la projection Lambert \n pour convertir les coordonnées")
        grid.addWidget(lambert_label, 2,0)
        grid.addWidget(self.lambert_csv, 2,1)
        
        q_label = qtg.QLabel("Qualité:")
        q_label.setAlignment(qtc.Qt.AlignCenter)
        self.q_csv = qtg.QComboBox()
        self.q_csv.addItems(["Q = 1","Q = 1 ou 2"])
        q_label.setToolTip("Choisissez la qualité des données à conserver")
        grid.addWidget(q_label, 3,0)
        grid.addWidget(self.q_csv, 3,1)
        
        
        start = qtg.QPushButton("Créer")
        start.clicked.connect(self.launch_csv)
        grid.addWidget(start, 4,1, 1,1)
        
        self.tab_csv.setLayout(grid)
        self.setTabText(1,"Créer CSV")
        
        
    def initUI_compare(self):
        """
        Initiate the interface for a tab
        """
        self.filenames = []

        grid = qtg.QGridLayout()
        grid.setSpacing(20)
        
        open_button = qtg.QPushButton("Ajouter fichier")
        open_button.clicked.connect(self.open_file)
        open_button.setToolTip("Ajouter un fichier .csv à la liste")
        grid.addWidget(open_button, 0,0)
        
        self.delete = qtg.QPushButton("Supprimer fichier")
        self.delete.clicked.connect(self.delete_file)
        self.delete.setToolTip("Supprimer un fichier .csv de la liste")
        grid.addWidget(self.delete, 1,0)
        
        self.file_list = qtg.QListWidget()
        grid.addWidget(self.file_list, 0,1, 2,2)
        
        value_label = qtg.QLabel("Attribut:")
        value_label.setAlignment(qtc.Qt.AlignCenter)
        value_label.setToolTip("Choisissez l'attribut de donnée \n que vous voulez comparer")
        self.attributes = qtg.QComboBox()
        self.attributes.addItems(['Est/Nord','Est','Nord','Hauteur','Vitesse','Vitesse Plani','Vitesse Alti','Acceleration'])
        grid.addWidget(value_label, 2,0)
        grid.addWidget(self.attributes, 2,1)
        
        
        self.redux_option = qtg.QCheckBox("Moyenner les valeurs")
        self.redux_option.setChecked(True)
        self.redux_option.setToolTip("Recentrer les valeurs en 0")
        grid.addWidget(self.redux_option, 3,0, 1,2)
        
        
        start = qtg.QPushButton("Visionner")
        start.setToolTip('Start !')
        start.clicked.connect(self.launch_compare)
        grid.addWidget(start, 4,1, 1,1)
        
        line = qtg.QFrame()
        line.setFrameStyle(qtg.QFrame.HLine)
        grid.addWidget(line, 5,0, 1,3)
        
        draw_label = qtg.QLabel("Options d'affichage:")
        grid.addWidget(draw_label, 6,0)
        
        color_label = qtg.QLabel("Couleur: ")
        color_label.setAlignment(qtc.Qt.AlignCenter)
        self.color_choice = qtg.QComboBox()
        self.color_choice.addItems(['Bleu','Vert','Rouge','Jaune','Violet','Turquoise','Noir'])
        grid.addWidget(color_label, 7,0)
        grid.addWidget(self.color_choice, 7,1)
        
        self.line_choice = qtg.QCheckBox("Relier les points")
        self.line_choice.setChecked(True)
        grid.addWidget(self.line_choice, 7,2)  
        
        self.tab_comp.setLayout(grid)
        self.setTabText(2,"Visionner")
        
        
    def initUI_3d(self):
        self.file_for_3d = ""
        
        grid = qtg.QGridLayout()
        grid.setSpacing(20)
        
        open_button = qtg.QPushButton("Fichier d'entrée")
        open_button.clicked.connect(self.open_3d)
        open_button.setToolTip("Choisissez le fichier .csv à visionner en 3D")
        grid.addWidget(open_button, 0,0)
        self.label_3d = qtg.QLabel("Fichier: ")
        grid.addWidget(self.label_3d, 0,1, 1,2)
        
        self.redux_3d = qtg.QCheckBox("Moyenner les valeurs")
        self.redux_3d.setChecked(False)
        self.redux_3d.setToolTip("Recentrer les valeurs en 0")
        grid.addWidget(self.redux_3d, 1,0, 1,2)
        
        start = qtg.QPushButton("Visualiser")
        start.clicked.connect(self.launch_3d)
        grid.addWidget(start, 2,1, 1,1)
        
        self.tab_3d.setLayout(grid)
        self.setTabText(3,"Modèle 3D")
        
        
    def initUI_cut(self):
        self.file_for_cut = ""
        self.cut_file = ""
        
        grid = qtg.QGridLayout()
        grid.setSpacing(20)
        
        open_button = qtg.QPushButton("Fichier d'entrée")
        open_button.clicked.connect(self.open_cut)
        open_button.setToolTip("Choisissez le fichier .csv pour \n extraire les données")
        grid.addWidget(open_button, 0,0)
        self.csv_cut_input = qtg.QLabel("Fichier: ")
        grid.addWidget(self.csv_cut_input, 0,1, 1,2)
        
        save_button = qtg.QPushButton("Fichier de sortie")
        save_button.clicked.connect(self.save_cut)
        save_button.setToolTip("Choisissez le fichier .csv pour \n sauvegarder les données")
        grid.addWidget(save_button, 1,0)
        self.csv_cut_output = qtg.QLabel("Fichier: ")
        grid.addWidget(self.csv_cut_output, 1,1, 1,2)
        
        label = qtg.QLabel("Intervalle (s):")
        label.setAlignment(qtc.Qt.AlignCenter)
        label.setToolTip("Choisissez l'intervalle de temps pour \n les données à conserver")
        grid.addWidget(label, 2,0)
        
        h1 = qtg.QHBoxLayout()
        start_label = qtg.QLabel("Début:")
        start_label.setAlignment(qtc.Qt.AlignCenter)
        self.min_cut = qtg.QSpinBox()
        self.min_cut.setRange(0,0)
        self.min_cut.valueChanged.connect(self.set_range)
        h1.addWidget(start_label)
        h1.addWidget(self.min_cut)
        grid.addLayout(h1, 2,1)
        
        h2 = qtg.QHBoxLayout()
        stop_label = qtg.QLabel("Fin:")
        stop_label.setAlignment(qtc.Qt.AlignCenter)
        self.max_cut = qtg.QSpinBox()
        self.max_cut.setRange(0,0)
        self.max_cut.valueChanged.connect(self.set_range)
        h2.addWidget(stop_label)
        h2.addWidget(self.max_cut)
        grid.addLayout(h2, 2,2)
        
        start = qtg.QPushButton("Découper")
        start.clicked.connect(self.launch_cut)
        grid.addWidget(start, 3,1, 1,1)
        
        self.tab_cut.setLayout(grid)
        self.setTabText(4,"Couper CSV")
        
        
    def initUI_fourier(self):
        self.file_for_fourier = ""
        
        grid = qtg.QGridLayout()
        grid.setSpacing(20)
        
        open_button = qtg.QPushButton("Fichier d'entrée")
        open_button.clicked.connect(self.open_fourier)
        open_button.setToolTip("Choisissez le fichier .csv pour \n effectuer l'analyse de Fourier")
        grid.addWidget(open_button, 0,0)
        self.fourier_label = qtg.QLabel("Fichier: ")
        grid.addWidget(self.fourier_label, 0,1, 1,2)
        
        value_label = qtg.QLabel("Attribut:")
        value_label.setAlignment(qtc.Qt.AlignCenter)
        value_label.setToolTip("Choisissez l'attribut de donnée \n que vous voulez analyser")
        self.attr_fourier = qtg.QComboBox()
        self.attr_fourier.addItems(['Est','Nord','Hauteur','Vitesse','Vitesse Plani','Vitesse Alti','Acceleration'])
        self.attr_fourier.currentIndexChanged.connect(self.enable_rot)
        grid.addWidget(value_label, 1,0)
        grid.addWidget(self.attr_fourier, 1,1)
        
        self.rot_option = qtg.QCheckBox('Rotation du plan')
        self.rot_option.setChecked(False)
        self.rot_option.setDisabled(True)
        self.rot_option.setToolTip("Effectue la rotation du plan contenant les points \n pour " \
                                    "diminuer la composante continue de l'analyse de Fourier")
        grid.addWidget(self.rot_option, 2,0, 1,2)
        
        start = qtg.QPushButton("Lancer l'analyse")
        start.clicked.connect(self.launch_fourier)
        grid.addWidget(start, 3,1, 1,1)
        
        self.tab_fourier.setLayout(grid)
        self.setTabText(5,"Analyse de Fourier")
    
        
    def initUI_lstsq(self):
        self.file_for_lstsq = ""
        
        grid = qtg.QGridLayout()
        grid.setSpacing(10)
        
        open_button = qtg.QPushButton("Fichier d'entrée")
        open_button.clicked.connect(self.open_for_lstsq)
        open_button.setToolTip("Choisissez le fichier .csv pour \n calculer l'estimation linéaire")
        grid.addWidget(open_button, 0,0)
        self.label_lstsq = qtg.QLabel("Fichier: ")
        grid.addWidget(self.label_lstsq, 0,1, 1,2)
        
        start = qtg.QPushButton("Calculer l'estimation linéaire")
        start.clicked.connect(self.launch_lstsq)
        grid.addWidget(start, 1,1, 2,1)
        
        self.std_label = qtg.QLabel("Écart-type:")
        self.std_label.setToolTip("Écart-type des résidus")
        self.diff_label = qtg.QLabel("Différence:")
        self.diff_label.setToolTip("Différence maximale pic à pic")
        grid.addWidget(self.std_label, 3,0, 1,1)
        grid.addWidget(self.diff_label, 3,2, 1,1)
        
        self.tab_lstsq.setLayout(grid)
        self.setTabText(6,"Estimation linéaire")
        
        
        
    """
    Les fonctions qui suivent permettent de modifier l'interfac graphique et les variables en fonction des 
    actions de l'utilisateur
    """
        
    def center(self):
        """
        Centre la fenêtre au milieu de l'écran en fonction de leurs tailles respectives
        """
        rect = self.frameGeometry()         #size of widget
        center = qtg.QDesktopWidget().availableGeometry().center()      #center of screen resolution
        rect.moveCenter(center)     #move center point of rect to center point of screen
        self.move(rect.topLeft())     #move widget to top left corner of rect
        
        
    def open_for_csv(self):
        file = qtg.QFileDialog()
        file.setFilter("Positon files (*.pos)")
        file.setAcceptMode(qtg.QFileDialog.AcceptOpen)
        
        if file.exec_():
            f = file.selectedFiles()
            self.file_for_csv = f[0]
            self.csv_label.setText("Fichier: " + f[0])
    
    def save_csv(self):
        file = qtg.QFileDialog()
        file.setFilter("csv files (*.csv)")
        file.setAcceptMode(qtg.QFileDialog.AcceptSave)
        
        if file.exec_():
            f = file.selectedFiles()
            self.csv_file = f[0]
            if(self.csv_file[-4:] != ".csv"): self.csv_file += ".csv"
            self.save_label.setText("Fichier: " + self.csv_file)
            
            
    def open_file(self):
        file = qtg.QFileDialog()
        file.setFilter("csv files (*.csv)")
        file.setAcceptMode(qtg.QFileDialog.AcceptOpen)
        
        if file.exec_():
            files = file.selectedFiles()
            for f in files:
                if(f not in self.filenames):
                    self.filenames.append(f)
                    self.file_list.addItem(f)
            
    def delete_file(self):
        index = self.file_list.currentRow()
        self.file_list.removeItemWidget(self.file_list.takeItem(index))
        del self.filenames[index]
        
            
    def open_3d(self):
        file = qtg.QFileDialog()
        file.setFilter("csv file (*.csv)")
        file.setAcceptMode(qtg.QFileDialog.AcceptOpen)
        
        if file.exec_():
            f = file.selectedFiles()
            self.file_for_3d = f[0]
            self.label_3d.setText("Fichier: " + f[0])
        
            
    def open_cut(self):
        file = qtg.QFileDialog()
        file.setFilter("Csv files (*.csv)")
        file.setAcceptMode(qtg.QFileDialog.AcceptOpen)
        
        if file.exec_():
            f = file.selectedFiles()
            self.file_for_cut = f[0]
            self.csv_cut_input.setText("Fichier: " + f[0])
            
            time = utl.read_csv(self.file_for_cut)[0]
            self.min_cut.setRange(time[0],time[-1])
            self.min_cut.setValue(time[0])
            self.max_cut.setRange(time[0],time[-1])
            self.max_cut.setValue(time[-1])
            
    def set_range(self):
        self.min_cut.setMaximum(self.max_cut.value())
        self.max_cut.setMinimum(self.min_cut.value())
            
    def save_cut(self):
        file = qtg.QFileDialog()
        file.setFilter("Csv file (*.csv)")
        file.setAcceptMode(qtg.QFileDialog.AcceptSave)
        
        if file.exec_():
            f = file.selectedFiles()
            self.cut_file = f[0]
            if(self.cut_file[-4:] != ".csv"): self.cut_file += ".csv"
            self.csv_cut_output.setText("Fichier: " + self.cut_file)
            
            
    def open_fourier(self):
        file = qtg.QFileDialog()
        file.setFilter("Csv file (*.csv)")
        file.setAcceptMode(qtg.QFileDialog.AcceptOpen)
        
        if file.exec_():
            f = file.selectedFiles()
            self.file_for_fourier = f[0]
            self.fourier_label.setText("Fichier: " + f[0])
            
    def enable_rot(self):
        if(self.attr_fourier.currentIndex() == 2):
            self.rot_option.setDisabled(False)
        else:
            self.rot_option.setDisabled(True)
    
        
    def open_for_lstsq(self):
        file = qtg.QFileDialog()
        file.setFilter("csv file (*.csv)")
        file.setAcceptMode(qtg.QFileDialog.AcceptOpen)
        
        if file.exec_():
            f = file.selectedFiles()
            self.file_for_lstsq = f[0]
            self.label_lstsq.setText("Fichier: " + f[0])
            
            
    
    def launch_csv(self):
        if(self.file_for_csv != "" and self.csv_file != ""):
            temp = utl.extract_data(self.file_for_csv,self.lambert_csv.currentText(),q=self.q_csv.currentIndex()+1)
            utl.create_csv(temp,output=self.csv_file)
            print("done")
            
            
    def launch_compare(self):
        if(len(self.filenames) > 0):
            result = []
            for file in self.filenames:
                temp = utl.read_csv(file)
                if(self.redux_option.isChecked()): utl.redux(temp[0],temp[1],temp[2],temp[3])
                result.append(temp)
                
            base = result[0]
            measures = []
            if(len(result) > 1):
                measures = result[1:]
            self.compare(base,*measures)
            print("done")
                      
            
    def launch_3d(self):
        if(self.file_for_3d != ""):
            data = utl.read_csv(self.file_for_3d)
            if(self.redux_3d.isChecked()): utl.redux(data[0],data[1],data[2],data[3])
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.set_xlabel('Est')
            ax.set_ylabel('Nord')
            ax.set_zlabel('Hauteur')
            ax.plot(data[1],data[2],data[3])
            print("done")
            
                  
    def launch_cut(self):
        if(self.file_for_cut != "" and self.cut_file != ""):
            temp = utl.read_csv(self.file_for_cut)
            utl.cut_csv(self.cut_file,temp,self.min_cut.value(),self.max_cut.value())
            print("done")
        
        
    def launch_fourier(self):
        if(self.file_for_fourier != ""):
            fr.fourier(self.file_for_fourier,self.attr_fourier.currentIndex(),self.rot_option.isChecked())
            print("done")
         
            
    def launch_lstsq(self):
        if(self.file_for_lstsq != ""):
            result = mc.lst_square(self.file_for_lstsq)
            data = utl.read_csv(self.file_for_lstsq)
            utl.redux(*data[:4])
            mc.draw(data,result[0],result[1])
            self.std_label.setText("Écart-type:  " + str(result[2]*100)[:6] + " cm")
            self.diff_label.setText("Différence:  " + str(result[3]*100)[:6] + " cm")
            print("done")

        
    def compare(self,base,*measures):
        #bleu, vert, rouge, jaune, violet, turquoise, noir
        colors = ['#2b5797','#00a300','#d22927','#ffc40d','#a200ff','#00aba9','#31302b']
        l_style = 'None'
        if(self.line_choice.isChecked()): l_style = '-'
        
        absc = 0        #abscisse et ordonnée du graphe
        ordo = 3
        if(self.attributes.currentIndex() == 0):
            absc = 1
            ordo = 2
        else:
            ordo = self.attributes.currentIndex()
            
        plt.plot(base[absc],base[ordo],color=colors[self.color_choice.currentIndex()],linestyle=l_style,marker='+',ms=5)
        
        k = 0
        for data in measures:
            if(k == self.color_choice.currentIndex()): k += 1
            plt.plot(data[absc],data[ordo],color=colors[k],linestyle=l_style,marker='+',ms=5)
            k += 1
            
#        plt.savefig("toto.png",dpi=300)
        plt.show()
            