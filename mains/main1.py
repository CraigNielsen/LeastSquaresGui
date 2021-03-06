from __future__ import with_statement

from collections import OrderedDict
import csv
import os
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.Qt import QTableWidgetItem, QFileDialog, QTreeWidgetItem, Qt,\
    QTreeWidgetItemIterator, QCoreApplication, QWidget, QGridLayout,\
    QObjectCleanupHandler
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
from matplotlib.pyplot import figure
from numpy import sqrt
import xlsxwriter

from LeastSquaresProject.display import rad2dms, dec2dms
from LeastSquaresProject.points import Points
from LeastSquaresProject.weights import Weights
from completeLeastSquares.provisional import Observations, getObs, obsSplit,\
    controlPoints, getUnknowns, getProvisionals, getL, getA, precisions,\
    adjustProvisional, Iterate, ErrorEllipse, bowditchAdjust, globalCheck
from leastSqr import Ui_MainWindow
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


# from mplwidget import MplCanvas
# Qt4 bindings for core Qt functionalities (non-GUI)
# Python Qt4 bindings for GUI objects
# import the MainWindow widget from the converted .ui files
class DesignerMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent = None):
        # initialization of the superclass

        super(DesignerMainWindow, self).__init__(parent)
        # setup the GUI --> function generated by pyuic4
        self.setupUi(self)
        # connect the signals with the slots
        self.ControlButton.setVisible(False)
        self.backup=False
        self.setWindowTitle("Craigs Least Squares Program")
        self.saveProvisButton.setVisible(False)
        self.hasLayOUT=False
        self.bowditch.setVisible(False)
        self.numcheckLabel.setVisible(False)
        self.updateObs.setVisible(False)
        self.updateControl.setVisible(False)
        self.glocheckLabel.setVisible(False)
        self.vtpvLabel.setVisible(False)
        self.posteriori.setVisible(False)
        self.posteriori_2.setVisible(False)
        self.nodeg.setVisible(False)
        self.amount=100
        self.zoomValue=1
        self.show_control=True
        #connections
#         QtCore.QObject.connect(self.commandLinkButton_3, QtCore.
#         SIGNAL("clicked()"),self.on_pushButtonLoad_clicked)
        self.getObsButton.clicked.connect(self.loadObs)

        self.getControlButton.clicked.connect(self.loadControl)
        self.updateControl.clicked.connect(self.loadupControl)
        self.CalcProvisionals.clicked.connect(self.calcProv)
        self.treeObs.itemClicked.connect(self.processItem)
        self.treeObs.itemClicked.connect(self.clik)
        self.solveButton.clicked.connect(self.solve)
        self.ControlButton.clicked.connect(self.update1)
        self.scaleDial.valueChanged.connect(self.dial)
        self.zoom.valueChanged.connect(self.zooming)
        self.saveProvisButton.clicked.connect(self.saveToFile)
        self.bowditch.clicked.connect(self.saveToFileBowditch)
        self.showObsBut.clicked.connect(self.backToObs)
        self.nodeg.clicked.connect(self.calcProv)
        self.saveAll.clicked.connect(self.writeOut)
        self.updateObs.clicked.connect(self.updateObsFunc)
        self.helpButton.clicked.connect(self.helpOpen)
#         self.treeObs.itemChanged.connect(self.turnon)
        self.tabWidget.currentChanged.connect(self.updateObsFunc)
    
    
    def helpOpen(self):
        os.startfile("Help File.pdf")
    def backToObs(self):
        self.tabWidget.setCurrentIndex(0)
        self.calcProv()
    def clik(self):
        self.CalcProvisionals.setEnabled(True)
        self.updateObsFunc()
        self.loadupControl()
        self.updateGraph()
        
    def updateObsFunc(self):
        
        root = self.treeObs.invisibleRootItem()
        child_count = root.childCount()
        remObsList=[]
        for i in range(child_count):
            item = root.child(i)
            url = item.text(0) # text at first (0) column
            j=item.childCount()
            for chil in range (j):
                child=item.child(chil)
                state= child.checkState(0)
                if state ==Qt.Unchecked:

                    if child.text(2)=='':
                        remObsList.append(["distance",str(item.text(0)),str(child.text(1))])
                    elif child.text(3)=='':
                        remObsList.append(["direction",str(item.text(0)),str(child.text(1))])
                
        if self.backup==False:
            self.Nbackup=self.N.copy()
            self.stationsOrderbackup=[]
            self.obsOrderbackup=[]
            for i in self.stationsOrder:
                self.stationsOrderbackup.append(i)
  
            for i in self.obsOrder:
                self.obsOrderbackup.append(i)
            self.backup=True
                
        self.N=self.Nbackup.copy()       
        if len(remObsList)>0:        
            self.N,self.stationsOrder,self.obsOrder = self.changeN(remObsList)
