from math import pi, atan2
import math

from numpy import size, sqrt, shape
import numpy

from Equations import equations
from LeastSquaresProject.point import Point
from LeastSquaresProject.points import *
from LeastSquaresProject.station import Station
from LeastSquaresProject.surveyData import SurveyData
from LeastSquaresProject.target import Target
from LeastSquaresProject.weights import Weights
import matplotlib.pyplot as plt
import networkx as nx
import sympy as sp


def Observations(filename):
    c0=0#Code
    c1=1#Setup    #COLUMNS FOR FILE INPUT: first column in excell is c0
    c2=2#Target
    c3=3#direction
    c4=4#distance
    c5=5#known
#     if SitholeExcelFormat:
#         c0=0#Code
#         c1=1#Setup    
#         c2=1#Target
#         c3=2#direction
#         c4=2#distance
#         c5=5#known
    
    
    
    count=0
    N=nx.MultiDiGraph()
    
    f = open(filename, 'r')    
    f.readline()
    node=""
    stationsOrder=[]
    obsOrder=[]
    for line in f:
        sp = line.split(',')
        if(int(sp[0]) == 0) :
            N.add_node(sp[1] )
            node=sp[1]
            stationsOrder.append(sp[1])
            obsOrder.append("sta "+sp[1])
        elif(int(sp[0]) == 1) :
            num= float(sp[3])*pi/180.
            N.add_edge(node,sp[2],key=node,direction= num)
            obsOrder.append("tarD"+sp[2])
        elif(int(sp[0]) == 2) :
            N.add_edge(node,sp[2] ,key=node,distance=float(sp[4]))
            obsOrder.append("tard"+sp[2])
        elif(int(sp[0]) == 3) :
            num= float(sp[3])*pi/180.
            N.add_edge(node,sp[2],key=node,direction= num)
            obsOrder.append("tarD"+sp[2])
            N.add_edge(node,sp[2] ,key=node,distance=float(sp[4]))
            obsOrder.append("tard"+sp[2])
            
    return N,stationsOrder,obsOrder      
def controlPoints(N,filename):    
      
    control = Points("control points")
    control2 = Points("control points")
    control.read(filename)
    temp=set()
    for n in N.edges_iter(data=True):
        temp.add(n[0])
        temp.add(n[1])

    for i in temp:
        if control.has_key(i):
            control2.add(i, control[i].x, control[i].y, control[i].h, True)
    return control2
def dfs_edges(G,source):
    visited=set()
    search=list()
 
    def node_visitor(parent): # recursive function
        visited.add(parent)  #adds argument to visited set
        children = G.neighbors(parent) # finds neighbors of current node
        for child in children: #iterates through neighbors             
            if not child in visited: # checks if the neighboring node has been visited
                search.append((parent,child)) #add the search leg : parent child relationship
                node_visitor(child)# recurse function with the new child
         
    for node in [source]: # loop through source nodes? #checks if already visited that node
        
        if node in visited:#if visited skip over
            continue
 
        node_visitor(node)#otherwise run function
 
    return search
def getPoints(N,control):
    
    N=N
    unknowns=set()
    
    for x in N:
        if not control.has_key(x):
            unknowns.add(x)
def getUnknowns(N,control):
    
    unknowns=set()
    unknowns2=set()
    unk=[]
    for x in N.edges_iter(data=True):
        if not control.has_key(x[0]):
            unknowns2.add(x[0]+"_x")
            unknowns2.add(x[0]+"_y")
            unknowns2.add(x[0]+"_o")
        else:
            unknowns2.add(x[0]+"_o")
        if not control.has_key(x[1]):
            unknowns2.add(x[1]+"_x")
            unknowns2.add(x[1]+"_y")
    for i in unknowns2:
        unk.append(i)

                 

    return unk
def provTrilateration(N,control,unknowns,provis):
    pass
def getProvisionals(N,control,unknowns2):
    unknowns={}
    for u in unknowns2:
        if not u[-1]=="o" and not unknowns.has_key(u[0:-2]):
            unknowns[u[0:-2]]=u[0:-2]
    provis,unknowns=provTraverse(N,control,unknowns)
    i=0
    if len(unknowns)>0:
        provis,unknowns=provResection(N,control,unknowns,provis)  
