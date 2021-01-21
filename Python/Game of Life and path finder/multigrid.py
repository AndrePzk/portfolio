import sys, random, copy
import numpy as np
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QApplication
from PyQt5.QtGui import QBrush

np.set_printoptions(threshold=sys.maxsize)

class Window(QtWidgets.QMainWindow):
    def __init__(self) :
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("multigrid.ui",self)
        self.table = self.LeMonde()
        self.scene = QGraphicsScene()
        graphicView = QGraphicsView(self.scene, self.widget)
        graphicView.setGeometry(0,0,620,620)
        #self.widget.setPixmap(QPixmap())
        #self.layout = QtWidgets.QGridLayout()
        self.GridInit()
        self.butt_init.clicked.connect(self.GridInit)
        self.butt_rand.clicked.connect(self.Randomize)
        self.butt_gol.clicked.connect(self.Golrun)
        self.butt_path.clicked.connect(self.Pathfind)
        self.widget.mousePressEvent = self.getPos
        



    def LeMonde(self) :
        T = np.zeros((60, 60))
        return T

    def Randomize(self) :
        self.GridInit()
        for w in range(1,59) :
            for v in range(1, 59) :
                self.table[w][v] = random.randint(0, 1)
        self.draw(self.table)


    def GridInit(self) :
        global pathstart, pathend, pathready, searching

        self.table = self.LeMonde()
        self.label.setText("")
        pathstart, pathend, pathready, searching = False, False, False, False
        for column in range(60):
            for row in range(60):
                self.scene.addRect(row * 10, column * 10, 10, 10, brush = QBrush(Qt.black))

    def redraw(self, table):
        global Toriginal

        for i in range(1, 59):
            for n in range(1, 59):
                if table[i][n] != Toriginal[i][n] :
                    row = i
                    col = n
                    if table[i][n] == 1 :
                        self.scene.addRect(row * 10, col * 10, 10, 10, brush = QBrush(Qt.white))
                    else :
                        self.scene.addRect(row * 10, col * 10, 10, 10, brush = QBrush(Qt.black))

    def draw(self, table) :
        for column in range(60):
            for row in range(60):
                self.scene.addRect(row * 10, column * 10, 10, 10, brush = QBrush(Qt.black))

        for w in range(1,59) :
            for v in range(1, 59) :
                if table[w][v] == 1 :
                    self.scene.addRect(w * 10, v * 10, 10, 10, brush = QBrush(Qt.white))
                if table[w][v] == 8  :
                    self.scene.addRect(w * 10, v * 10, 10, 10, brush = QBrush(Qt.red))
                if table[w][v] == 9 :
                    self.scene.addRect(w * 10, v * 10, 10, 10, brush = QBrush(Qt.blue))
    
    def Golrun(self) :
        global gol_state
        if gol_state == False :
            gol_state = True
            self.butt_gol.setText("Game of Life - Stop")
            self.GolLoop()
        else :
            self.butt_gol.setText("Game of Life - Start")
            gol_state = False
            

    def GolLoop(self) :
        global gol_state
        while gol_state == True :
            self.table = self.gen(self.table)
            self.redraw(self.table)
            QApplication.processEvents()

    def gen(self, T) :
        Tnext = []
        global Toriginal
        Tnext = copy.deepcopy(T)
        T = copy.deepcopy(Tnext)
        Toriginal = copy.deepcopy(T)
        for y in range(1, 59) :
            for x in range(1, 59) :
                srrnd = 0
                
                for k in range(-1, 2) :
                    for l in range (-1, 2) :
                        if k == 0 and l == 0 :
                            pass
                        else :
                            if T[y+k][x+l] == 1 :
                                srrnd+=1
                            
                if T[y][x] == 1 :
                    if 1 < srrnd < 4 :
                        Tnext[y][x] = 1
                    else :
                        Tnext[y][x] = 0
                if T[y][x] == 0 :
                    if srrnd == 3 :
                        Tnext[y][x] = 1
                    else :
                        Tnext[y][x] = 0

        return Tnext

    def getPos(self, event):
        global pathstart, pathend, pathready, startx, starty, goalx, goaly

        x = int((event.pos().x() - 10) / 10)
        y = int((event.pos().y() - 10) / 10)
        a = self.table[x][y]
        print(x, y)
        if pathstart == False and pathend == False : 
            if a == 0 :
                b = 1
            if a == 1 :
                b = 0
        elif pathstart == True and pathend == False :
            b = 8
            startx, starty = x, y
            pathend = True
            self.label.setText("Select goal")
        else :
            b = 9
            goalx, goaly = x, y
            pathstart, pathend = False, False
            pathready = True
            self.label.setText("Ready")
        self.table[x][y] = b
        self.draw(self.table)

    def Pathfind(self) :
        global pathstart, pathend, pathready
        if pathstart == False and pathend == False and pathready == False :
            pathstart = True
            self.label.setText("Select Start")
        elif pathready == True :
            self.label.setText("Searching...")
            self.pathfinderloop()

        
    def pathfinderloop(self) :
        global startx, starty, goalx, goaly, pathready, searching, distancex, distancey
        searching = True
        pos = np.array([startx, starty])
        path, history_local = [], []
        orientation = np.zeros((2))
        newpath = True
        switch = True
        while searching :
            QApplication.processEvents()
            if newpath : 
                if goalx - pos[0] != 0 :
                    distancex = (goalx - pos[0])
                    orientation[0] = (goalx - pos[0]) / abs(goalx - pos[0])
                else :
                    orientation[0] = 0
                if goaly - pos[1] != 0 :
                    distancey = (goaly - pos[1]) 
                    orientation[1] = (goaly - pos[1]) / abs(goaly - pos[1])
                else :
                    orientation[1] = 0

            newx = int(pos[0]+orientation[0])
            newy = int(pos[1]+orientation[1])
            local = self.table[int(pos[0]) - 1 : int(pos[0]) + 2, int(pos[1]) - 1 : int(pos[1]) + 2]
            


            

            if self.table[newx][newy] == 9 :
                path.append(pos)
                searching = False
                for i in path :
                    self.table[int(i[0])][int(i[1])] = 9
                path, history_local = [], []
                self.label.setText("Found !")

            elif 0 in local :
                if self.table[newx][newy] == 0 :
                    path.append(pos)
                    pos = pos + orientation
                    self.table[newx][newy] = 8
                    newpath = True
                    history_local.append(copy.deepcopy(local))

                elif self.table[newx][newy] != 0 and self.table[newx][newy] != 9 :
                    newpath = False

                    possibilities = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
                    val = possibilities.index((orientation[0], orientation[1]))
                    for i in range(1, len(possibilities)) :
                        newx = int(pos[0]+possibilities[(val + i)%len(possibilities)][0])
                        newy = int(pos[1]+possibilities[(val + i)%len(possibilities)][1])
                        if self.table[newx][newy] == 0 :
                            orientation = np.array((possibilities[(val + i)%len(possibilities)][0], possibilities[(val + i)%len(possibilities)][1]))
                            break

                        elif self.table[int(pos[0]+possibilities[val - i][0])][int(pos[1]+possibilities[val - i][1])] == 0 :
                            orientation = np.array((possibilities[val - i][0], possibilities[val - i][1]))
                            break
            
            else :
                backing = True
                history_local.append(copy.deepcopy(local))
                path.append(pos)
                c = 0
                pos = np.array([startx, starty])
                while backing :
                    v, w = int(path[-1-c][0]), int(path[-1-c][1])
                    print(v, w)
                    self.table[v][w] = 99
                    if 0 in history_local[-1-c] or c == len(path) :
                        backing = False
                        pos = path[-1 - c]
                        for x in range(c+1) :
                            path.pop()
                    else :     
                        c += 1
               
                self.table[startx][starty] = 8

            self.draw(self.table)
        
        

if __name__ == "__main__":
    gol_state, pathstart, pathend, pathready, searching = False, False, False, False, False
    startx, starty, goalx, goaly, distancex, distancey = 0, 0, 0, 0, 0, 0
    Toriginal = []
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())