#         for u,v,d in self.N.edges_iter(data=True):
#             print u
#             print v
#             print d  
            
        N=self.N
        self.obs1,self.ObsList=getObs(N)
        self.obs=obsSplit(self.obs1)
#             item.setText(1, 'result from %s' % url) # update result column (1)
    
    
    
    def changeN(self,remObsList):
#         for u,v,d in self.N.edges_iter(data=True):
#             print u
#             print v
#             print d
        for i in remObsList:
              
            del self.N.edge[i[1]][i[2]][i[1]][i[0]]
            if len(self.N.get_edge_data(i[1],i[2],i[1]))==0:
                self.N.remove_edge(i[1],i[2])
        keys={}
        for u,v,d in self.N.edges_iter(data=True):
            keys[u]=None
            keys[v]=None
            
        for v,d in self.N.nodes_iter(data=True):
            if not keys.has_key(v):
                
                self.N.remove_node(v)
        
        return  self.N,self.stationsOrder,self.obsOrder
    def zooming(self):
        self.zoomValue=self.zoom.value()
        self.setWindowSize()
        self.update0()
        
    def dial(self):
        self.amount=self.scaleDial.value()*500
        self.update0()
    def loadCsv(self, fileName):
        self.model.clear()
        with open(fileName, "rb") as fileInput:
            for row in csv.reader(fileInput):    
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)
    def saveToFile(self):
        fileName = QFileDialog.getSaveFileName(self,
                "Open Points File",
                "",
                "All Files (*);;Text Files (*.txt);;Excel (*.xlsx)", "")
        if fileName[-4:]==".txt":
            f = open(fileName, 'w')  
            f.write("            Y             X  \n") 
            for i,j in self.provisionals.iteritems():
                f.write(i +":    "+" "+ str(round(float(j.y),3))+"     "+ str(round(float(j.x),3))+"\n\n")
            f.close()
        elif fileName[-5:]==".xlsx":
            fileName=str(fileName)
            workbook = xlsxwriter.Workbook(fileName)
            worksheet = workbook.add_worksheet()
            i=0
            for nm,j in sorted(self.provisionals.iteritems()):
                worksheet.write(i,0, nm)
                worksheet.write(i,1, (round(float(j.y),3)))
                worksheet.write(i,2, (round(float(j.x),3)))
                i+=1
                
            workbook.close()
            
    def saveToFileBowditch(self):
        
        ''' the bowditch needs to be setup such that the final coordinate is a known point, a single letter, then the reference 
        will be in the next 2 rows, with a dash next to the single letter'''
        fileName = QFileDialog.getSaveFileName(self,
                "Open Points File",
                "",
                "Excel (*.xlsx)", "")
        dX,dY=bowditchAdjust(self.provisionals,self.control,self.obsOrder[-1][4:])
        self.bowditch.setText("not completed yet.")
        sumDistance=0
        
        for i,j in self.obs1.iteritems():
            
            for p,t in j.iteritems():
                if self.provisionals.has_key(p):
                    sumDistance=sumDistance+t.distance
        
        dX=dX/sumDistance        
        dY=dY/sumDistance        
        fileName=str(fileName)
        workbook = xlsxwriter.Workbook(fileName)
        worksheet = workbook.add_worksheet()
        i=0
        worksheet.write(0,0, 'Leg')
        worksheet.write(0,1, 'Dir/OrCorr./Dis')
        worksheet.write(0,2, 'Name')
        worksheet.write(0,3, 'Y')
        worksheet.write(0,4, 'X')
        worksheet.write(2,2, self.control[self.stationsOrder[0]].name)
        worksheet.write(2,3, self.control[self.stationsOrder[0]].y)
        worksheet.write(2,4, self.control[self.stationsOrder[0]].x)
        i+=4
        temp=self.stationsOrder[0]
        soFar=0
        format = workbook.add_format()
        format.set_underline()
    
       
        for nm3 in self.stationsOrder:
            for nm,ob in self.obs1[nm3].iteritems():
                if self.provisionals.has_key(nm):
                    worksheet.write(i,0, nm3+"-"+nm)
                    worksheet.write(i,1, rad2dms(self.obs1[nm3][nm].direction))
                    worksheet.write(i,2, nm)
                
                    worksheet.write(i,3, round(self.provisionals[nm].y,3))
                    worksheet.write(i,4, round(self.provisionals[nm].x,3))
                    i+=1
                    ldist=self.obs1[nm3][nm].distance
                    soFar+=ldist
                    worksheet.write(i,3,soFar*dY)
                    worksheet.write(i,4,soFar*dX)
                    i+=1
                    worksheet.write(i,1, str(round(self.obs1[nm3][nm].distance,2))+"m")
                    worksheet.write(i,2, nm,format)
                    worksheet.write(i,3, round(self.provisionals[nm].y+soFar*dY,2),format)
                    worksheet.write(i,4, round(self.provisionals[nm].x+soFar*dX,2),format)
                    i+=2
                    
                    temp=nm
            
        workbook.close()
