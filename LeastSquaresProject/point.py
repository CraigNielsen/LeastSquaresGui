'''
Created on Mar 17, 2014

@author: 01410541
'''


from numpy import arctan, math, sqrt, cos, sin


class Point(object):
    '''
    classdocs
    '''


    def __init__(self, x, y, h, known,name):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.h = h
        self.known=known
        self.name=name
        
    def setKnown(self,k):
        self.known = k   
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
        dya=yb-ya+0.
        dxa=xb-xa+0.
        distance= sqrt(dxa**2+dya**2)
        return distance #TBN
#     print joinT(200,100,-300,-150)
#     print joinT(100.,100.,-300.,-150.) 
    def polar(self,d,t):
        return Point(self.x+d*cos(t), self.y+d*sin(t), 0., False, "unknownName") 
    def __str__(self):
        return "X: " + str(round(self.x,2)) +"m\nY: " + str(round(self.y,2)) +"m\nH: " + str(round(self.h,2)) + "m\n"   
    
    def ChangeVariable(self,variable,value):
        if self.known==True:
            print "Known Point Error, Change to unknown"
            return
        if variable=="x":
            self.x = value
        if variable=="y":
            self.y = value
        if variable=="h":
            self.h = value      
               