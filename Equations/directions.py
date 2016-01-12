'''
Created on Mar 30, 2014

@author: Craig
'''
from math import pi

from LeastSquaresProject import point



    
def equation(self,point1,point2,id):  
    x1=point1.x
    y1=point1.y
    x2=point2.x
    y2=point2.y
    d21=point.joinS(point1,point2)
    
    a=self.p*(x2-x1)/d21^2.
    b=self.p*(y2-y1)/d21^2.
    
    if id=="y1":
        return -a 
    if id=="y2":
        return a 
    if id=="x1":
        return b 
    if id=="x2":
        return -b 
        
          