#         if fileName:
#             f = open(fileName, 'w')  
#             f.write("            Y             X  \n") 
#             for i,j in self.provisionals.iteritems():
#                 f.write(i +":    "+" "+ str(round(float(j.y),3))+"     "+ str(round(float(j.x),3))+"\n\n")
#             f.close()
    def loadObs(self):
        self.CalcProvisionals.setEnabled(True)
        fileName = QFileDialog.getOpenFileName(self,
                "Open Points File",
                "",
                "All Files (*);;Text Files (*.txt)", "")
        if fileName:
#             self.lineEditPoints.setText(fileName)
            self.treeObs.clear()
            self.readObsFile(fileName)
    def solve(self):
        try:
            if not self.provisionals :
                self.calcProv()
        except: 
            self.calcProv()
        self.bowditch.setVisible(False)
        count=0
        for i,j in self.obs.iteritems():
            count+=len(j.keys())
        self.numberObs=count     
        self.numberUnknowns=len(self.unknowns)
        if self.numberObs-self.numberUnknowns<=0:
            self.nodeg.setVisible(True)
            return
        self.iterations= int(self.iterationLine.text())
        self.iteration()
        
        self.setWindowSize()
        
        self.residuals()
        self.residuals2()
        self.update1()
        self.tabWidget.setCurrentIndex(2)
        
        
            
    def setWindowSize(self):
        maxX= max(data.x for data in self.provis.values())+100*self.zoomValue
        minX= min(data.x for data in self.provis.values())-100*self.zoomValue
        maxY= max(data.y for data in self.provis.values())+100*self.zoomValue
        minY= min(data.y for data in self.provis.values())-100*self.zoomValue
        
        range=max([maxX-minX,maxY-minY])
        self.maxX=minX+range
        self.maxY=minY+range
        self.minX=minX
        self.minY=minY
        
    def update1(self):
        if self.show_control==True:
            self.show_control=False
        elif self.show_control==False:
            self.show_control=True
        self.updateGraph1()
    def update0(self):
        self.updateGraph1()
    def loadupControl(self):
        self.treeControl.clear()
        self.readControlFile(self.CfileName)
    def loadControl(self):
        self.CfileName = QFileDialog.getOpenFileName(self,
                "Open Points File",
                "",
                "All Files (*);;Text Files (*.txt)", "")
        if self.CfileName:
