'''
Created on Mar 17, 2014

@author: 01410541
'''


import math

from numpy import floor, pi, float64, size
import numpy

from Equations import Directions, Distances, equations
from LeastSquaresProject.point import Point
from LeastSquaresProject.surveyData import SurveyData
from LeastSquaresProject.weights import Weights
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from points import Points


numpy.set_printoptions(threshold=numpy.nan)



def LeastSqrRead(inputControl,inputObservations):
    control = Points()
    control.read(inputControl)
    provis = Points()
    np.set_printoptions(precision=12)
    np.set_printoptions(suppress=True)
    np.set_printoptions(linewidth=2000)
    numpy.set_printoptions(threshold=1000)
    print "Reading Obs"
    obs = SurveyData()
    count=obs.read(inputObservations)#reads in file into the surveyData dictionary which contains Target object with two variables
    # determine adjustment information
    unknowns2 = set() # set of text items 
    obsList=[]
    for i,sta in obs.iteritems():
        for j,k in sta.iteritems():
            if k.type=='both':
                obsList.append(i +"-"+ "direction-" +" "+ j)
                obsList.append(i +"-"+ "distance-" +" "+ j)
            else:
                obsList.append(i +"-"+ k.type +" "+ j)
    print obsList
#     knowns = []
    
    for station_name, station in obs.iteritems():
        unknowns2.add(station_name+'_o')
        for target_name, target in station.iteritems():
            if not control.has_key(target_name):
                unknowns2.add(target_name+'_x')
                unknowns2.add(target_name+'_y')
            pass#print target_name, target.direction.
    unknowns=[]
    for i in unknowns2:
        unknowns.append(i)
    print unknowns
    G=nx.MultiGraph()   
    G.add_node(2)
    G.add_node(5)
    G.add_edge(2,3)
    nx.draw(G)
    # Means all distances between points
    print "===             Calculate Mean Distance Observations           =================="

#     for sn1,station1 in obs.iteritems():
#         for sn2,station2 in obs.iteritems():
#             for tn1,target1 in station1.iteritems():
#                 for tn2,target2 in station2.iteritems():
#                     if (not target2.distance==None) and (not target1.distance==None) :
#                         if tn1==sn2 and tn2==sn1:
#                             print tn1,sn1,tn2,sn2
#                             print "distance 1: "+ str(target1.distance) + "\ndistance 2 :" + str(target2.distance)
#                             temp=target1.distance
#                             target1.distance = (target1.distance+target2.distance)/2.0
#                             target2.distance = (temp+target2.distance)/2.0
#                             print "mean: "+ str(target2.distance)
    print "================================================================================="
    print "===             Calculate Provisional Coordinates           =================="

    #give stations coordinates if they're control points
    
    for name,obj in control.iteritems():
        if obs.has_key(name):
            obs[name].setPoint(obj)
    
    
    for sn1,station1 in obs.iteritems():
            
            for tn1,target1 in station1.iteritems():
                if not control.has_key(tn1) and not station1[tn1].distance==None and not station1.point==None:
#                     print "station :"+sn1
                    d= station1[tn1].distance
                    t= station1[tn1].direction
                    x,y,h=station1.point.polar(d,t)
#                     print "target :" + tn1
                    provis.add(tn1,x,y,h,False)
                    obs[tn1].setPoint(provis[tn1])
#                     print   str(obs[tn1].point)
#                     print str(tn1) + str(provis[tn1])
    for i,j in provis.iteritems():
        print i 
        print j
    
    print "================================================================================="
    print "======           Truncate Distances              ==========================================================================="
#     temp=Points()
#     for i,obj in provis.iteritems():
#         temp.add(i,obj.x,obj.y,obj.h,False)
#     for p,obj in temp.iteritems():
#         provis.replace(p,floor(obj.x),floor(obj.y),floor(obj.h),False)
#         print provis[p]
#     
#   
  
    
    print "======================   TESTING   ====================================================="
