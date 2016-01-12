'''
Created on Mar 24, 2014

@author: 01410541
'''
from LeastSquaresProject.point import Point


class Station(dict):
    '''
    classdocs
    '''


    def __init__(self):
        
        self.point = None
        self.orientation=None
        self.known=False
            
    def setPoint(self,Point1):
        self.point = Point1
        
    def setOrientation(self,o):
        self.oreintation=o
    def setKnown(self,o):
        self.known=o
    def hasTarget(self,station):
            if self.has_key(station):
                return True
            else:
                return False