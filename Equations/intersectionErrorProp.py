'''
Created on Mar 5, 2014

@author: Craig
'''




import math

from matplotlib import cm
from matplotlib.mlab import griddata
from numpy import radians, tan, sqrt, cos, sin, arctan2, degrees
import numpy
from scipy import arctan, interpolate

from IntSecProject1.InterS2 import inters
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def heatmap(tD):
    
    ##==============           INITIAL VALUES BETWEEN 1 and 20                        ==============
    #===============           divide all coords by Ymax if Y and Xmax if N, then multiply by 20
    Xa= 4.
    Ya= 10.
    Xb= 16.
    Yb= 4.0
    print "Calculating..."
    angleGrace=0.1 # the fucntion gets unstable as delta nears zero (as points A and B get closer to each other), this value controls this instability
    threshold=0.01 #this value controls the range of the error model, set this value higher for accurate error values, but lower for better image generation 
    tD= tD
    #the tD is the std dev associated with directions
#     eXa= 0.007
#     eYa= 0.005
#     eXb= 0.009
#     eYb= 0.005
    def RMS(tAB, tAN, sAN, eAn):
        
        eX= (sAN*sin(tAN))**2*(tD)**2 + (cos(tAN)**2)*eAn**2
        eY= (sAN*cos(tAN))**2*(tD)**2 + (sin(tAN)**2)*eAn**2
        return sqrt(eX + eY)
    def joinT(yb,ya,xb,xa):
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
            
        return tAn #TBN
#     print joinT(200,100,-300,-150)
#     print joinT(100.,100.,-300.,-150.)    
    
    def joinS(yb2,ya2,xb2,xa2):
        dya=yb2-ya2
        dxa=xb2-xa2
        
        sAB=sqrt(dya**2+dxa**2)

        return sAB #TBN    
    tAB= joinT(Yb,Ya,Xb,Xa)
    tBA= joinT(Ya,Yb,Xa,Xb)
    sAB= joinS(Yb,Ya,Xb,Xa)
    
    def EAN(beta,delta):
        
        eD= tD**2 + tD**2
        if ( delta==0.0 or delta==-2*math.pi or delta==math.pi*2):
#             print "delta = : " + "beta :" +  str(beta)+ " delta :" +  str(delta)
            return threshold
        if ((0.- angleGrace) < delta < 0.+angleGrace):
            error = threshold
            return error
        elif ((math.pi*2.- angleGrace) < delta < (math.pi*2.+angleGrace) ):
            error = threshold
            return error
        elif (math.pi- angleGrace < delta < math.pi +angleGrace):
            error = threshold
            return error
        elif( math.pi*3.- angleGrace < delta < math.pi*3.+angleGrace ):
            error = threshold
            return error
        
        elif (  math.pi*4.- angleGrace < delta < math.pi*4.+angleGrace):
            error = threshold
            return error
        
        error=sqrt( (sAB*cos(beta)/sin(delta))**2*tD**2 + (sin(beta)/(sin(delta)**2)*cos(delta)*sAB)**2*eD)
#         if (error>0.5): 
#             print "beta" + str(degrees(beta))
#             print "delta" + str(degrees(delta))
#             print "error :"
#             print "                 " + str(error)       
        
        return error
    
    
    
    xpl = numpy.arange(-1, 20, 0.2)   # no need for .tolist()
    ypl = numpy.arange(-1, 20, 0.2)  # meshgrid can work with numpy.array's
#     print "ypl: " + str(ypl)

    
    z = ['']  
    x = ['']
    y = ['']      
    for x2 in xpl:
        for y2 in ypl:
            
            tAN=joinT(y2,Ya,x2,Xa) #join from A to N
            tBN=joinT(y2,Yb,x2,Xb) #join from B to N
            sAN= joinS(y2,Ya,x2,Xa)
            sBN= joinS(y2,Yb,x2,Xb)
            alpha=tAB-tAN
            while (alpha<0):
                alpha=alpha+2*math.pi
            beta = tBN-(tBA)
            while (beta<0):
                beta=beta+2*math.pi

            delta=math.pi - alpha - beta
            while (delta<0):
                delta=delta+2*math.pi

            eAn=EAN(beta,delta)
            eBn=EAN(alpha,delta)
            x.append(x2)
            y.append(y2)
            I=RMS(tAB, tAN, sAN,eAn)
            K=RMS(tAB+math.pi, tBN, sBN,eAn)
            if (K<I):
                z.append(K)
            else : z.append(I)
#             print    "x: " + str(x2) + " and y: " + str(y2)
            
    del z[0]
    del x[0]
    del y[0]
#     print z.shape
#     print x
#     print "====================================================================================================================="
#     print "from:"
#     print "Xa: " + str(Xa) + "     Xb: " + str(Xb)
#     print "Ya: " + str(Ya) + "     Yb: " + str(Yb)
#     print "=====================================================================================================================" 
#     print "N : \n" + str(x)
#     print "Y : \n" +str(y) 
#     print "RMS : \n" + str(z)
    print "====================================================================================================================="
    print "Note: \n"
    print " ## this program is meant to illustrate areas of weakness, and as a surveyor, you would know areas to avoid doing the intersection. \n The error in these areas are controlled in this program, all other error values are accurate."
    print "====================================================================================================================="
     
    window3(x,y,z)
    
def window3(x,y,z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x = x
    y = y
    z = z
    
    
    xi = np.linspace(1, 19)# axis values go here
    yi = np.linspace(1, 19)
    
    N, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)
    
    surf = ax.plot_surface(N, Y, Z, rstride=3, cstride=3, cmap=cm.jet,
                           linewidth=0, antialiased=True)
    
    ax.set_zlim3d(np.min(Z), np.max(Z))
    fig.colorbar(surf)
    def getMarker(i):
    # Use modulus in order not to have the index exceeding the lenght of the list (markers)
        return "$"+'\gamma'+"$"
    plt.xlabel('N', fontsize=18)
    plt.ylabel('Y', fontsize=18)
    plt.title("Intersection Error figure. \n View from top for heatmap")
    
    plt.show()
    

if __name__ == '__main__':
#     np.seterr(invalid='ignore')
    heatmap(radians(20./3600.))