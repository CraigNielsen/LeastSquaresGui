'''
Created on Mar 17, 2014

@author: 01410541
'''


from numpy import arctan, math, sqrt, cos, sin, float64


class Point(object):
    '''
    classdocs
    '''


    def __init__(self, x, y, h):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.h = h
        
    def __add__(self, p):
        return Point(self.x + p.x,
                     self.y + p.y,
                     self.h + p.h)
        
    def __sub__(self, p):
        return Point(self.x - p.x,
                     self.y - p.y,
                     self.h - p.h)   
    def join(self,p):
        yb,ya,xb,xa=p.y,self.y,p.x,self.x
        dya=yb-ya+0.
        dxa=xb-xa+0.
        
        if (dxa==0 and dya>0):
            tAn=math.pi/4.
            return tAn
        elif (dxa==0 and dya<=0):
            tAn=(3./2.)*math.pi
            return tAn
        elif (dya==0 and dxa>=0):
            tAn = 0.
            return tAn
        elif (dya==0 and dxa<0):
            tAn = math.pi
            return tAn
        
        else :   
            tAn= arctan(((dya)/dxa))
           
        
#         get correct quadrant
            if(dya<0 and dxa>0):
                tAn= tAn + 2*math.pi
            elif(dya<0 and dxa<0):
                tAn= tAn + math.pi
            elif(dya>0 and dxa<0):
                tAn= tAn + math.pi
        return (tAn) #TBN
    def joinS(self,p):
        yb,ya,xb,xa=p.y,self.y,p.x,self.x
        dya=float64(yb-ya+0.)
        dxa=float64(xb-xa+0.)
        distance= sqrt(dxa**2+dya**2)
        return distance #TBN
#     print joinT(200,100,-300,-150)
#     print joinT(100.,100.,-300.,-150.) 
    def polar(self,d,t):
        return self.x+d*cos(t),self.y+d*sin(t),0.  
    def __str__(self):
        return "X: " + str(self.x) +"\nY: " + str(self.y) +"\nH: " + str(self.h) + "\n"         
               