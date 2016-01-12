'''
Created on Mar 7, 2014


@author: Craig Ferguson
Student number :                                                 FRGCRA003
'''
from math import sqrt
import math
from matplotlib import cm
from matplotlib.mlab import griddata
from numpy import  arctan, radians,  sin, cos
from sympy.functions.elementary.trigonometric import tan
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy as sy


def easyR():
#===================================================================================================================================================
    
    #   Range and Domain 0-100 , interval 5. Keep coordinates in this format
    
    Xa2=20.
    Ya2=80.
    Xb2=20.
    Yb2=20.
    Xc2=80.
    Yc2=50.
    
    eT= radians(60./60.)    #=== Error in directions
    threshold=0.02          #==threshold to control danger circle uncertainty, and adjust depth of figure as wanted
    
#===================================================================================================================================================
#===================================================================================================================================================
#==================       Error Equations E and F Calculated using diff() function prior to running to lighten resources     =======================

    print "Calculating..."
    
    tA,tB = sy.symbols('tA,tB')
    dtA=eT**2 + eT**2
    #   check() also calculates error propagation by means of matrix multiplication, used as a check
    def check():
        
        Xa,Ya,Xb,Yb,Xc,Yc, = sy.symbols('xa,ya,xb,yb,xc,yc')
#         dtA,dx2,dx3,dx4 = sy.symbols('dtA,dx2,dx3,dx4')
        tNBtop= -(Xc-Xa)+(Yc-Yb)*sy.cot(tB) +(Ya-Yb)*sy.cot(tA)
        tNBbot= (Yc-Ya)+(Xc-Xb)*sy.cot(tB)+(Xa-Xb)*sy.cot(tA)
        dtA=eT**2 + eT**2
        TNB=[[sy.atan(tNBtop/tNBbot)]]
#         print TNB
        params = [tA,tB]
        Cov = sy.Matrix([[dtA, 0],
                         [0, dtA]])
        A = sy.Matrix(TNB)
        J = A.jacobian(params)
        eProp = J*Cov*J.T
        return eProp.subs(Xa,Xa2).subs(Xb,Xb2).subs(Xc,Xc2).subs(Ya,Ya2).subs(Yb,Yb2).subs(Yc,Yc2)

    
    #partial differentials squared multiply by error squared
    
#========            PARTIAL DERIVATIVES^2 * Variance for E:alpha and F:beta    
    E=((-(Xa2 - Xb2)*(-tan(tA)**2 - 1)*(Xa2 - Xc2 + (Ya2 - Yb2)/tan(tA) + (-Yb2 + Yc2)/tan(tB))/((-Ya2 + Yc2 + (Xa2 - Xb2)/tan(tA) + (-Xb2 + Xc2)/tan(tB))**2*tan(tA)**2) + (Ya2 - Yb2)*(-tan(tA)**2 - 1)/((-Ya2 + Yc2 + (Xa2 - Xb2)/tan(tA) + (-Xb2 + Xc2)/tan(tB))*tan(tA)**2))/((Xa2 - Xc2 + (Ya2 - Yb2)/tan(tA) + (-Yb2 + Yc2)/tan(tB))**2/(-Ya2 + Yc2 + (Xa2 - Xb2)/tan(tA) + (-Xb2 + Xc2)/tan(tB))**2 + 1))**2*dtA
    F=((-(-Xb2 + Xc2)*(-tan(tB)**2 - 1)*(Xa2 - Xc2 + (Ya2 - Yb2)/tan(tA) + (-Yb2 + Yc2)/tan(tB))/((-Ya2 + Yc2 + (Xa2 - Xb2)/tan(tA) + (-Xb2 + Xc2)/tan(tB))**2*tan(tB)**2) + (-Yb2 + Yc2)*(-tan(tB)**2 - 1)/((-Ya2 + Yc2 + (Xa2 - Xb2)/tan(tA) + (-Xb2 + Xc2)/tan(tB))*tan(tB)**2))/((Xa2 - Xc2 + (Ya2 - Yb2)/tan(tA) + (-Yb2 + Yc2)/tan(tB))**2/(-Ya2 + Yc2 + (Xa2 - Xb2)/tan(tA) + (-Xb2 + Xc2)/tan(tB))**2 + 1))**2*dtA
    z7=E+F