#     
#     provis.add('U1',58961.,49666.4,0.,False)
#     print provis['U1']
#     provis.add('U2',59120.6,49687.0,0.,False)
#     print provis['U2']
#     provis.add('U3',59295.0,49732.0,0.,False)
#     print provis['U3']
#    
#     
#     
#     print Directions(control['SUR09'],'known',provis['U1trunc'],'unknown','y')
#     print Distances(control['SUR09'],'known',provis['U1trunc'],'unknown','x')
#     print obs['SUR09'].point.joinS(provis['test'])
    print "================================================================================="
    print "======    Calculate Misclosure L      ==========================================="
    L=numpy.zeros(shape=(count,1))
    i=0
    for sn1,station in obs.iteritems():
        for tn1,target in station.iteritems():
            if target.type=="both":
                if control.has_key(tn1):
                    calc=obs[sn1].point.join(control[tn1])
                elif provis.has_key(tn1):
                    calc=obs[sn1].point.join(provis[tn1])
                else: print "error"
                
                
                observed=obs[sn1][tn1].direction
                target.setMisclosure(observed-calc)
                L[i][0]=(observed-calc)*180.*3600./pi
                i+=1
                L[i][0]=obs[sn1][tn1].distance-floor(obs[sn1][tn1].distance)
                print L[i][0]
                i+=1
                continue
            else:
                if control.has_key(tn1):
                    calc=obs[sn1].point.join(control[tn1])
                elif provis.has_key(tn1):
                    calc=obs[sn1].point.join(provis[tn1])
                
                else: print "error"
                observed=obs[sn1][tn1].direction
                target.setMisclosure(observed-calc)
                L[i][0]=(observed-calc)*180.*3600./pi
                i+=1
            print str(sn1) + " " + str(tn1)           
#             print observed
            print ('%0.1f' % float64(target.misclosure*180./math.pi*3600.))    
    print "==============        A Matrix        ========================================="
    print count
    
    A = numpy.zeros(shape=(count,len(unknowns)))
    A[0][0]=3
    i=0
    j=0
    doub=False
    print unknowns
    for at,station in obs.iteritems():
        print at
        if control.has_key(at):station.point.setKnown(True)
        
         
        for atObserved,observ in station.iteritems():
            print "target : " +atObserved +" " + observ.type
            j=0
            if observ.type=='both':
                doub=True
                for at_wrt in unknowns:
                    
                    if at_wrt[-1]=='o':
                        if at==at_wrt[0:-2]:
                            A[i][j]=-1.
                            print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                            j+=1
                            continue
                        else: 
                            A[i][j]=0
                            print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                            j+=1
                            continue
                    if not atObserved==at_wrt[0:-2] and not at==at_wrt[0:-2]: 
    #                     print t
    #                     print at_wrt[0:-2]
                        A[i][j]=0
                        print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                        j+=1
                        continue
                    
                    if control.has_key(atObserved):#if observing control
                        
                            A[i][j]=equations(station.point,control[atObserved],at_wrt,'direction')
                            print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                            
                            A[i+1][j]=equations(station.point,control[atObserved],at_wrt,'distance')
                            print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                            j+=1
                        
                        
                    else:#if observing provisional
                            A[i][j]=equations(station.point,provis[atObserved],at_wrt,'direction')
                            print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                            
                            A[i+1][j]=equations(station.point,provis[atObserved],at_wrt,'distance')
                            print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                            j+=1
            else:
                for at_wrt in unknowns:
                    
                    if at_wrt[-1]=='o':
                        if at==at_wrt[0:-2]:
                            A[i][j]=-1.
                            print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                            j+=1
                            continue
                        else: 
                            A[i][j]=0
                            j+=1
                            continue
                    if not atObserved==at_wrt[0:-2] and not at==at_wrt[0:-2]:
    #                     print t
    #                     print at_wrt[0:-2]
                        A[i][j]=0
                        print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                        j+=1
                        continue
                    
                    if control.has_key(atObserved):#if observing control
                        
                            A[i][j]=equations(station.point,control[atObserved],at_wrt,observ.type)
                            print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                            j+=1
                        
                        
                    else:#if observing provisional
                            A[i][j]=equations(station.point,provis[atObserved],at_wrt,observ.type)
                            print str(i) +" "+ str(j)+ "  :"+ str(A[i][j])
                            j+=1
                
            if doub==True: 
                i+=2
                print "i: " +str(i) 
                
                doub=False
                
            else: 
                i+=1
                print "i: " +str(i) 
    print ""
    print "             U1_y',          'U1_x',      'U3_y',       'U3_x',      'SUR12_o',     'U2_o',       'U2_x',         'U2_y',       'U1_o',       'U3_o',        'SUR09_o' "
    names=[]
    for name,ob in obs.iteritems():
        for na,tar in ob.iteritems():
            if tar.type=="both":
                names.append(name + "-" + na + "D")
                names.append(name + "-" + na + "d")
            else:
                names.append(name + "-" + na + "D")

                
    row_labels = ['SUR09-T013', 'Y', 'N', 'W']
    for row_label, row in zip(names, A):
        print '%s [%s]' % (row_label, '      '.join('%01f' % i for i in row))          
