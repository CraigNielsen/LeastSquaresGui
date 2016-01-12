from numpy import pi, float64

from LeastSquaresProject.point import Point


def equations(point1,point2,identity,ob):
    if (identity[-1]=="x" or identity[-1]=="y"): 
        if point1.known and point2.known: return 0    
        if ob=="direction":
            return Directions(point1,point1.known,point2,point2.known,identity)
        
        elif ob=="distance":
            return Distances(point1,point1.known,point2,point2.known,identity)
    elif identity[-1]=="o":
        print "error!!! o"
        
    
def Directions(point1,known1,point2,known2,identity):
    if point1.known and point2.known: return 0
    p=3600.*180./pi
    x1=point1.x
    name1=point1.name
    name2=point2.name
    y1=point1.y
    h1=point1.h
    x2=point2.x
    y2=point2.y
    k1=point1.known
    k2=point2.known
    
    poi =Point(x1,y1,h1,k1,name1)
    d21=float64(poi.joinS(point2))**2
    a=p*(x2-x1)/d21
    b=p*(y2-y1)/d21
    

    
    if point2.known and not point1.known:  
    
        if identity[-1]=="y":
            return -a 
        if identity[-1]=="x":
            return b 
        
    elif point1.known and not point2.known: 
    
        if identity[-1]=="y":
            return a 
        if identity[-1]=="x":
            return -b 
    elif not point1.known and not point2.known: 
        if identity[0:-2]==name1:
            if identity[-1]=="y":
                return -a 
            if identity[-1]=="x":
                return b 
        if identity[0:-2]==name2:
            if identity[-1]=="y":
                return a 
            if identity[-1]=="x":
                return -b 

def Distances(point1,known1,point2,known2,identity):
    
    if point1.known and point2.known: return 0
    
    x1=point1.x
    y1=point1.y
    h1=point1.h
    name1=point1.name
    name2=point2.name
    x2=point2.x
    y2=point2.y
    k1=point1.known
    k2=point2.known
    
    poi =Point(x1,y1,h1,k1,name1)
    d21=float64(poi.joinS(point2))
    
    a=(y2-y1)/d21
    b=(x2-x1)/d21
    
    
    
    if point2.known and not point1.known: 
    
        if identity[-1]=="y":
            return -a 
        if identity[-1]=="x":
            return -b 
        
    elif point1.known and not point2.known: 
    
        if identity[-1]=="y":
            return a 
        if identity[-1]=="x":
            return b 
    elif not point1.known and not point2.known: 
        if identity[0:-2]==name1:
            if identity[-1]=="y":
                return -a 
            if identity[-1]=="x":
                return -b 
        if identity[0:-2]==name2:
            if identity[-1]=="y":
                return a 
            if identity[-1]=="x":
                return b 

# def Orientation():   