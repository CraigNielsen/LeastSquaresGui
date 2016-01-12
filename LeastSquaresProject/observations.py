'''
Created on Apr 3, 2014

@author: Craig
'''
from numpy import pi, float64

from LeastSquaresProject.display import dec2dms
from LeastSquaresProject.display import rad2dms
from LeastSquaresProject.station import Station
from LeastSquaresProject.target import Target
import networkx as nx

class ObsSplit(dict):
    '''
    classdocs
    '''


    def __init__(self, name):
        self.name=name
    def read(self,obs,control):
        OBS=ObsSplit(self.name)
        for sta,station in obs.iteritems():
            OBS[sta]=Station(station.point)
            for tar,target in station.iteritems():
                if target.type=='both':
                    OBS[sta][tar+" d"]=Target(distance=target.distance)
                    OBS[sta][tar+" d"].setType('distance')
                    OBS[sta][tar+" D"]=Target(direction=target.direction)
                    OBS[sta][tar+" D"].setType('direction')
                else:
                    OBS[sta][tar+' D']=Target(direction=target.direction)
                    OBS[sta][tar+" D"].setType('direction')
        return OBS
    def __str__(self):
        print "\n_________" + self.name + "_________\n" 
        for i,j in self.iteritems():
            for x,y in j.iteritems():
                if y.type == 'direction':
                    print "Station: " + i + " "+ "Observed: "+ x + " "+"direction: "+str(dec2dms(y.direction*180/pi))
                      
                else:
                    print "Station: "+ i + " "+ "Observed: "+ x +" "+ "distance: "+str(y.distance)+"m"                   
        print"++++++++++++++++++++++++++++++++++++++++\n"
        return " "
                
                    
                    
                
                
                