#====================================================================================================================================================
#     check() was used as a check for the error calculated in the partial derivatives above. Both methods give the same answer.
#     z7 = check()
#====================================================================================================================================================
    
    
    
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
    def joinS(yb2,ya2,xb2,xa2):
        dya=yb2-ya2
        dxa=xb2-xa2
        
        sAB=sqrt(dya**2+dxa**2)

        return sAB #TBN       
    def intersection(Nx,Ny,Xa,Ya,Xb,Yb,tNa,Z):
        tAN= tNa+math.pi 
        sAN= joinS(Ny,Ya,Nx,Xa)
        eAn=Z
        eX= (sAN*sin(tAN))**2*(eT)**2 + (cos(tAN)**2)*eAn**2
        eY= (sAN*cos(tAN))**2*(eT)**2 + (sin(tAN)**2)*eAn**2
        return sqrt(eX + eY)
    def AddValues():    
        for Nx in xa:
            for Ny in ya:
                
                tNa=joinT(Ny,Ya2,Nx,Xa2) #join from N to A
                tNb=joinT(Ny,Yb2,Nx,Xb2) #join from N to B
                tNc=joinT(Ny,Yc2,Nx,Xc2) #join from N to C
                alpha=tNb-tNa
                beta= tNc-tNb
                
                while (alpha<0):
                    alpha=alpha+2*math.pi
                while (beta<0):
                    beta=beta+2*math.pi
                x.append(Nx)
                y.append(Ny)
                
                if ((Nx==Xa2 and Ny==Ya2) or (Nx==Xb2 and Ny==Yb2) or (Nx==Xc2 and Ny==Yc2)):
                    z2.append(10)
                else : z2.append(0)
                
                Z=((z7.subs(tA,alpha).subs(tB,beta))) + 0.0
                if (math.isnan(Z)):
    #                 print "N : " + str(Nx)
    #                 print "Y : " + str(Ny)
    #                 print "Z : " + str(Z)
    #                 print "Math Error"
                    Z=threshold
                if (Z>threshold):
                    Z=threshold
    #   check for the best geometry for intersection   
                i=intersection(Nx,Ny,Xa2,Ya2,Xb2,Yb2,tNa,Z**1.0/2)
                j=intersection(Nx,Ny,Xb2,Yb2,Xc2,Yc2,tNb,Z**1.0/2)
                k=intersection(Nx,Ny,Xc2,Yc2,Xa2,Ya2,tNc,Z**1.0/2)
                if (k<j and k<=i):
                    z3.append(k )
                elif (j<k and j<=i):
                    z3.append(j )
                elif (i<k and i<=j):
                    z3.append(i)
                else : z3.append(k)
                
                z.append(Z**1.0/2)
    def Display():
        del z[0]
        del x[0]
        del y[0]
        del z2[0]
        del z3[0]
        title1='Error Figure for Directions Accuracy to N from resection:\n threshold= ' + str(threshold)
        title2='Total RMS for Point N' 
        title0='Control Points...\nClose window to continue'
        print "Control Points Locations"
        window3(x,y,z2,threshold,title0)
        print "==================================================================================================================================================="
        print "==================================================================================================================================================="
        print "RMS error values for direction to N Y location Pairs:"
        window3(x,y,z,threshold,title1)
        print "==================================================================================================================================================="
        print "==================================================================================================================================================="
        print "Total RMS error values for N Y location Pairs after intersection:"    
        window3(x,y,z3,threshold,title2)    
    
    xa = np.arange(0,100,5.0)
    ya = np.arange(0,100,5.0)
    z = ['']  
    x = ['']
    y = ['']  
    z2 = ['']  
    z3 = ['']
    
    AddValues()            
    Display()    
    
def window3(x,y,z,threshold,titles):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    x = x     
    y = y
    z = z    
    def Output():
        print z
        print "N :"
        print x
        print "Y :"
        print y
    Output()    
    xi = np.linspace(1, 90)# axis values go here
    yi = np.linspace(1, 90)
    
    N, Y = np.meshgrid(xi, yi)
    Z = griddata(x, y, z, xi, yi)
    surf = ax.plot_surface(N, Y, Z, rstride=3, cstride=3, cmap=cm.jet,
                           linewidth=0, antialiased=True)
    
    ax.set_zlim3d(np.min(Z), np.max(Z))
    fig.colorbar(surf)
    plt.title(titles)
    plt.xlabel('N' , fontsize=18)
    plt.ylabel('Y', fontsize=18)
    plt.show()

if __name__ == '__main__':
    easyR()