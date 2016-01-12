'''
Created on Mar 24, 2014

@author: 01410541
'''
from numpy import float64


class Target(object):
    '''
    classdocs
    '''


    def __init__(self,distance=None,direction=None):
        '''
        Constructor
        '''
        self.direction = direction
        self.distance = distance
        self.misclosure = None
        self.type='unknown'
        
    def setDirection(self,direction):
        self.direction = float64(direction)
        
    def setDistance(self,distance):
        self.distance = float64(distance)
    def setMisclosure(self,misclosure):
        self.misclosure = float64(misclosure)
    def setType(self,t):
        if self.type=='unknown':
            self.type = t
        else:
            self.type = 'both'
        
        
    def __str__(self):
        return "Direction : "+ str(self.direction)+"\nDistance : "+str(self.distance)+"\nMisclosure : "+str(self.misclosure)+"\n"