#     if len(unknowns)>0:
#         provis,unknowns=provTrilateration(N,control,unknowns,provis)  
    if len(unknowns)>0:
        provis,unknowns=provIntersection(N,control,unknowns,provis)
    provis2,unknowns=provTraverse(N,control,unknowns)
    while len(unknowns)>0:
        provis2,unknowns=provTraverse(N,control,unknowns)
        provis2,unknowns=provIntersection(N,control,unknowns,provis2)
        provis2,unknowns=provResection(N,control,unknowns,provis2) 
        i+=1
        if i>200:
            print "error not finding provisionals"
            break
    for i,j in provis.iteritems():
            j.ChangeVariable("x",round(j.x,3))
            j.ChangeVariable("y",round(j.y,3))
    if provis2:
        for i,j in provis2.iteritems():
                j.ChangeVariable("x",round(j.x,3))
                j.ChangeVariable("y",round(j.y,3))
    for i,j in provis2.iteritems():
        provis.add(i, j.x, j.y, j.h, False)
    return provis 
def bowditchAdjust(provis,control,k):
    print "this is not complete yet!!"
    diffX=control[k[0]].x-provis[k].x
    diffY=control[k[0]].y-provis[k].y
    count=len(provis.keys())

    return diffX,diffY
    
    
    