#   except:                   
#                     print "trying"
#                     A[i][j]=equations(station.point,provis[t],at_wrt[-1],types[i])
#           
#            
#         i+=1
#                     
    print A       
    print "==============        Calculate Least squares       ========================================="
    
    Pob= Weights()
    Pob.setDirectionWeight(1)
    Pob.setDistanceWeight(1)
    P=Pob.matrix(obs,A)
    A=numpy.asmatrix(A)
    N= (((A.T)*A)**(-1))*A.T*L
    print "now"
    print A.T*P*L
    for row_label, row in zip(unknowns, N):
        print '%7s [%s]' % (row_label, '      '.join('%07f' % i for i in row)) 
    j=0
#     for name in unknowns:
#         print name[0:-2] + str(+N[i])
#         
#         print name + str(ob.y+N[i])
#         i+=1
#         print ob.x
#         print ob.y
    print unknowns
    print provis
    finalX=Points()
    orientations={}
    for i in unknowns:
        name= i[0:-2]
        variable = i[-1]
        if variable=="o":
            orientations[name]= float64(N[j])
            j+=1
            continue
        x=provis[name].x
        y=provis[name].y
        h=provis[name].h
        if not finalX.has_key(name):
            finalX[name]= Point(0,0,0,False,name)
        if variable=="x":
            finalX[name].ChangeVariable(variable,float64(x+N[j]))
            j+=1
            continue
        if variable=="y":
            finalX[name].ChangeVariable(variable,float64(y+N[j]))
            j+=1
            continue
        if variable=="h":
            finalX[name].ChangeVariable(variable,float64(h+N[j]))
            j+=1
            continue
            
        print finalX[name]
            
#     T=numpy.matrix([[1,2,3],[3,2,3],[3,2,1],[3,2,1]])
#     S=numpy.matrix([[3,2,3],[3,2,1],[3,2,1],[1,2,3]])
#     M=numpy.matrix([[3,2,3],[3,2,1],[1,2,3],[3,2,1]])
#     print T
#     print T.T*T
#     print S.T*S
#     print M.T*M
#     print A.T*P*L
#     print T*T.T
    
    for i,j in finalX.iteritems():
        print i + ": "
        print("Y: %.2f" % j.y)
        print("N: %.2f" % j.x)
    print "Orientations :\n"
    for i,ob in orientations.iteritems():
        
        print str.format("{0}   {1}", i, round(ob,1))

    V=A*N-L
    for i in range(size(V)):
        print str(obsList[i]) +": " +  str(V[i]) 
    return finalX , obs,control
#     i=0
#     
#     print A.T*V
    