#             self.lineEditPoints.setText(fileName)
            self.treeControl.clear()
            self.readControlFile(self.CfileName)
        self.updateControl.setVisible(True)
    
    def iteration(self):
        weights_distance= self.distanceLine.text()
        weights_direc= self.directionLine.text()
        Pob= Weights(weights_distance, weights_direc)
        L,Lnames=getL(self.provisionals,self.obs,self.control)
        A=getA(self.provisionals,self.obs,self.control,self.unknowns)
        self.P=Pob.matrix(self.obs,A)
        X=(A.T*self.P*A)**-1*A.T*self.P*L
        Xdict=Points("Solutions Dictionary")
        j=0
        for i in self.unknowns:
            Xdict[i]=X[j]
            j+=1
        self.Xdict=Xdict
        self.V,posteriori,covarience_mat,precisi=precisions(A,X,self.P,L,self.obs,self.unknowns)
        self.provis=adjustProvisional(Xdict,self.provisionals,self.obs, self.unknowns)
        k=0
        for i in range (self.iterations):
            k+=1
            provis=adjustProvisional(Xdict,self.provis, self.obs, self.unknowns)
            A,Xdict,provis,obs,control,unknowns,L=Iterate(provis, self.obs, self.control, self.unknowns,self.P)
            X=((A.T*self.P*A)**-1)*A.T*self.P*L
            Xdict=Points("Solutions Dictionary")
            j=0
            for i in unknowns:
                Xdict[i]=X[j]
                j+=1
            V,posteriori,self.covarience_mat,precisi=precisions(A,X,self.P,L,self.obs,unknowns)
        self.XOdict=Points("Orientations Dictionary")
        j=0
        for i in self.unknowns:
            if i[-1]=="o":
                self.XOdict[i]=X[j]
            j+=1
        for i,o in self.XOdict.iteritems():
            print i
            print o
        self.A=A
        self.L=L
        self.posterioriValue=posteriori
        self.V=V
        self.vtpv=float(self.V.T*self.P*self.V)
        self.covarience_mat=covarience_mat
        self.precisi=precisi
        




#     showGraph(N,provisionals,control)
    def provisFind(self):
        
        for i in self.model.takeRow(0):
#             print i.currentText()
            pass
    
    def processItem(self, item, column):
#         print item.text(0), item.text(1), item.checkState(0)
        count= item.childCount()
        state=item.checkState (0)
        if state ==Qt.Unchecked:
            for i in range(count):
                item.child(i).setCheckState (0, Qt.Unchecked)
        if state ==Qt.Checked:
            for i in range(count):
                item.child(i).setCheckState (0, Qt.Checked)
                
    def updateGraph1(self):
        self.canvas.figure.clf() 
#         plt.clf()
        self.CalcProvisionals.setText("FINAL COORDINATES")
        self.CalcProvisionals.setEnabled(False)
        self.updateProv()
        

        pos={}
        for nm,ob in self.provis.iteritems():
            x=ob.x
            y=ob.y
            pos[nm]=  (x,y)         
        for nm,ob in self.control.iteritems():
            x=ob.x
            y=ob.y
            pos[nm]=  (x,y)
        nx.draw_networkx_nodes(self.N,pos,
                           node_color='y',
                           node_size=800,
                           alpha=0)
        T=self.N.copy()
        
                
        if self.show_control==True:
            nx.draw_networkx_nodes(self.N,pos,
                           nodelist=self.control,
                           node_color='r',
                           node_size=50,
                           alpha=0.2)
        else:
            for i,j in self.control.iteritems():
                T.remove_node(i)    
        
        nx.draw(T,pos,node_size=100,alpha=0)      
            
        edges={}
        for v,u,d in self.N.edges(data=True):
            if d.has_key("distance") and d.has_key('direction'):
                edges[v,u]='b'
            
            
        
        nx.draw_networkx_edges(self.N,pos,
                       edgelist=edges,
                       width=1,alpha=0.5,edge_color='b')
#         ellipse = mpl.patches.Ellipse(xy=(self.control['SUR09'].x,self.control['SUR09'].y), width=1000, height=100)
        self.ell=self.ellipses()
        for e in self.ell:
            plt.gca().add_patch(e)
        
    #     matplotlib.pyplot.ion()
    #     plt.draw()
#         self.axis.autoscale(True, axis='both', tight=True)
#         self.canvas.figure.autoscale_view(tight=None, scalex=True, scaley=True)
        self.figure.set_visible(True)
#         self.axes[0]_subplotspec_gridspec.set_hspace
        self.figure.axes[0].autoscale(tight=True)
        self.figure.axes[0].set_xlim((self.minX, self.maxX))
        self.figure.axes[0].set_ylim((self.minY, self.maxY))
        self.figure.axes[0].set_ylim((self.minY, self.maxY))
#         self.figure.set_tight(True)
        self.figure.set_tight_layout(tight=True)
        self.canvas.draw()   
        self.ControlButton.setVisible(True)
        
    def ellipses(self):
            
            list=[]