def provResection(N,control,unknowns,provis):

    for u,j in unknowns.iteritems():
        temp=[]
        for n in N.edges_iter(data=True):
            target=n[1]
            station=n[0]
            if n[0]==u and control.has_key(n[1])and N[station][target][station].has_key("direction"):
                temp.append(target)
                temp.append(control[n[1]])
                temp.append(N[station][target][station]['direction'])
                if len(temp)>=9:
                    
                    def resec(y0,x0,a0,y1,x1,a1,y2,x2,a2,u):
                        Y = [];
                        N= [];
                        A = [];
                        Y.append(y0)
                        Y.append(y1)
                        Y.append(y2)
                        N.append(x0)
                        N.append(x1)
                        N.append(x2)
                        A.append(a0)
                        A.append(a1)
                        A.append(a2)
                        
                #            
                #            % calculation of provisional coordinates using observations...........
                #            %=====================================================================
                
                        alpha=A[1]-A[0];
                        
                        if (alpha<0): 
                            alpha=alpha+360*math.pi/180;
                        beta=A[2]-A[1];
                        if (beta<0): 
                            beta=beta+360*math.pi/180;
                        charlie=A[0]-A[2];
                        if (charlie<0): 
                            charlie=charlie+360*math.pi/180;
                
                        
                        Talpha=math.tan(alpha);
                        Tbeta=math.tan(beta);
                        if 0<=Talpha<0.05 or -0.05<Talpha<=0 or 0<=Tbeta<0.05 or -0.05<Tbeta<=0 :
                            print '====   Unsafe Geometry   ===' 
                         
                         
                #            %coord differences BAX: B minus A in N & BAY: B minus A in Y
                        BAX=N[1]-N[0];
                        BAY=Y[1]-Y[0];
                        BCX=N[1]-N[2];
                        BCY=Y[1]-Y[2];
                        ACX=N[1]-N[2];
                        ACY=Y[1]-Y[2];
                #            
                #         %=======BLUNTS METHOD FORMULA==========================================
                        def cot(x):
                            return 1/(math.tan(x))
                        
                        deltaY= -(N[2]-N[0])+(Y[2]-Y[1])*cot(beta)+(Y[0]-Y[1])*cot(alpha);
                        deltaX= (Y[2]-Y[0])+(N[2]-N[1])*cot(beta)+(N[0]-N[1])*cot(alpha);
                        tNB=math.atan(deltaY/deltaX);
                        
                #         %check quadrant==========
                        if (deltaY>0) and (deltaX<0):
                            tNB=tNB+math.pi;
                        elif ((deltaY<0) and (deltaX<0)):
                            tNB=tNB+math.pi;
                        elif (deltaY<0) and (deltaX>0):
                            tNB=tNB+2*math.pi;
                #     %=========================
                        
                        
                        
                        Dcorrection=tNB-A[1];
                #         %    display(degrees2dms(radtodeg(Dcorrection)));
                        Ac=[[],[],[]]; 
                        Ac[0]=A[0]+ Dcorrection;
                        Ac[1]=A[1]+ Dcorrection;
                        Ac[2]=A[2]+ Dcorrection;
                        t1N=Ac[0]+math.pi;
                        t2N=Ac[1]+math.pi;
                        t3N=Ac[2]+math.pi;
                #            
                        
                #            %========calculate intersection for provisional point=========
                #         t= Intersection;
                #         NX1,NY1 = t.intersect (Y[0],N[0],A[0],Y[1],N[1],A[1]);
                #            NX1= N(1)+((Y(2)-Y(1))-(N(2)-N(1))*tan(t2N))/(tan(t1N)-tan(t2N));
                #            NY1= Y(1) + (NX1-N(1))*tan(t1N);
                        NX1= N[0]+((Y[1]-Y[0])-(N[1]-N[0])*math.tan(t2N))/(math.tan(t1N)-math.tan(t2N));
                        NY1= Y[0] + (NX1-N[0])*math.tan(t1N);
                        NH1=0
                        p=Point(NX1,NY1,NH1,False,u)
                        return p
                        
                    stat1=temp[0]
                    stat2=temp[3]
                    stat3=temp[6]
                    x0=temp[1].x
                    y0=temp[1].y
                    h0=temp[1].h
                    a0=N[station][stat1][station]['direction']
                    x1=temp[4].x
                    y1=temp[4].y
                    h1=temp[4].h
                    a1=N[station][stat2][station]['direction']
                    x2=temp[7].x
                    y2=temp[7].y
                    h2=temp[7].h
                    a2=N[station][stat3][station]['direction']
                    prov=resec(y0,x0,a0,y1,x1,a1,y2,x2,a2,u)
                    del temp[0:3]
                    provis.add(prov.name,prov.x,prov.y,prov.h,prov.known)
                
            elif  n[0]==u and provis.has_key(n[1]) and N[station][target][station].has_key("direction"):
                temp.append(target)
                temp.append(provis[n[1]])
                temp.append(N[station][target][station]['direction'])
                if len(temp)>=9:
                    def resec(y0,x0,a0,y1,x1,a1,y2,x2,a2,u):
                        Y = [];
                        N= [];
                        A = [];
                        Y.append(y0)
                        Y.append(y1)
                        Y.append(y2)
                        N.append(x0)
                        N.append(x1)
                        N.append(x2)
                        A.append(a0)
                        A.append(a1)
                        A.append(a2)
                        
                #            
                #            % calculation of provisional coordinates using observations...........
                #            %=====================================================================
                
                        alpha=A[1]-A[0];
                        
                        if (alpha<0): 
                            alpha=alpha+360*math.pi/180;
                        beta=A[2]-A[1];
                        if (beta<0): 
                            beta=beta+360*math.pi/180;
                        charlie=A[0]-A[2];
                        if (charlie<0): 
                            charlie=charlie+360*math.pi/180;
                
                        
                        Talpha=math.tan(alpha);
                        Tbeta=math.tan(beta);
                        if 0<=Talpha<0.05 or -0.05<Talpha<=0 or 0<=Tbeta<0.05 or -0.05<Tbeta<=0 :
                            print '====   Unsafe Geometry   ===' 
                         
                #            %coord differences BAX: B minus A in N & BAY: B minus A in Y
                        BAX=N[1]-N[0];
                        BAY=Y[1]-Y[0];
                        BCX=N[1]-N[2];
                        BCY=Y[1]-Y[2];
                        ACX=N[1]-N[2];
                        ACY=Y[1]-Y[2];
                #            
                #         %=======BLUNTS METHOD FORMULA==========================================
                        def cot(x):
                            return 1/(math.tan(x))
                        
                        deltaY= -(N[2]-N[0])+(Y[2]-Y[1])*cot(beta)+(Y[0]-Y[1])*cot(alpha);
                        deltaX= (Y[2]-Y[0])+(N[2]-N[1])*cot(beta)+(N[0]-N[1])*cot(alpha);
                        tNB=math.atan(deltaY/deltaX);
                        
                #         %check quadrant==========
                        if (deltaY>0) and (deltaX<0):
                            tNB=tNB+math.pi;
                        elif ((deltaY<0) and (deltaX<0)):
                            tNB=tNB+math.pi;
                        elif (deltaY<0) and (deltaX>0):
                            tNB=tNB+2*math.pi;
                #     %=========================
                        
                        
                        
                        Dcorrection=tNB-A[1];
                #         %    display(degrees2dms(radtodeg(Dcorrection)));
                        Ac=[[],[],[]]; 
                        Ac[0]=A[0]+ Dcorrection;
                        Ac[1]=A[1]+ Dcorrection;
                        Ac[2]=A[2]+ Dcorrection;
                        t1N=Ac[0]+math.pi;
                        t2N=Ac[1]+math.pi;
                        t3N=Ac[2]+math.pi;
                #            
                        
                #            %========calculate intersection for provisional point=========
                #         t= Intersection;
                #         NX1,NY1 = t.intersect (Y[0],N[0],A[0],Y[1],N[1],A[1]);
                #            NX1= N(1)+((Y(2)-Y(1))-(N(2)-N(1))*tan(t2N))/(tan(t1N)-tan(t2N));
                #            NY1= Y(1) + (NX1-N(1))*tan(t1N);
                        NX1= N[0]+((Y[1]-Y[0])-(N[1]-N[0])*math.tan(t2N))/(math.tan(t1N)-math.tan(t2N));
                        NY1= Y[0] + (NX1-N[0])*math.tan(t1N);
                        NH1=0
                        p=Point(NX1,NY1,NH1,False,u)
                        return p
                        
                    stat1=temp[0]
                    stat2=temp[3]
                    stat3=temp[6]
                    x0=temp[1].x
                    y0=temp[1].y
                    h0=temp[1].h
                    a0=N[station][stat1][station]['direction']
                    x1=temp[4].x
                    y1=temp[4].y
                    h1=temp[4].h
                    a1=N[station][stat2][station]['direction']
                    x2=temp[7].x
                    y2=temp[7].y
                    h2=temp[7].h
                    a2=N[station][stat3][station]['direction']
                    prov=resec(y0,x0,a0,y1,x1,a1,y2,x2,a2,u)
                    del temp[0:3]
                    provis.add(prov.name,prov.x,prov.y,prov.h,prov.known)
                   
    for i,j in provis.iteritems():
        if unknowns.has_key(i):
            unknowns.pop(i)
    return(provis,unknowns)
