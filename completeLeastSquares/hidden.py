'''
Created on Apr 28, 2014

@author: Craig Ferguson FRGCRA003
'''
from LeastSquaresProject.points import Points
from LeastSquaresProject.weights import Weights
from completeLeastSquares.provisional import *
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def Hidden(obsFile,controlFile,saveAs,SitholeExcelFormat,DirectionsW,DistanceW,showgraph,iterations,showGlobalCheckForIterations):
    
    ##_________________________________________________________________________________All functions used for the adjustment F3 in eclipse to 'goto' function
    
    np.set_printoptions(precision=3)
    np.set_printoptions(linewidth=2000)
    np.set_printoptions(suppress=True)
    numpy.set_printoptions(threshold=1000)
    N,stationsOrder=Observations(obsFile)
    control = controlPoints(N,controlFile)
#     N,control=Test(0)
    unknowns=getUnknowns(N,control)
    provisionals= getProvisionals(N,control,unknowns) 
    obs=getObs(N)
    obs=obsSplit(obs)
    L,Lnames=getL(provisionals,obs,control)
    A=getA(provisionals,obs,control,unknowns)
    Pob= Weights()
    Pob.setDirectionWeight(DirectionsW)
    Pob.setDistanceWeight(DistanceW)
    P=Pob.matrix(obs,A)
    X=(A.T*P*A)**-1*A.T*P*L
    Xdict=Points("Solutions Dictionary")
    j=0
    for i in unknowns:
        Xdict[i]=X[j]
        j+=1
        
    V,posteriori,covarience_mat,precisi=precisions(A,X,P,L,obs,unknowns)
    
    provis=adjustProvisional(Xdict,provisionals,obs, unknowns)
    
    
#________________________________________________________________________________________________________FILE WRITING AND ITERATION



    file = open(saveAs, "w")
    file.write("________CONTROL POINTS________\n\n")
    for i,j in control.iteritems():
        file.write(i +":\n"+ str(j)+"\n")
    file.write("________UNKNOWNS________\n\n")
    file.write(str(unknowns)+'\n\n')
    file.write("_______________________________________ CALCULATIONS _______________________________________ \n\n\n\n")


    k=0  
    print "________Calculating>>>>>>>>>>>>>>>>>>>>>>>....................."
    for i in range (iterations):
        k+=1
        provis=adjustProvisional(Xdict,provis, obs, unknowns)
        A,Xdict,provis,obs,control,unknowns,L=Iterate(provis, obs, control, unknowns,P)
        X=((A.T*P*A)**-1)*A.T*P*L
        Xdict=Points("Solutions Dictionary")
        j=0
        for i in unknowns:
            Xdict[i]=X[j]
            j+=1
        V,posteriori,covarience_mat,precisi=precisions(A,X,P,L,obs,unknowns)
        
        file.write("________ITERATION: "+str(k)+" ________\n\n")

        if float(round(float((A.T*P*V).T*(A.T*P*V)),6))==0.:
            file.write("____________________________________________________\n\nCalculation check 'A.tPV' successful\n---------------------------------------------\n")
        else:
            file.write("Calculation check 'A.tPV' unsuccessful to 6 dec places\n\n")
        
    #     V,posteriori,covarience_mat,precisions
        file.write("________'V.TPV'________\n\n")
        file.write(str(V.T*P*V)+'\n\n')    
        file.write("________Posteriori________\n\n")
        file.write(str(posteriori)+'\n\n') 
#         file.write("________Covarience Matrix________\n\n")   #    COVARIENCE MATRIX
#         file.write(str(covarience_mat)+'\n\n')  
        file.write("________Precisions of Unknowns ________\n\n")
        for i,j in precisi.iteritems():
            file.write(i +":\n"+ str(round(float(j),3))+"\n\n")
        print "__finished "+str(k) + " iterations__"
        if showGlobalCheckForIterations:
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

    
    #"observed direction( "+str(target.distance)+") + "+"residual: ("+str(float(V[i]))+")-"+"new calculated direction ("+ str(newD)+") = " + str(round(float(target.distance + V[i] - newD),2))
    check=globalCheck(provis,control,V,obs,unknowns,Xdict)
    print provis
    file.close()
    
    if showgraph:
        showGraph(N,provis,control)
#     showGraph(N,provisionals,control)
   
    

    