#             list=[Ellipse(xy=(j.x,j.y), width=1000, height=100, angle=45)
#             for i,j in self.provis.iteritems()]
#             return list
            print self.resid
            for i,j in self.provis.iteritems():
                xlocation=temp=self.unknowns.index(i+"_x")
                ylocation=temp=self.unknowns.index(i+"_y")
                Qx=float(self.covarience_mat[xlocation,xlocation])
                Qy=float(self.covarience_mat[ylocation,ylocation])
                Qxy=self.covarience_mat[xlocation,ylocation]
                
                x,y,a=ErrorEllipse(self.posterioriValue, Qx,Qy,Qxy)
                
                list.append(Ellipse(xy=(j.x,j.y), width=x*self.amount, height=y*self.amount, angle=a))    
            return list
            

    def reLayout(self):
            QWidget().setLayout(self.layout())
            layout = QGridLayout(self) 

    def clearLayout(self):
        if self.layout is not None:
            while self.layout.count():
                item = self.layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())      
        
    def updateGraph(self):
#         try:
#             self.graph.clear()
#             print 'yes'
#         except AttributeError:
#             print "error"
#         else:
#             pass
#         QtGui.QWidget.__init__(self)
#         self.canvas = MplCanvas()
#         #We instantiate the Matplotlib canvas object.
#         self.vbl = QtGui.QVBoxLayout()
#         #Here, we create a layout manager (in this case a vertical box).
#         self.vbl.addWidget(self.canvas)
#         # We add the Matplotlib canvas to the layout manager.
#         self.graph.setLayout(self.vbl)
#         # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

#         self.canvas.clf()
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        
#         self.layout.reLayout()
        if self.hasLayOUT==True:
            self.clearLayout()
        if self.hasLayOUT==False:
            self.layout = QtGui.QVBoxLayout()
        self.hasLayOUT=True
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
#         self.graph.layout().deleteLater()
        self.graph.setLayout(self.layout)
        self.ControlButton.setVisible(False)
        pos={}
        for nm,ob in self.provisionals.iteritems():
            x=ob.x
            y=ob.y
            pos[nm]=  (x,y)         
        for nm,ob in self.control.iteritems():
            x=ob.x
            y=ob.y
            pos[nm]=  (x,y)
        nx.draw_networkx_nodes(self.N,pos,
                           node_color='y',
                           node_size=800,
                           alpha=1)
        nx.draw_networkx_nodes(self.N,pos,
                       nodelist=self.control,
                       node_color='r',
                       node_size=800,
                       alpha=1)
        
#         ellipse = mpl.patches.Ellipse(xy=(58305,49663), width=1000, height=1000)
#         fig,ax = plt.subplots()
# #         self.figure.add_artist(ellipse) 
#         nx.draw_networkx_nodes(ellipse, xy=(self.control['SUR09'].x,self.control['SUR09'].y))
        edges={}
        for v,u,d in self.N.edges(data=True):
            if d.has_key("distance") and d.has_key('direction'):
                edges[v,u]='b'
#         fig = figure()
#         ax = fig.add_subplot(111, aspect='equal')
#         e=(Ellipse((self.control['SUR09'].x,self.control['SUR09'].y), width=100, height=5, angle=45))    
#         ax.add_artist(e)
#         plt.plot(self.control['SUR09'].x,self.control['SUR09'].y,'g.', markersize=100.0)                  #([e], [e], 'g.', markersize=20.0) 
          
        nx.draw(self.N,pos)
        nx.draw_networkx_edges(self.N,pos,
                       edgelist=edges,
                       width=8,alpha=0.5,edge_color='b')
#         nx.draw(Ellipse((self.control['SUR09'].x,self.control['SUR09'].y), width=100, height=5, angle=45,edgecolor=('green')))
        
        plt.axis('scaled')
#         nx.set_aspect('auto')
        
#         forceAspect(nx,aspect=1)
#         plt.show()
#         nx.draw(ellipse)
#         nx.add_artist(ellipse)
    #     matplotlib.pyplot.ion()
    #     plt.draw()
#         self.canvas.addAction(ellipse)
        QCoreApplication.processEvents()
        self.canvas.draw()
#         plt.draw() 
    def residuals2(self):
        self.AObs=self.posterioriValue*self.A*(self.A.T*self.P*self.A)**-1*self.A.T
        self.cofactorM=self.A*(self.A.T*self.P*self.A)**-1*self.A.T
        self.AResObs=self.posterioriValue*(self.P**-1 - self.A*(self.A.T*self.P*self.A)**-1*self.A.T)
