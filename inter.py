from PyQt5 import QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, qApp, QFileDialog, QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView)
from PyQt5.QtGui import QIcon
import sys
import main
import pandas
import matplotlib.pyplot as plt


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.models = []
        self.diets = []
        self.Equi = False
        self.Dict = False    
        self.initUI()

    def initUI(self):      

        self.datatable = QTableWidget()
        self.setCentralWidget(self.datatable)
        self.statusBar()
    
        exitAct = QAction(QIcon('/Data/Icons/exit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit the App')
        exitAct.triggered.connect(qApp.quit)

        menuGo = QAction(QIcon('/Data/Icons/run.png'), 'Go', self)
        menuGo.setShortcut('Ctrl+G')
        menuGo.setStatusTip('Run the program')
        menuGo.triggered.connect(self.go)

        openDiet = QAction(QIcon('/Data/Icons/open.png'), 'Choose Diet', self)
        openDiet.setShortcut('Ctrl+D')
        openDiet.setStatusTip('Select the diets')
        openDiet.triggered.connect(self.ajouterDiets)

        openModel = QAction(QIcon('/Data/Icons/open.png'), 'Choose Model', self)
        openModel.setShortcut('Ctrl+M')
        openModel.setStatusTip('Select the models')
        openModel.triggered.connect(self.ajouterModels)

        exportEqui = QAction(QIcon('open.png'), 'Export equivalences to xls', self, checkable = True)
        exportEqui.setChecked(True)
        exportEqui.setStatusTip('Export equivalences to xls')
        exportEqui.triggered.connect(self.activerEqui_xls)

        exportDict = QAction(QIcon('open.png'), 'Export dictionary to xls', self, checkable = True)
        exportDict.setChecked(True)
        exportDict.setStatusTip('Export dictionary to xls')
        exportDict.triggered.connect(self.activerDict_xls)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)
        self.toolbar.addAction(menuGo)
        self.toolbar.addAction(openModel)
        
        menubar = self.menuBar()
        menuModel = menubar.addMenu('&Model')
        menuModel.addAction(openModel)
        menuDiet = menubar.addMenu('&Diet')
        menuDiet.addAction(openDiet)
        menuOptions = menubar.addMenu('&Options')
        menuOptions.addAction(exportEqui)
        menuOptions.addAction(exportDict)

        
        self.setGeometry(600, 600, 700, 600)
        self.setWindowTitle('Modelisation')
        
        self.show()
        
    
    def ajouterModels(self):

        fnames = QFileDialog.getOpenFileNames(self, 'Open file', '/home/eric/Projectes/ProjecteBio/Models/Models')
        l= []
        for name in fnames[0]:
            l.append(name)
             
        self.models = l

    def ajouterDiets(self):

        fnames = QFileDialog.getOpenFileNames(self, 'Open file', '/home/eric/Projectes/ProjecteBio/Models/dietes')
        l= []
        for name in fnames[0] :
            l.append(name)       
        self.diets = l
        print(self.diets)

    def activerDict_xls(self):
        self.Dict = True

    def activerEqui_xls(self):
        self.Equi = True
        
    def go(self):
        self.df = main.main(self.diets, self.models, self.Dict, self.Equi)
        mod = list(self.df)
        die = list(self.df.index)
        print(self.df)
        self.datatable.setColumnCount(len(self.df.columns)+1)
        self.datatable.setRowCount(len(self.df.index)+1)
        self.buttons = []
        k = 0
        for i in range(len(die)):
            print("d:" + str(i))
            #posem el titol de les files
            Vheader = QTableWidgetItem(die[i])
            self.datatable.setVerticalHeaderItem(i, Vheader)

            for j in range(len(mod)):
                #posar l'element
                n = QTableWidgetItem(str(self.df.get_value(die[i],mod[j])))
                self.datatable.setItem(i,j,n)
                #posar el titol a la columna
                self.datatable.setHorizontalHeaderItem(j,QTableWidgetItem(mod[j]))                
            self.buttons.append(k)
            self.buttons[k]=QtWidgets.QPushButton('dGraph')
            self.buttons[k].clicked.connect(self.dGraphiquer)
            self.datatable.setCellWidget(i,j+1,self.buttons[k])
            header = self.datatable.horizontalHeader()
            k = k+1

        for j in range(len(mod)):
            self.buttons.append(k)
            self.buttons[k]=QtWidgets.QPushButton('mGraph')
            self.buttons[k].clicked.connect(self.mGraphiquer)
            self.datatable.setCellWidget(len(die),j,self.buttons[k])
            k = k+1

        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for i in range(1, len(mod)):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

    def mGraphiquer(self):
        buttonClicked = self.sender()
        index = self.datatable.indexAt(buttonClicked.pos())
        print("BIOOO")
        print(index.row())
        print(index.column())
        print("STIIIC")
        nd = {}
        mod = list(self.df)
        die = list(self.df.index)
        for diet in die:
            nd[diet] = self.df[mod[index.column()]][diet]
        dafr = pandas.DataFrame.from_dict(nd, orient='index')
        dafr.plot(kind='bar')
        plt.suptitle(mod[index.column()])
        plt.show()

    def dGraphiquer(self):
        buttonClicked = self.sender()
        index = self.datatable.indexAt(buttonClicked.pos())
        print("BIOOO")
        print(index.row())
        print(index.column())
        print("STIIIC")
        nd = {}
        mod = list(self.df)
        die = list(self.df.index)
        for model in mod:
            nd[model] = self.df[model][die[index.row()]]
        dafr = pandas.DataFrame.from_dict(nd, orient='index')
        dafr.plot(kind='bar')
        plt.suptitle(die[index.row()])
        plt.show()
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


