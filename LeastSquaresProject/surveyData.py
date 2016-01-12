'''
Created on Mar 24, 2014

@author: 01410541
'''

from numpy import radians, float64, pi

from LeastSquaresProject.display import dec2dms
from LeastSquaresProject.station import Station
from target import Target
import networkx as nx
import matplotlib.pyplot  as plt
class SurveyData(dict):
    

    def __init__(self,name='unknown'):
        
        self.name=name
        distances=[]
        

                
    def read(self, filename,control):
        c0=0#Code
        c1=1#Setup    #COLUMNS FOR FILE INPUT: first column in excell is c0
        c2=2#Target
        c3=3#direction
        c4=4#distance
        c5=5#known
        count=0
        N=nx.Graph()
        custom_edge_color={}
#         custom_edge_color['A','B'] = 'c'
        
        f = open(filename, 'r')    
        f.readline()
        station_name='temp'
        for line in f:
            sp = line.split(',')
            
            if(int(sp[0]) == 0) : #if code equals zero, its a station
                station_temp=station_name
                station_name = sp[c1]
                if control.has_key(station_name):
                    self[station_name] = Station(control[station_name])  # this is NNNNNBBBBBBBB Use code to create station whenever new station
                    x= self[station_name].point.x
                    y= self[station_name].point.y
                    loc=(x,y)
                    N.add_node(station_name,location=loc)
                elif not self[station_name].point==None :
                    print "ok.."
                else:
                    print "error: "+ station_name
                    
                #                                 then
               
            elif(int(sp[0]) == 1): #if code equals 1, its an direction to a target
                count+=1
                target_name = sp[c2]
                station = self[station_name]#get a reference to the current station object, where you will keep your target object with its info
#                 
#                 if not station.has_key(target_name):#if observation "station" doesn't have target name as key yet,
#                     station[target_name] = Target()# create the new Target object within Observation dictionary
#                 station[target_name].setType('direction')    
#                 station[target_name].setDirection(radians(float64(sp[c3])))# then set the direction of current target object
                if not station.has_key(target_name):
                    station[target_name] = Target()
                    station[target_name].setType('direction')  
                    station[target_name].setDirection(radians(float64(sp[c3])))
                    N.add_edge(station_name,target_name,direction=radians(float64(sp[c3])))
                elif station[target_name].type=='distance':
                    N.add_edge(station_name,target_name,direction=radians(float64(sp[c3])))
                    custom_edge_color[station_name,target_name] = 'c'
                    station[target_name].setType('both')  
                    station[target_name].setDirection(radians(float64(sp[c3])))
                    self[target_name]=Station(self[station_name].point.polar(self[station_name][target_name].distance,self[station_name][target_name].direction))
#                     self[target_name].setPoint(self[station_name].point.polar(self[station_name][target_name].distance,self[station_name][target_name].direction))
                
            elif(int(sp[0]) == 2):#else, if code is 2, for distance
                count+=1
                target_name =  sp[c2]#get the target name
                station = self[station_name]#create an observation dictionary object to put a target object into
                # the target object will have both a direction and a distance, and is an observation.

                if not station.has_key(target_name):
                    station[target_name] = Target()
                    station[target_name].setType('distance')  
                    station[target_name].setDistance(float64(sp[c4]))
                    N.add_edge(station_name,target_name,distance=float64(sp[c4]))
                elif station[target_name].type=='direction':
                    station[target_name].setType('both')  
                    station[target_name].setDistance(float64(sp[c4]))
                    N.add_edge(station_name,target_name,distance=float64(sp[c4]))
                    custom_edge_color[station_name,target_name] = 'c'
                    self[target_name]=Station(self[station_name].point.polar(self[station_name][target_name].distance,self[station_name][target_name].direction))
#                     self[target_name].setPoint(self[station_name].point.polar(self[station_name][target_name].distance,self[station_name][target_name].direction))
        pos={}
        for nm,ob in self.iteritems():
            x=ob.point.x
            y=ob.point.y
            pos[nm]=  (x,y)         
        for nm,ob in control.iteritems():
            x=ob.x
            y=ob.y
            pos[nm]=  (x,y)         
#         nx.draw(N,pos)
#         plt.show()
        return count,N,pos
                        
    def __str__(self):
        print "________"+self.name+"________"
        for i,j in self.iteritems():
            for x,y in j.iteritems():
                if y.type == 'both':
                    print "Station: " + i + " "+ "Observed: "+ x + " "+"direction: "+str(dec2dms(y.direction*180/pi))+" \nStation: "+ i + " "+ "Observed: "+ x +" "+ "distance: "+str(y.distance)+"m"
                      
                elif y.type == 'direction':
                    type=y.type
                    print "Station: "+ i + " "+ "Observed: "+ x + " "+type+": " + str(dec2dms(y.direction*180/pi))                      
                elif y.type == 'distance':
                    type=y.type
                    print "Station: "+ i + " "+ "Observed: "+ x + " "+type+": " + str((y.distance))        + "m"              
        print"++++++++++++++++++++++++++++++++++++++++\n"
        return " "
                
    def hasStation(self,station):
        if self.has_key(station):
            return True
        else:
            return False
                
    def hasTarget(self,station):
        if self.has_key(station):
            return True
        else:
            return False