def provIntersection(N,control,unknowns,provis):   
    
    for u,j in unknowns.iteritems():
        temp=[]
        for n in N.edges_iter(data=True):
            station=n[0]
            if n[1]==u and control.has_key(n[0]):
                temp.append(station)
                temp.append(control[n[0]])
                temp.append(N[station][u][station]['direction'])
                if len(temp)>=6:
                    def inter(y0,x0,a0,y1,x1,a1,u):
     
                        NX= x0+((y1-y0)-(x1-x0)*math.tan(a1))/(math.tan(a0)-math.tan(a1));
                        NY= y0 + (NX-x0)*math.tan(a0);
                        NH=0 
                        p=Point(NX,NY,NH,False,u)
                        return p
                    stat1=temp[0]
                    stat2=temp[3]
                    x0=temp[1].x
                    y0=temp[1].y
                    h0=temp[1].h
                    a0=N[stat1][u][stat1]['direction']
                    x1=temp[4].x
                    y1=temp[4].y
                    h1=temp[4].h
                    a1=N[stat2][u][stat2]['direction']
                    prov=inter(y0,x0,a0,y1,x1,a1,u)
                    del temp[0:3]
                    provis.add(prov.name,prov.x,prov.y,prov.h,prov.known)
                
            elif  n[1]==u and provis.has_key(n[0]):
                temp.append(station)
                temp.append(provis[n[0]])
                temp.append(N[station][u][station]['direction'])
                if len(temp)>=6:
                    def inter(y0,x0,a0,y1,x1,a1,u):
     
                        NX= x0+((y1-y0)-(x1-x0)*math.tan(a1))/(math.tan(a0)-math.tan(a1));
                        NY= y0 + (NX-x0)*math.tan(a0);
                        NH=0 
                        p=Point(NX,NY,NH,False,u)
                        return p
                    stat1=temp[0]
                    stat2=temp[3]
                    x0=temp[1].x
                    y0=temp[1].y
                    h0=temp[1].h
                    a0=N[stat1][u][stat1]['direction']
                    x1=temp[4].x
                    y1=temp[4].y
                    h1=temp[4].h
                    a1=N[stat2][u][stat2]['direction']
                    prov=inter(y0,x0,a0,y1,x1,a1,u)
                    del temp[0:3]
                    provis.add(prov.name,prov.x,prov.y,prov.h,prov.known)
            
    for i,j in provis.iteritems():
        if unknowns.has_key(i):
            unknowns.pop(i)
    return(provis,unknowns)