#         print (self.A.T*self.P*self.A)**-1
#         print self.posterioriValue
#         print self.posterioriValue*(self.A.T*self.P*self.A)**-1
        self.cofactorAObs.clear()
        self.cofactorZ.clear()
        self.residA=OrderedDict()
        self.residARe=OrderedDict()
#         print self.cofactorM   
        count = 0
        for i,j in self.obs.iteritems():
            for k,l in j.iteritems():
                count+=1
        self.obsCount=count
        self.cofactorAObs.setColumnCount(count)
        self.cofactorAObs.setRowCount(count)
        self.cofactorZ.setColumnCount(count)
        self.cofactorZ.setRowCount(count)
        for i in range (count):
            for j in range (count):
                temp=QTableWidgetItem()
                temp.setText(str(self.cofactorM[i,j]))
                self.cofactorAObs.setItem(i,j,temp)
        for i in range (count):
            for j in range (count):
                temp=QTableWidgetItem()
                temp.setText(str(self.AResObs[i,j]))
                self.cofactorZ.setItem(i,j,temp)
        i=0
        for x,sta in self.obs.iteritems():
            for tn,tar in sta.iteritems():

                name=x
    #             name=x[0:-2]
                if not self.residA.has_key(x+tn):
                    self.residA[x+tn]=[None]
                if not self.residARe.has_key(x+tn):
                    self.residARe[x+tn]=[None]
                
    
                self.residA[x+tn][0]=sqrt(self.AObs[i,i])
                self.residARe[x+tn][0]=sqrt(self.AResObs[i,i])
                i+=1
#         print self.residA
#         print self.residARe
        for x,sta in self.obs.iteritems():
           for tn,target in sta.iteritems(): 
                name=x+tn
                item1 = QTreeWidgetItem(self.stdDevAtree)
                item2 = QTreeWidgetItem(self.stdDevObsTree)
                if tn[-1]=="D":
                    item1.setText(0, "Direction from"+ x +"to :"+tn[0:-2])
                    item2.setText(0,"Direction from"+ x+"to :"+tn[0:-2])
                elif tn[-1]=="d":
                    item1.setText(0, "Distance from"+ x+"to :"+tn[0:-2])
                    item2.setText(0,"Distance from"+ x+"to :"+tn[0:-2])
                    
                    
                    
                item1.setText(1, str(round(float(self.residA[name][0]),3)))
                item2.setText(1, str(round(float(self.residARe[name][0]),3)))
#             if not (self.resid[name][0])==None:
#                 item.setText(1, str(round(float(self.resid[name][0]),3)))
#                 
#             if not (self.resid[name][1])==None:
# 
#                 item.setText(2, str(round(float(self.resid[name][1]),3)))
#                
#             if not (self.resid[name][2])==None:
#                 item.setText(3, str(round(float(self.resid[name][2]),3)))
#                 if (self.resid[name][0])==None and (self.resid[name][1])==None:
#                     item.setText(0, name+"(control)")   
                     
    def residuals(self):
        self.stdDevTree.clear()
        self.resid={}
        for x in self.unknowns:
            list=[]
            
            name=x[0:-2]
            item = QTreeWidgetItem(self.stdDevTree)
            item.setText(0, name)
            if not self.resid.has_key(name):
                self.resid[name]=[None,None,None]
            
            if x[-1]=="o":
                self.resid[name][2]=(self.precisi[name+"_o"])
                item.setText(3, str(round(float(self.resid[name][2]),3)))
                
            elif x[-1]=="x":
                self.resid[name][0]=(self.precisi[name+"_x"])
                item.setText(1, str(round(float(self.resid[name][0]),3)))
                
                
            elif x[-1]=="y":
                self.resid[name][1]=(self.precisi[name+"_y"])
                item.setText(2, str(round(float(self.resid[name][1]),3)))
                
        for name in self.unknowns:
            name=x[0:-2]
               
            if not (self.resid[name][2])==None:
                
                if (self.resid[name][0])==None and (self.resid[name][1])==None:
                        item.setText(0, name+"(control)")
        
        self.vtpvLabel.setText("VTPV: "+str(self.vtpv))
        self.vtpvLabel.setVisible(True)
        if float(round(float((self.A.T*self.P*self.V).T*(self.A.T*self.P*self.V)),6))==0.:
            self.numcheckLabel.setVisible(True)
        self.posteriori.setText("Posteriori: "+str(self.posterioriValue))
        self.posteriori.setVisible(True)
        self.posteriori_2.setText(str(round(self.posterioriValue,5)))
        self.posteriori_2.setVisible(True)
        check1=globalCheck(self.provis,self.control,self.V,self.obs,self.unknowns,self.Xdict)
        for x,ob in self.XOdict.iteritems():
            list=[]
            name=x[0:-2]
            item = QTreeWidgetItem(self.stdDevTree)
            item.setText(0, name+" orientation:")
            item.setText(3, str(round(float(self.XOdict[x]),3)))
        sum=0
        for i in check1.values():
            sum+=round(i,4)
        if round(sum,3)==0.:
            self.glocheckLabel.setVisible(True)
        else:
            self.glocheckLabel.setText("GLOBAL UNSUCCESS")       
