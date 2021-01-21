import sys, numpy
from matplotlib import pyplot
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QTime, QDate, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvas 

class Livraison(QtWidgets.QMainWindow):
    def __init__(self) :
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("Interface_livraison.ui",self)
        self.sel_viticulteur.addItems(viticulteur)
        self.ListeParcelle()
        self.ListeCepage()
        self.sel_viticulteur.currentIndexChanged.connect(self.ListeParcelle)
        self.sel_parcelle.currentIndexChanged.connect(self.ListeCepage)
        self.bouton_ajout.clicked.connect(self.AjoutRecolte)
        self.bouton_tot.clicked.connect(self.OuvrirRecu)

    def ListeParcelle(self) :
        global liste_parcelle
        viti = str(self.sel_viticulteur.currentText())
        parc = []
        for i in range(len(liste_parcelle)) :
            if viti in liste_parcelle[i] :
                parc.append(liste_parcelle[i][1])
        self.sel_parcelle.clear()
        self.sel_parcelle.addItems(parc)

    def ListeCepage(self) :
        global liste_parcelle, cepages
        parc = str(self.sel_parcelle.currentText())
        cep = []
        for i in range(len(liste_parcelle)) :
            if parc in liste_parcelle[i] :
                for n in liste_parcelle[i][2] :
                    cep.append(cepages[int(n) - 1])
        self.sel_cepage.clear()
        self.sel_cepage.addItems(cep)

    def AjoutRecolte(self) :
        global ventes, somme
        now = QDate.currentDate()
        time = QTime.currentTime()
        name = str(self.sel_viticulteur.currentText())
        parc = str(self.sel_parcelle.currentText())
        cep = str(self.sel_cepage.currentText())
        qtt = self.sel_poids.value()
        if qtt :
            ventes.append([now.toString('d/M/yy'), time.toString('h:mm:ss'), name, parc, cep, qtt])
            found = False
            for n in somme :
                if name in n and cep in n :
                    found = True
                    n[2] += qtt
            if found == False :
                somme.append([name, cep, qtt])
        self.sel_poids.setValue(0)


    def OuvrirRecu(self) :
        Fenetre = Recu(self)
        Fenetre.show()

class Recu(QtWidgets.QMainWindow) :
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("total.ui",self)
        self.qtableFromArray(ventes, self.tableau)
        self.bouton_print.clicked.connect(self.Impression)
        self.bouton_tot2.clicked.connect(self.OuvrirSomme)

    def qtableFromArray(self, array, qtable) :
        nbCol = len(titres)
        qtable.setColumnCount(nbCol)
        qtable.setHorizontalHeaderLabels(titres)
        qtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        if ventes :
            nbRow = len(array)         
            qtable.setRowCount(nbRow)
            for i in range(nbRow):
                for j in range(nbCol):
                    qtable.setItem(i,j, QtWidgets.QTableWidgetItem(str(array[i][j])))

    def Impression(self) :
        global ventes
        with open("Recu_" + QDate.currentDate().toString('d_M_yyyy') + ".txt", "w") as st :
            for i in range(len(ventes)) :
                st.write(str(ventes[i][0]) + ";" + str(ventes[i][1]) + ";" + str(ventes[i][2]) + ";" + str(ventes[i][3]) + ";" + str(ventes[i][4]) + ";" + str(ventes[i][5]) + "\n")
                

    def OuvrirSomme(self) :
        Fenetre2 = Somme(self)
        Fenetre2.show()
    
class Somme(QtWidgets.QMainWindow) :
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("somme.ui",self)
        self.qtableFromArray(somme, self.tableau_somme)
        self.bouton_print2.clicked.connect(self.ImpressionSomme)
        self.plotWidget = FigureCanvas(self.GraphSomme(somme))
        lay = QtWidgets.QVBoxLayout(self.blankwidget)  
        lay.setContentsMargins(0, 0, 0, 0)      
        lay.addWidget(self.plotWidget)
        

    def qtableFromArray(self, array, qtable) :
        nbCol = len(titres2)
        qtable.setColumnCount(nbCol)
        qtable.setHorizontalHeaderLabels(titres2)
        qtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        if somme :
            nbRow = len(array)         
            qtable.setRowCount(nbRow)
            for i in range(nbRow):
                for j in range(nbCol):
                    qtable.setItem(i,j, QtWidgets.QTableWidgetItem(str(array[i][j])))

    def ImpressionSomme(self) :
        global somme
        with open("Somme_" + QDate.currentDate().toString('d_M_yyyy') + ".txt", "w") as st :
            for i in range(len(somme)) :
                st.write(str(somme[i][0]) + ";" + str(somme[i][1]) + ";" + str(somme[i][2]) + "\n")
    
    def GraphSomme(self, somme) :
        somme.sort()
        labels, cepages, qtt = [], [], []
        y = 0

        for i in somme :
            labels.append(i[0])
            cepages.append(i[1])
            qtt.append(i[2])
        x = numpy.arange(len(labels))
        width = 0.35
        fig, ax = pyplot.subplots()

        rects1 = ax.bar(x, qtt, width, label='Quantité')
        ax.set_ylabel('Poids (kg)')
        ax.set_title('Poids de raisin par cépage')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        n = 0
        for rect in rects1:
            height = rect.get_height()
            if height > y :
                y = height
            ax.annotate(cepages[n],
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
            n += 1
        fig.tight_layout(pad=2)
        pyplot.ylim(0, y * 1.2)
        return fig


if __name__ == "__main__":
    titres = ["Date", "Heure", "Viticulteur", "Parcelle", "Cépage", "Quantité (kg)"]
    titres2 = ["Nom", "Cépage", "Quantité (kg)"]
    cepages = ["pinot noir", "merlot", "malbec", "trousseau", "gamay", "chardonnay", "sauvignon", "grenache", "savagnin", "chenin" ]
    liste = []
    ventes = []
    somme = []
    with open("producteurs.txt", "r") as st :
        for ligne in st :
            ligne = ligne.rstrip('\n')
            liste.append(ligne)
    del(liste[0])
    for i in range(len(liste)) :
        liste[i] = liste[i].split(";")
    liste = list(map(list, zip(*liste)))
    for i in range(len(liste[1])) :
        liste[2][i] = liste[2][i].split(", ")
    viticulteur = list(set(liste[0]))
    viticulteur.sort()
    liste_parcelle = list(zip(liste[0], liste[1], liste[2]))
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Livraison()
    window.show()
    sys.exit(app.exec_())