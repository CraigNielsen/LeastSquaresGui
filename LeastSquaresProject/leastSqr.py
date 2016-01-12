import math

from numpy import floor, pi, float64, size, sqrt
import numpy

from Equations import Directions, Distances, equations
from LeastSquaresProject.observations import ObsSplit
from LeastSquaresProject.point import Point
from LeastSquaresProject.precisions import obsCount
from LeastSquaresProject.surveyData import SurveyData
from LeastSquaresProject.weights import Weights
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from points import Points


numpy.set_printoptions(threshold=numpy.nan)

class LeastSqr(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def Read(self,inputControl,inputObservations):
        control = Points("control points")
        control.read(inputControl)
#         print control
        
        provis = Points("provisional points")
#         print provis
        np.set_printoptions(precision=12)
        np.set_printoptions(suppress=True)
        np.set_printoptions(linewidth=2000)
        numpy.set_printoptions(threshold=1000)
        print "Reading Obs"
        obs = SurveyData()
        count,N,pos=obs.read(inputObservations,control)#reads in file into the surveyData dictionary which contains Target object with two variables
        print obs
        edge_weight={}
#         for u,v,d in N.edges(data=True):
#             print u
#             print v
#             edge_weight[u][v]=d['direction']
           
        
#         dict([((u,v,),int(d['distance'])) for u,v,d in N.edges(data=True)])
        nx.draw_networkx_nodes(N,pos,
                       node_color='y',
                       node_size=800,
                       alpha=0.8)
        nx.draw_networkx_nodes(N,pos,
                       nodelist=control,
                       node_color='r',
                       node_size=800,
                       alpha=0.8)
        edges={}
        for v,u,d in N.edges(data=True):
#             print d
            if d.has_key("distance") and d.has_key('direction'):
                edges[v,u]='b'
            
            
        nx.draw(N,pos)
        nx.draw_networkx_edges(N,pos,
                       edgelist=edges,
                       width=8,alpha=0.5,edge_color='b')
        plt.show()
        OBS=ObsSplit("Individual Observations 2014 Survey")
        OBS=OBS.read(obs,control)
#         print OBS
#         N.add_nodes_from(obs.keys())
#         for n, p in control.iteritems():
#             N.node[n]['pos'] = p
#         
#         nx.draw(N,'pos')
#         plt.show()
        
        
        
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
    #     knowns = []
        
        for station_name, station in obs.iteritems():
            unknowns2.add(station_name+'_o')
            for target_name, target in station.iteritems():
                if not control.has_key(target_name):
                    unknowns2.add(target_name+'_x')
                    unknowns2.add(target_name+'_y')
                pass
        unknowns=[]
#         print obsList
        for i in unknowns2:
            unknowns.append(i)
        
        # Means all distances between points
#         print "===             Calculate Mean Distance ObsSplit           =================="
    
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
        for sta,station in obs.iteritems():
            if control.has_key(sta):
                continue
            else:
                provis.add(sta, station.point.x, station.point.y, station.point.h, False)
#         print provis
        
        #give stations coordinates if they're control points
        
#         for name,obj in control.iteritems():
#             if obs.has_key(name):
#                 obs[name].setPoint(obj)
#         
#         
#         for sn1,station1 in obs.iteritems():
#                 
#                 for tn1,target1 in station1.iteritems():
#                     if not control.has_key(tn1) and not station1[tn1].distance==None and not station1[tn1].direction==None and not station1.point==None:
#                         d= station1[tn1].distance
#                         t= station1[tn1].direction
#                         x,y,h=station1.point.polar(d,t)
#                         provis.add(tn1,x,y,h,False)
#                         obs[tn1].setPoint(provis[tn1])
        
        print "================================================================================="
        print "======           Truncate Distances              ==========================================================================="
        temp=Points()
        for i,obj in provis.iteritems():
            temp.add(i,obj.x,obj.y,obj.h,False)
        for p,obj in temp.iteritems():
            provis.replace(p,floor(obj.x),floor(obj.y),floor(obj.h),False)
#             print provis[p]
         
       
      
        
        print "======================   TESTING   ====================================================="
    #     
        provis.add('SUR10',58961.,49666.4,0.,False)
        provis.add('RU4A',59120.6,49687.0,0.,False)
        provis.add('SUR11',59295.0,49732.0,0.,False)
        
        print "================================================================================="
        
        print "======    Calculate Misclosure L      ==========================================="
        
      
        
        
        L=numpy.zeros(shape=(count,1))
        Lnames=Points("L vector name pairs")
        i=0
        for sn1,station in OBS.iteritems():
            
            for tn1,target in station.iteritems():
                tn1=tn1[0:-2]
#                 tn1=tn1[0:-2]
                if target.type=="direction":
                    if control.has_key(tn1):
                        calc=obs[sn1].point.join(control[tn1])
                        temp=obs[sn1].point
                    elif provis.has_key(tn1):
                        calc=obs[sn1].point.join(provis[tn1])
                    else: 
                        print "error"
                        calc=0
                    observed=obs[sn1][tn1].direction
                    target.setMisclosure(observed-calc)
                    L[i][0]=((observed-calc)*3600.*180./pi)
                    
                    Lnames[sn1 + " to "+ tn1 + " direc"]=round(((observed-calc)*3600.*180./pi),1)
                    i+=1
#                   
                    continue
                elif target.type == "distance":
                    if control.has_key(tn1):
                        calc=obs[sn1].point.joinS(control[tn1])
                    elif provis.has_key(tn1):
                        calc=obs[sn1].point.joinS(provis[tn1])
                    else: print "error"
                    
                    observed=obs[sn1][tn1].distance
                    target.setMisclosure(observed-calc)
                    L[i][0]=round((observed-calc),3)
                    Lnames[sn1 + " to "+ tn1 + " distance"]=L[i][0]
                    i+=1
#                 print str(sn1) + " " + str(tn1)           
    #             print observed
#                 print ('%0.1f' % float64(target.misclosure*180./math.pi*3600.))    
#         print Lnames
#         print L
        print "==============        A Matrix        ========================================="
        
        A = numpy.zeros(shape=(count,len(unknowns)))
        A[0][0]=3
        i=0
        j=0
        for station_name,station in OBS.iteritems():
            
            if control.has_key(station_name):
                    current_station=control[station_name]
            elif provis.has_key(station_name):
                    current_station=provis[station_name]
                    
            for tname,target in station.iteritems():
                tname=tname[0:-2]
                j=0
#                 tname=tname[0:-2]
                if target.type=='direction' or target.type=='distance' :
                    for diff_wrt in unknowns:
                        
                        if diff_wrt[-1]=='o'and target.type=='distance':
                            A[i][j]=0
                            continue
                        if diff_wrt[-1]=='o'and target.type=='direction':
                            if station_name==diff_wrt[0:-2]:
                                A[i][j]=-1.
                                j+=1
                                continue
                            else: 
                                A[i][j]=0
                                j+=1
                                continue
                        if not tname==diff_wrt[0:-2] and not station_name==diff_wrt[0:-2]: 
                            A[i][j]=0
                            j+=1
                            continue
                        
                        if control.has_key(tname):#if observing control
                                if target.type=="direction":
                                    A[i][j]=equations(current_station,control[tname],diff_wrt,'direction')
                                else :   
                                    A[i][j]=equations(current_station,control[tname],diff_wrt,'distance')
                                j+=1
                                continue
                            
                        else:#if observing provisional
                                if target.type=="direction":
                                    A[i][j]=equations(current_station,provis[tname],diff_wrt,'direction')
                                else:
                                    A[i][j]=equations(current_station,provis[tname],diff_wrt,'distance')
                                j+=1
                                continue
                else:
                    for diff_wrt in unknowns:
                        
                        if diff_wrt[-1]=='o':
                            if station_name==diff_wrt[0:-2]:
                                A[i][j]=-1.
                                j+=1
                                continue
                            else: 
                                A[i][j]=0
                                j+=1
                                continue
                        if not tname==diff_wrt[0:-2] and not station_name==diff_wrt[0:-2]:
                            A[i][j]=0
                            j+=1
                            continue
                        
                        if control.has_key(tname):#if observing control
                            
                                A[i][j]=equations(current_station,control[tname],diff_wrt,target.type)
                                j+=1
                            
                            
                        else:#if observing provisional
                                A[i][j]=equations(current_station,provis[tname],diff_wrt,target.type)
                                j+=1
                    
                    
                i+=1
#                     print "i: " +str(i) 
        #print ""
        print "SUR10_o',    'RU4A_y',      'RU4A_x',  'SUR11_x',     'SUR11_y',         'SUR12_o',         'SUR10_y',     'SUR10_x',      'RU4A_o',     'SUR11_o',         'SUR09_o'"
#         print A
#         print OBS
        names=[]
        for name,ob in obs.iteritems():
            for na,tar in ob.iteritems():
                if tar.type=="both":
                    names.append(name + "-" + na + "D")
                    names.append(name + "-" + na + "d")
                else:
                    names.append(name + "-" + na + "D")
    
                    
        row_labels = ['SUR09-T013', 'Y', 'N', 'W']
#         for row_label, row in zip(names, A):
            #print '%s [%s]' % (row_label, '      '.join('%01f' % i for i in row))          
    #   except:                   
    #                     print "trying"
    #                     A[i][j]=equations(station.point,provis[t],diff_wrt[-1],types[i])
    #           
    #            
    #         i+=1
    #                     
        #print A       
        print "==============        Calculate Least squares       ========================================="
        
        Pob= Weights()
        Pob.setDirectionWeight(1)
        Pob.setDistanceWeight(1)
        P=Pob.matrix(obs,A)
        A=numpy.asmatrix(A)
        N= (((A.T)*P*A)**(-1))*(A.T*P*L)
        Xtemp=Points("N correction pairs")
        i=0
        
        for name in unknowns:
            Xtemp[name]=float64(N[i])
            i+=1
        finalX=Points("final Coordinates:")
        orientations={}
        j=0
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
#         print finalX
        V=A*N-L
#         print V
#         print A.T*V
        posteriori=float((V.T*P*V)/(count-size(unknowns)))
#         print posteriori
        covarience_mat= posteriori*(A.T*A)**(-1)
        precisions=Points("Precisions of Unknowns")
        i=0
#         print "awek"
#         print N
#         print covarience_mat[1,1]
        for name,value in Xtemp.iteritems():
#             print value
#             print N[i]
            precisions[name]=sqrt(float(covarience_mat[i,i]))
            i+=1
            
#         print precisions
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        return A, Xtemp,provis,OBS,control,unknowns,V,P
    #     i=0
    #     
    #     print A.T*V  
    
    
    
    
    def getL(self,provis,obs,control):
#         print "================================================================================="
#         print "======    Calculate Misclosure L      ==========================================="
        
      
        
        count=obsCount(obs)
        L=numpy.zeros(shape=(count,1))
        Lnames=Points("L vector name pairs")
        i=0
        for sn1,station in obs.iteritems():
            for tn1,target in station.iteritems():
                tn2=tn1
                tn1=tn1[0:-2]
                if target.type=="direction":
                    if control.has_key(tn1):
                        if provis.has_key(sn1):
                            calc=provis[sn1].join(control[tn1])
                        elif control.has_key(sn1):
                            calc=control[sn1].join(control[tn1])
                    elif provis.has_key(tn1):
                        if provis.has_key(sn1):
                            calc=provis[sn1].join(provis[tn1])
                        elif control.has_key(sn1):
                            calc=control[sn1].join(provis[tn1])
                    else: 
                        print "error"
                        calc=0
                    observed=obs[sn1][tn2].direction
                    target.setMisclosure(observed-calc)
                    L[i][0]=(observed-calc)
                    
                    Lnames[sn1 + " to "+ tn1 + " direc"]=L[i][0]
                    i+=1
#                   
                    continue
                elif target.type == "distance":
                    if control.has_key(tn1):
                        if provis.has_key(sn1):
                            calc=provis[sn1].joinS(control[tn1])
                        elif control.has_key(sn1):
                            calc=control[sn1].joinS(control[tn1])
                    elif provis.has_key(tn1):
                        if provis.has_key(sn1):
                            calc=provis[sn1].joinS(provis[tn1])
                        elif control.has_key(sn1):
                            calc=control[sn1].joinS(provis[tn1])
                    else: print "error"
                    
                    observed=obs[sn1][tn2].distance
                    target.setMisclosure(observed-calc)
                    L[i][0]=round((observed-calc),3)
                    Lnames[sn1 + " to "+ tn1 + " distance"]=L[i][0]
                    i+=1   
        return L
    def Provisional(self,N,provis,unknowns):    
        j=0    
        finalX=Points('New Provisional Points')
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
        return finalX
#     def adjustProvisional(self,obs,N):
    def adjustProvisional(self,N,provis,obs,unknowns): 
        i=0
        j=0
        for ideas in unknowns:
            name=ideas[0:-2]
            type= ideas[-1]
            if type=="x":
                provis[name].x=provis[name].x + N[ideas]
            elif type=="y":
                provis[name].y=provis[name].y + N[ideas]
            if type=='o':
                pass
#                 for sname,station in obs.iteritems():
#                     if sname==name:
#                         for tname,target in station.iteritems():
#                             
#                             if target.type=="direction":
#                                 temp=float64(target.direction)+float64(N[ideas]*pi/180.)
#                                 target.setDirection(temp)
                    
            j+=1
        return provis          

         
    def getA(self,provis,OBS,control,unknowns):
        count=self.obsCount(OBS)
        L=self.getL(provis, OBS, control)
#         print "==============        A Matrix        ========================================="
        
        A = numpy.zeros(shape=(count,len(unknowns)))
        A[0][0]=3
        i=0
        j=0
        for station_name,station in OBS.iteritems():
            
            if control.has_key(station_name):
                    current_station=control[station_name]
            elif provis.has_key(station_name):
                    current_station=provis[station_name]
                    
            for tname,target in station.iteritems():

                j=0
#                 tname=tname[0:-2]
                if target.type=='direction' or target.type=='distance' :
                    for diff_wrt in unknowns:
                        
                        
                        if diff_wrt[-1]=='o':
                            if station_name==diff_wrt[0:-2]:
                                A[i][j]=-1.
                                j+=1
                                continue
                            else: 
                                A[i][j]=0
                                j+=1
                                continue
                        if not tname==diff_wrt[0:-2] and not station_name==diff_wrt[0:-2]: 
                            A[i][j]=0
                            j+=1
                            continue
                        
                        if control.has_key(tname):#if observing control
                                if target.type=="direction":
                                    A[i][j]=equations(current_station,control[tname],diff_wrt,'direction')
                                else :   
                                    A[i][j]=equations(current_station,control[tname],diff_wrt,'distance')
                                j+=1
                                continue
                            
                        else:#if observing provisional
                                if target.type=="direction":
                                    A[i][j]=equations(current_station,provis[tname],diff_wrt,'direction')
                                else:
                                    A[i][j]=equations(current_station,provis[tname],diff_wrt,'distance')
                                j+=1
                                continue
                else:
                    for diff_wrt in unknowns:
                        
                        if diff_wrt[-1]=='o':
                            if station_name==diff_wrt[0:-2]:
                                A[i][j]=-1.
                                j+=1
                                continue
                            else: 
                                A[i][j]=0
                                j+=1
                                continue
                        if not tname==diff_wrt[0:-2] and not station_name==diff_wrt[0:-2]:
                            A[i][j]=0
                            j+=1
                            continue
                        
                        if control.has_key(tname):#if observing control
                            
                                A[i][j]=equations(current_station,control[tname],diff_wrt,target.type)
                                j+=1
                            
                            
                        else:#if observing provisional
                                A[i][j]=equations(current_station,provis[tname],diff_wrt,target.type)
                                j+=1
                    
                    
                i+=1
                return A
            
    def Iterate(self,provis,OBS,control,unknowns):
        count=obsCount(OBS)
        L=self.getL(provis, OBS, control)
#         print "==============        A Matrix        ========================================="
        
        A = numpy.zeros(shape=(count,len(unknowns)))
        A[0][0]=3
        i=0
        j=0
        for station_name,station in OBS.iteritems():
            
            if control.has_key(station_name):
                    current_station=control[station_name]
            elif provis.has_key(station_name):
                    current_station=provis[station_name]
                    
            for tname,target in station.iteritems():
                tname=tname[0:-2]
                j=0
#                 tname=tname[0:-2]
                if target.type=='direction' or target.type=='distance' :
                    for diff_wrt in unknowns:
                        
                        
                        if diff_wrt[-1]=='o':
                            if station_name==diff_wrt[0:-2]:
                                A[i][j]=-1.
                                j+=1
                                continue
                            else: 
                                A[i][j]=0
                                j+=1
                                continue
                        if not tname==diff_wrt[0:-2] and not station_name==diff_wrt[0:-2]: 
                            A[i][j]=0
                            j+=1
                            continue
                        
                        if control.has_key(tname):#if observing control
                                if target.type=="direction":
                                    A[i][j]=equations(current_station,control[tname],diff_wrt,'direction')
                                else :   
                                    A[i][j]=equations(current_station,control[tname],diff_wrt,'distance')
                                j+=1
                                continue
                            
                        else:#if observing provisional
                                if target.type=="direction":
                                    A[i][j]=equations(current_station,provis[tname],diff_wrt,'direction')
                                else:
                                    A[i][j]=equations(current_station,provis[tname],diff_wrt,'distance')
                                j+=1
                                continue
                else:
                    for diff_wrt in unknowns:
                        
                        if diff_wrt[-1]=='o':
                            if station_name==diff_wrt[0:-2]:
                                A[i][j]=-1.
                                j+=1
                                continue
                            else: 
                                A[i][j]=0
                                j+=1
                                continue
                        if not tname==diff_wrt[0:-2] and not station_name==diff_wrt[0:-2]:
                            A[i][j]=0
                            j+=1
                            continue
                        
                        if control.has_key(tname):#if observing control
                            
                                A[i][j]=equations(current_station,control[tname],diff_wrt,target.type)
                                j+=1
                            
                            
                        else:#if observing provisional
                                A[i][j]=equations(current_station,provis[tname],diff_wrt,target.type)
                                j+=1
                    
                    
                i+=1
        names=[]
        for name,ob in OBS.iteritems():
            for na,tar in ob.iteritems():
                if tar.type=="both":
                    names.append(name + "-" + na + "D")
                    names.append(name + "-" + na + "d")
                else:
                    names.append(name + "-" + na + "D")
    
                    
        row_labels = ['SUR09-T013', 'Y', 'N', 'W']
#         for row_label, row in zip(names, A):
#             print '%s [%s]' % (row_label, '      '.join('%01f' % i for i in row))          
   
#         print "==============        Calculating Least squares       ========================================="
        
        
        Pob= Weights()
        Pob.setDirectionWeight(1)
        Pob.setDistanceWeight(1)
        P=Pob.matrix(OBS,A)
        A=numpy.asmatrix(A)
        N= (((A.T)*A)**(-1))*A.T*L
        provUpdate=self.Provisional(N, provis, unknowns)
        Xtemp=Points("N correction pairs")
        i=0
        
        for name in unknowns:
            Xtemp[name]=float64(N[i])
            i+=1
                
        V=A*N-L
#         print A.T*V
        posteriori=float((V.T*P*V)/(count-size(unknowns)))
#         print posteriori
        covarience_mat= posteriori*(A.T*A)**(-1)
        precisions=Points("Precisions of Unknowns")
        i=0
        for name,value in Xtemp.iteritems():
            precisions[name]=sqrt(float(covarience_mat[i,i]))
            i+=1
            
#         print precisions    
#         
#         for i,j in finalX.iteritems():
#             print i + ": "
#             print("Y: %.2f" % j.y)
#             print("N: %.2f" % j.x)
#         print "Orientations :\n"
#         for i,ob in orientations.iteritems():
#             
#             print str.format("{0}   {1}", i, round(ob,1))
#     

        return A,Xtemp , provUpdate , OBS , control , unknowns, V,P
    
# if __name__ == '__main__':
#     Leas= LeastSqr()
#     A,Xdict,provis,OBS,control,unknowns,V,P=Leas.Read('control.csv','observations.csv')  