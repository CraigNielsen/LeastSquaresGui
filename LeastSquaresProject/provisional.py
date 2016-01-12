'''
Created on Mar 28, 2014

@author: Craig
'''

class Provisional():
    '''
    classdocs
    '''


    def __init__(self):
        
        self.name=None
        self.x = None
        self.y = None
        self.h = None
    
    def setProvisional(self,name,x,y,h):
        self.name=name
        self.x = float(x)
        self.y = float(y)
        self.h = float(h)