def provTraverse(N,control,unknowns):
    orderList=list()
    provis=Points("Provisional Coordinates")
    for x,y in control.iteritems():
        if len(unknowns)>1:
            orderList.append( order(N,x,unknowns,control))
        else:
            break
    for i in orderList:
        for j in i:
            station=j[0]
            target=j[1]
            if N[station][target][station].has_key("distance") and N[station][target][station].has_key("direction"):
#                 N.add_node(target,key=target,coordinate=polar(station['coordinate'],))
                if control.has_key(station) and not control.has_key(target):
                    newp= control[station].polar(N[station][target][station]['distance'],N[station][target][station]['direction'])
                    provis.add(target, newp.x, newp.y, newp.h, False)
                    
                elif provis.has_key(station) and not control.has_key(target):
                    newp= provis[station].polar(N[station][target][station]['distance'],N[station][target][station]['direction'])
                    provis.add(target, newp.x, newp.y, newp.h, False)
                    
                elif not control.has_key(target):
                    print "provisional provTraverse error... no such point in control or provisional"
    for i,j in provis.iteritems():
        if unknowns.has_key(i):
            unknowns.pop(i)
    return(provis,unknowns)
def order(N,source,unknowns,control):
    
    visited=set()
    search=list()

    def node_visitor(parent): # recursive function
      
        
        visited.add(parent)  #adds argument to visited set
        children = N.neighbors(parent) # finds neighbors of current node
        for child in children: #iterates through neighbors             
            if not child in visited: # checks if the neighboring node has been visited
                search.append((parent,child)) #add the search leg : parent child relationship
                node_visitor(child)# recurse function with the new child
        
    for node in [source]: # loop through source nodes? #checks if already visited that node
        if node in visited:#if visited skip over
            continue
        node_visitor(node)#otherwise run function

    return search
def obsCount(obs):
        count=0
        for i,j in obs.iteritems():
            for k,t in j.iteritems():
                count+=1
                if t.type=="both":
                    count+=1
        return count
def getObs(N):
    obs=SurveyData("Observations")
    obsList=[]
    for station in N.edges_iter(data=True):
        
        if station[2].has_key('distance'):
            stat=station[0]
            targ=station[1]
            if not obs.hasStation(stat): obs[stat]=Station()
            if not obs[stat].hasTarget(targ): obs[stat][targ]=Target()
#                    
            obs[stat][targ].setDistance(station[2]['distance'])
            if obs[stat][targ].type == "direction":
                obs[stat][targ].setType('both')
            else:
                obs[stat][targ].setType('distance')
                obsList.append(stat +"to"+targ+"_d")
            
            
        if station[2].has_key('direction'):
            stat=station[0]
            targ=station[1]
            if not obs.hasStation(stat): obs[stat]=Station()
            if not obs[stat].hasTarget(targ): obs[stat][targ]=Target()
            obs[stat][targ].setDirection(station[2]['direction'])
            if obs[stat][targ].type == "distance":
                obs[stat][targ].setType('both')
            else:
                obs[stat][targ].setType('direction')
                obsList.append(stat +"to"+targ+"_D")
    return obs,obsList
def obsSplit(obs):
        OBS=SurveyData()
        for sta,station in obs.iteritems():
            OBS[sta]=Station()
            
            for tar,target in station.iteritems():
                if target.type=='both':
                    OBS[sta][tar+" d"]=Target(distance=target.distance)
                    OBS[sta][tar+" d"].setType('distance')
                    OBS[sta][tar+" D"]=Target(direction=target.direction)
                    OBS[sta][tar+" D"].setType('direction')
                elif target.type=='direction':
                    OBS[sta][tar+' D']=Target(direction=target.direction)
                    OBS[sta][tar+" D"].setType('direction')
                elif target.type=='distance':
                    OBS[sta][tar+' d']=Target(distance=target.distance)
                    OBS[sta][tar+" d"].setType('distance')
                else:
                    print "error in OBS SPLIT : No type for target"
        return OBS 