#             self.glocheckLabel.setStyleSheet(color="red")     
            self.glocheckLabel.setVisible(True) 
              

        
        
    def calcProv(self):
        self.nodeg.setVisible(False)
        self.unknowns=getUnknowns(self.N,self.control)
        self.provisionals= getProvisionals(self.N,self.control,self.unknowns) 
        self.treeProvis.clear()
        self.saveProvisButton.setVisible(True)
        self.bowditch.setVisible(True)
#         for name in self.stationsOrder:
#             item = QTreeWidgetItem(self.treeProvis)
#             item.setText(0, name)
#             
#             
#             item.setText(1, str(round(self.provisionals[name].x,3)))
#             item.setText(2, str(round(self.provisionals[name].y,3)))
#             item.setText(3, str(round(self.provisionals[name].h,3)))
            
        for x,y in self.provisionals.iteritems():
            item = QTreeWidgetItem(self.treeProvis)
            item.setText(0, x)
            item.setText(1, str(round(y.y,3)))
            item.setText(2, str(round(y.x,3)))
            item.setText(3, str(round(y.h,3)))
        self.updateGraph()
    def updateProv(self):
        self.treeProvis.clear()
        for x,y in self.provis.iteritems():
            item = QTreeWidgetItem(self.treeProvis)
            item.setText(0, x)
            item.setText(1, str(round(y.y,3)))
            item.setText(2, str(round(y.x,3)))
            item.setText(3, str(round(y.h,3)))
            
#     @QtCore.pyqtSlot()
#     def on_pushButtonLoad_clicked(self):
#         self.loadCsv('E:\==Programming==\==Python Projects==\Assignment2\==MAIN and Report==\complete12345.csv')                
#     @QtCore.pyqtSlot()
#     def on_pushButtonLoad1_clicked(self):
#         self.loadCsv1('E:\==Programming==\==Python Projects==\Assignment2\==MAIN and Report==\controlTest.csv')                
#     @QtCore.pyqtSlot()
#     def on_pushButtonLoad3_clicked(self):
#         self.provisFind()                
   
    def readObsFile(self, filename):
        self.N,self.stationsOrder,self.obsOrder = Observations(filename)
        N=self.N
        self.obs1,self.ObsList=getObs(N)
        self.obs=obsSplit(self.obs1)
        for name in self.stationsOrder:
            item = QTreeWidgetItem(self.treeObs)
            item.setText(0, name)
            
            for t,j in self.obs[name].iteritems():
                subitem=QTreeWidgetItem(item)
                subitem.setText(1, t[0:-2])
                if j.type=='direction':
                    subitem.setText(2,str( rad2dms(j.direction))) 
                    subitem.setCheckState(0, Qt.Checked)          
                if j.type=='distance':
                    subitem.setCheckState(0, Qt.Checked)
                    subitem.setText(3, str(j.distance))
                if j.type=='both':
                    subitem.setText(2,str( rad2dms(j.direction))) 
                    subitem.setCheckState(0, Qt.Checked)
                    subitem.setText(3, str(j.distance))
                item.setCheckState(0, Qt.Checked)
#         for x,y in self.obs.iteritems():
#             #print coord
#             item = QTreeWidgetItem(self.treeObs)
#             item.setText(0, x)
#             
# #             if x[2] == 0:
# #                 item.setCheckState(0, Qt.Unchecked)
# #             else:
# #                 item.setCheckState(0, Qt.Checked)
#             for t,j in y.iteritems():
#                 subitem=QTreeWidgetItem(item)
#                 subitem.setText(1, t)
#                 if j.type=='direction':
#                     subitem.setText(2,str( rad2dms(j.direction))) 
#                     subitem.setCheckState(0, Qt.Checked)          
#                 if j.type=='distance':
#                     subitem.setCheckState(0, Qt.Checked)
#                     subitem.setText(3, str(j.distance))
#                 if j.type=='both':
#                     subitem.setText(2,str( rad2dms(j.direction))) 
#                     subitem.setCheckState(0, Qt.Checked)
#                     subitem.setText(3, str(j.distance))
#                 item.setCheckState(0, Qt.Checked)        
    def readControlFile(self, filename):
        self.control = controlPoints(self.N,filename)
