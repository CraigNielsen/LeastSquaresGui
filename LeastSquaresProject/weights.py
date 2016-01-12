'''
Created on Apr 1, 2014

@author: Craig
'''
import numpy


class Weights(dict):
    '''
    classdocs
    '''


    def __init__(self,distanceWeight=None,directionWeight=None):
        self.distanceWeight=distanceWeight
        self.directionWeight=directionWeight
        
    def setDistanceWeight(self,v):
        self.distanceWeight=v
    def setDirectionWeight(self,v):
        self.directionWeight=v
        
    def read(self,filename):
        print "not setup yet"
    
    def matrix(self,observations,A):
        r,c=A.shape
        P= numpy.zeros(shape=(r,r))
        i=0
        j=0
        for stat,station in observations.iteritems():
            for tar,target in station.iteritems():
                if target.type=="both":
                    P[i][j]=self.directionWeight
                    i+=1
                    j+=1
                    P[i][j]=self.distanceWeight
                    i+=1
                    j+=1
                    continue
                elif target.type=='distance':
                    P[i][j]=self.distanceWeight
                    i+=1
                    j+=1
                    continue
                elif target.type=='direction':
                    P[i][j]=self.directionWeight
                    i+=1
                    j+=1
                    continue
                else:
                    print "error"
                    P[i][j]= -666
                    i+=1
                    j+=1
                    continue
            
        return numpy.asmatrix(P)
                    
        