def ErrorEllipse(priori, Qx,Qy,Qxy):

        priori=   priori**2
        i=(Qx+Qy)/2.
        k=sqrt((Qx-Qy)**2.+4*Qxy**2.)/2.
        q=sqrt((Qx-Qy)**2./4.+Qxy**2.)
        
        Asqr=priori*(i+k)
        Bsqr=priori*(i-k)
        theta=0.5*atan2((-2*Qxy),(Qx-Qy))
        while theta<0:
            theta+=pi

        a= (round(sqrt(Asqr),3))
        b= (round(sqrt(Bsqr),3))
        r= (round(theta*180./pi,0)) 
        return a,b,r
              
def getL(provis,obs,control):
#         print "================================================================================="
#         print "======    Calculate Misclosure L      ==========================================="
    
  
    
    count=obsCount(obs)
    L=numpy.zeros(shape=(count,1))
    Lnames=Points("L vector name pairs")
    i=0
    for sn1,station in obs.iteritems():
        for tn1,target in station.iteritems():
#             print sn1 +" to "+tn1+" "+target.type
            tn2=tn1
            tn1=tn1[0:-2]
            if target.type=="direction":
                if control.has_key(tn1):
                    if provis.has_key(sn1):
                        calc=provis[sn1].join(control[tn1])
                    elif control.has_key(sn1):
                        calc=control[sn1].join(control[tn1])
                    else:
                        print "no key in either prov or control ERROR"
                elif provis.has_key(tn1):
                    if provis.has_key(sn1):
                        calc=provis[sn1].join(provis[tn1])
                    elif control.has_key(sn1):
                        calc=control[sn1].join(provis[tn1])
                    else:
                        print "no key in either prov or control ERROR"
                else: 
                    print "error direction to unknown point"
                    calc=0
                observed=obs[sn1][tn2].direction
#                 target.setMisclosure((observed-calc)*180/pi*3600)
                L[i][0]=round((observed-calc)*180./pi*3600.,1)
#                 print sn1 + " "+tn1
#                 print L[i][0]
                
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
                else: print "error type is distance to unknown point"
                
                observed=obs[sn1][tn2].distance
                target.setMisclosure(observed-calc)
                L[i][0]=round((observed-calc),3)
                Lnames[sn1 + " to "+ tn1 + " distance"]=L[i][0]
#                 print sn1 + " "+tn1
#                 print L[i][0]
                i+=1   
    return L,Lnames
def getA(provis,OBS,control,unknowns):
        count=obsCount(OBS)
        L=getL(provis, OBS, control)
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
#                 print station_name +" to "+tname+" "+target.type
                j=0
#                 tname=tname[0:-2]
                if target.type=='direction' or target.type=='distance' :
                    for diff_wrt in unknowns:
                        
                        if diff_wrt[-1]=='o':
                            if station_name==diff_wrt[0:-2] and target.type=='direction':
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
                            
                        elif provis.has_key(tname):#if observing provisional
                                if target.type=="direction":
                                    A[i][j]=equations(current_station,provis[tname],diff_wrt,'direction')
                                else:
                                    A[i][j]=equations(current_station,provis[tname],diff_wrt,'distance')
                                j+=1
                                continue
                        else:
                            print "error in A matrix: Not control or provisional"
                            print station_name
                            print tname
                            break
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
def showGraph(N,provisionals,control):
    pos={}
    for nm,ob in provisionals.iteritems():
        x=ob.x
        y=ob.y
        pos[nm]=  (x,y)         
    for nm,ob in control.iteritems():
        x=ob.x
        y=ob.y
        pos[nm]=  (x,y)
    nx.draw_networkx_nodes(N,pos,
                       nodelist=provisionals,
                       node_color='y',
                       node_size=1,
                       alpha=0)
#     nx.draw_networkx_nodes(N,pos,
#                    nodelist=control,
#                    node_color='r',
#                    node_size=1,
#                    alpha=1)
    edges={}
    for v,u,d in N.edges(data=True):
        if d.has_key("distance") and d.has_key('direction'):
            edges[v,u]='b'
        
    T=N.copy()
    for i,j in control.iteritems():
        T.remove_node(i)
        
    nx.draw(T,pos,node_size=100,alpha=0,nodelist=provisionals)
    nx.draw_networkx_edges(N,pos,
                   edgelist=edges,
                   width=1,alpha=0.5,edge_color='b')

    plt.show()    