#         obs=obsSplit(obs)
        for x,y in self.control.iteritems():
            #print coord
            item = QTreeWidgetItem(self.treeControl)
            item.setText(0, x)
            item.setText(1, str(round(y.y,3)))
            item.setText(2, str(round(y.x,3)))
            item.setText(3, str(round(y.h,3)))
            item.setCheckState(0, Qt.Checked)
#             if x[2] == 0:
#                 item.setCheckState(0, Qt.Unchecked)
#             else:
#                 item.setCheckState(0, Qt.Checked)
    def writeOut(self):
        fileName = QFileDialog.getSaveFileName(self,
                "Open Points File",
                "",
                "Text File (*.txt);;", "")
        file = open(fileName, "w")
        file.write("________CONTROL POINTS________\n\n")
        for i,j in self.control.iteritems():
            file.write(i +":\n"+ str(j)+"\n")
        file.write("________UNKNOWNS________\n\n")
        file.write(str(self.unknowns)+'\n\n')
        file.write("_______________________________________ CALCULATIONS _______________________________________ \n\n\n\n")
        k=0  

        for i in range (self.iterations):
            k+=1
            provis=adjustProvisional(self.Xdict,self.provis, self.obs, self.unknowns)
            A,Xdict,provis,obs,control,unknowns,L=Iterate(provis, self.obs, self.control, self.unknowns,self.P)
            X=((A.T*self.P*A)**-1)*A.T*self.P*L
            Xdict=Points("Solutions Dictionary")
            j=0
            for i in unknowns:
                Xdict[i]=X[j]
                j+=1
            V,posteriori,covarience_mat,precisi=precisions(A,X,self.P,L,obs,unknowns)
            
            file.write("________ITERATION: "+str(k)+" ________\n\n")
        
            if float(round(float((A.T*self.P*V).T*(A.T*self.P*V)),6))==0.:
                file.write("____________________________________________________\n\nCalculation check 'A.tPV' successful\n---------------------------------------------\n")
            else:
                file.write("Calculation check 'A.tPV' unsuccessful to 6 dec places\n\n")
            
        #     V,posteriori,covarience_mat,precisions
            file.write("________'V.TPV'________\n\n")
            file.write(str(V.T*self.P*V)+'\n\n')    
            file.write("________Posteriori________\n\n")
            file.write(str(posteriori)+'\n\n') 
        #         file.write("________Covarience Matrix________\n\n")   #    COVARIENCE MATRIX
        #         file.write(str(covarience_mat)+'\n\n')  
            file.write("________Precisions of Unknowns ________\n\n")
            for i,j in precisi.iteritems():
                file.write(i +":\n"+ str(round(float(j),3))+"\n\n")

            
            check=globalCheck(provis,control,V,obs,unknowns,Xdict)
            file.write("________Global Check________\n\n")
            for i,j in check.iteritems():
                file.write(i +":\n"+ str(j)+"\n")
            file.write("________________----   END OF ITERATION "+str(k)+"   ----____________\n\n")
            file.write("_______________________________________________________________________\n\n")
        #     showGraph(N,provisionals,control)
        
        
        file.write("________FINAL COORDINATES________\n\n")
        for i,j in provis.iteritems():
            file.write(i +":\n"+ str(j)+"\n\n")
        
        file.write("________X Solution Vector, With distances in meters and directions in seconds ________\n\n")
        for i,j in Xdict.iteritems():
            file.write(i +":\n"+ str(round(float(j),3))+"\n\n")  
                
if __name__ == '__main__':
#     os.system(r'""convert.bat""')
#     os.system(r'""convertQrc.bat""')
    # create the GUI application
    app = QtGui.QApplication(sys.argv)
    # instantiate the main window
    dmw = DesignerMainWindow()
    # show it
    dmw.show()
    # start the Qt main loop execution, exiting from this script
    # with the same return code of Qt application
    sys.exit(app.exec_())