def adjustProvisional(X,provisional,obs,unknowns): 
    i=0
    j=0
    provis = provisional.Totalcopy()
    for ideas in unknowns:
        name=ideas[0:-2]
        type= ideas[-1]
        if type=="x":
            provis[name].x=provisional[name].x + float(X[ideas])
        elif type=="y":
            provis[name].y=provisional[name].y + float(X[ideas])
#         if type=='o':
#             for sname,station in obs.iteritems():
#                     if sname==name:
#                         for tname,target in station.iteritems():
#                              
#                             if target.type=="direction":
#                                 temp=float64(target.direction)+float64(X[ideas]*pi/180.)
#                                 while temp>=2*pi:
#                                     temp=temp-2*pi
#                                 while temp<-2*pi:
#                                     temp=temp+2*pi
#                                 target.setDirection(temp)

                
        j+=1
        
    return provis 
def adjustProvisionalI(X,provisional,obs,unknowns): 
    i=0
    j=0
    provis = provisional
    for ideas in unknowns:
        name=ideas[0:-2]
        type= ideas[-1]
        if type=="x":
            provis[name].x=provisional[name].x - float(X[ideas])
        elif type=="y":
            provis[name].y=provisional[name].y - float(X[ideas])
        if type=='o':
            pass

                
        j+=1
        
    return provis

def Iterate(provis,OBS,control,unknowns,P):
        count=obsCount(OBS)
        
        L,Lnames=getL(provis, OBS, control)
#         print "==============        A Matrix        ========================================="
        
        A=getA(provis,OBS,control,unknowns)
        names=[]
        for name,ob in OBS.iteritems():
            for na,tar in ob.iteritems():
                if tar.type=="both":
                    names.append(name + "-" + na + "D")
                    names.append(name + "-" + na + "d")
                else:
                    names.append(name + "-" + na + "D")
    
                    
#         row_labels = ['SUR09-T013', 'Y', 'N', 'W']
#         for row_label, row in zip(names, A):
#             print '%s [%s]' % (row_label, '      '.join('%01f' % i for i in row))          
   
#         print "==============        Calculating Least squares       ========================================="
        
        
        
#         A=numpy.asmatrix(A)
        X= (((A.T)*P*A)**(-1))*A.T*P*L
        
        Xdict=Points("Solutions Dictionary")
        j=0
        for i in unknowns:
            Xdict[i]=X[j]
            j+=1
        provUpdate=adjustProvisional(Xdict,provis,OBS,unknowns)
        Xtemp=Points("N correction pairs")
        i=0
        
        for name in unknowns:
            Xtemp[name]=float64(X[i])
            i+=1



        return A,Xtemp , provUpdate , OBS , control , unknowns,L
def globalCheck(provis,control,V,obs,unknowns,X):
    check=Points("global Check")
    i=0
    for stat,station in obs.iteritems():
        for tar,target in station.iteritems():
            tar=tar[0:-2]
            if target.type =="distance":
                if control.has_key(stat) and provis.has_key(tar):
                    newD=sqrt((provis[tar].y-control[stat].y)**2 + (provis[tar].x-control[stat].x)**2)
                    check[stat + " to " + tar + " "+ target.type]=target.distance + V[i] - newD
                    i+=1
                elif provis.has_key(stat) and provis.has_key(tar):
                    newD=sqrt((provis[tar].y-provis[stat].y)**2 + (provis[tar].x-provis[stat].x)**2)
                    check[stat + " to " + tar + " "+ target.type]=target.distance + V[i] - newD
                    i+=1
                elif provis.has_key(stat) and control.has_key(tar):
                    newD=sqrt((control[tar].y-provis[stat].y)**2 + (control[tar].x-provis[stat].x)**2)
                    check[stat + " to " + tar + " "+ target.type]=target.distance + V[i] - newD
                    i+=1
                else:i+=1
            elif target.type =="direction":
                if control.has_key(stat) and provis.has_key(tar):
                    newD=atan2( (provis[tar].y-control[stat].y), (provis[tar].x-control[stat].x))
                    check[stat + " to " + tar + " "+ target.type]=target.direction + float(V[i])/3600*pi/180. - newD +(X[stat+"_o"])/3600*pi/180.
                    while check[stat + " to " + tar + " "+ target.type]>1.99*pi:
                        check[stat + " to " + tar + " "+ target.type]=check[stat + " to " + tar + " "+ target.type]-2*pi
                    i+=1
                elif provis.has_key(stat) and provis.has_key(tar):
                    newD=atan2( (provis[tar].y-provis[stat].y), (provis[tar].x-provis[stat].x))
                    check[stat + " to " + tar + " "+ target.type]=target.direction + float(V[i])/3600*pi/180. - newD +(X[stat+"_o"])/3600*pi/180.
                    while check[stat + " to " + tar + " "+ target.type]>1.99*pi:
                        check[stat + " to " + tar + " "+ target.type]=check[stat + " to " + tar + " "+ target.type]-2*pi
                    i+=1
                elif provis.has_key(stat) and control.has_key(tar):
                    newD=atan2( (control[tar].y-provis[stat].y), (control[tar].x-provis[stat].x))
                    check[stat + " to " + tar + " "+ target.type]=target.direction + float(V[i])/3600*pi/180. - newD +(X[stat+"_o"])/3600*pi/180.
                    while check[stat + " to " + tar + " "+ target.type]>1.99*pi:
                        check[stat + " to " + tar + " "+ target.type]=check[stat + " to " + tar + " "+ target.type]-2*pi
                    i+=1
                else:i+=1
            else: i+=1    
#     for i,j in check.iteritems():
#         print i
#         print j
    return check
def Test(test):
    if test == 0:
        N=Observations("complete2.csv")
        control = controlPoints(N,"controlTest.csv")
    if test == 1:
        N=Observations("resection.csv")
        control = controlPoints(N,"E:\\==Programming==\\==Python Projects==\\Geomatics\\LeastSquaresProject\\control.csv")
    if test ==2 :
        N=Observations("E:\\==Programming==\\==Python Projects==\\Geomatics\\LeastSquaresProject\\observations.csv")
        control = controlPoints(N,"E:\\==Programming==\\==Python Projects==\\Geomatics\\LeastSquaresProject\\control.csv")
    if test == 3:
        N=Observations("testObservations.csv")
        control = controlPoints(N,"controlTest.csv")
    if test == 4:
        N=Observations("intersection.csv")
        control = controlPoints(N,"E:\\==Programming==\\==Python Projects==\\Geomatics\\LeastSquaresProject\\control.csv")
    if test == 5:
        N=Observations("triangulation.csv")
        control = controlPoints(N,"E:\\==Programming==\\==Python Projects==\\Geomatics\\LeastSquaresProject\\controlTriangulation.csv")
    if test == 6:
        N=Observations("trilateration.csv")
        control = controlPoints(N,"E:\\==Programming==\\==Python Projects==\\Geomatics\\LeastSquaresProject\\control.csv")
    if test == 7:
        N=Observations("traverse1.csv")
        control = controlPoints(N,"traverse1_control.csv")
    return N,control
   
    
def precisions(A,X,P,L,obs,unknowns):
    V=A*X-L
    Vdict=Points("Variance dictionary")
    j=0
    for i in unknowns:
        Vdict[i]=V[j]
        j+=1
    Xtemp=Points("N correction pairs")
    i=0
    for name in unknowns:
            Xtemp[name]=float64(X[i])
            i+=1
    count=obsCount(obs)
#     if float(round(float((A.T*P*V).T*(A.T*P*V)),12))==0.:
#         print "----------------------\nCalculation check 'A.tPV' successful\n______________________"
#     else:
#         print "check calculations"
#     print float (V.T*P*V)/(count-len(unknowns))
    posteriori=float((V.T*P*V)/float(count-len(unknowns)))
    covarience_mat= posteriori*(A.T*P*A)**(-1)
    precisions=Points("Precisions of Unknowns")
    i=0
    Qxi,Qyi=0,0
    for name in unknowns:
        
        precisions[name]=sqrt(float(covarience_mat[i,i]))
        
#         precisions[name+"xy"]=sqrt(float(covarience_mat[i,i]))
        i+=1

    return V,posteriori,covarience_mat,precisions

    ##ACCESS NETWORK N VARIABLES
#     edges = dfs_edges(N,'menzies')#start function iteration , send 3 as source
#     for e in edges:#edges in order
#         print e
#         print N[e[0]][e[1]][0]
# 
#     for n in N.edges_iter(data=True):
#         print n

 