'''
Created on Mar 2, 2014

@author: Craig
'''







import math

import numpy
import scipy 


import sympy as sp;



class Resection():
 
     
        
    def __init__(self):

#         %--------read in from file-----CSV--Y.N.DD-------------
        data = numpy.genfromtxt('E:\\==--GEOMATICS--==\\===---SUBJECTS BAckUP---===\\=second year=\\Surveying\\Work Experience\\traverse check\\data points etc\\atbase2.csv', delimiter = ',');    
#            
        n=data.shape[0];
        k=0;
        Y = [];
        N= [];
        A = [];
        while  (k<n):
            
            Y.append(data[k,0]);
            N.append(data[k,1]);
            A.append(math.radians((data[k,2])));
            k=k+1;
           
        print('=======================================================');
#            
        if (n<3):
            print('not enough points for resection');
        if (n==3):
            print('no degrees of freedom');
        
        print ('=======================================================');
#            
#            % calculation of provisional coordinates using observations...........
#            %=====================================================================

        alpha=A[1]-A[0];
        
        if (alpha<0): 
            alpha=alpha+360*math.pi/180;
        beta=A[2]-A[1];
        if (beta<0): 
            beta=beta+360*math.pi/180;
        charlie=A[0]-A[2];
        if (charlie<0): 
            charlie=charlie+360*math.pi/180;

        
        Talpha=math.tan(alpha);
        Tbeta=math.tan(beta);
        print('unsafe if near zero:' + '%.3f or:'  % Talpha + '%.3f ' % Tbeta);
        print('=======================================================');
         
         
#            %coord differences BAX: B minus A in N & BAY: B minus A in Y
        BAX=N[1]-N[0];
        BAY=Y[1]-Y[0];
        BCX=N[1]-N[2];
        BCY=Y[1]-Y[2];
        ACX=N[1]-N[2];
        ACY=Y[1]-Y[2];
#            
#         %=======BLUNTS METHOD FORMULA==========================================
        def cot(x):
            return 1/(math.tan(x))
        
        deltaY= -(N[2]-N[0])+(Y[2]-Y[1])*cot(beta)+(Y[0]-Y[1])*cot(alpha);
        print 'delta .....';
        print deltaY;
        deltaX= (Y[2]-Y[0])+(N[2]-N[1])*cot(beta)+(N[0]-N[1])*cot(alpha);
        print deltaX;
        tNB=math.atan(deltaY/deltaX);
        
#         %check quadrant==========
        if (deltaY>0) and (deltaX<0):
            tNB=tNB+math.pi;
        elif ((deltaY<0) and (deltaX<0)):
            tNB=tNB+math.pi;
        elif (deltaY<0) and (deltaX>0):
            tNB=tNB+2*math.pi;
#     %=========================
        
        
        
        Dcorrection=tNB-A[1];
#         %    display(degrees2dms(radtodeg(Dcorrection)));
        Ac=[[],[],[]]; 
        Ac[0]=A[0]+ Dcorrection;
        Ac[1]=A[1]+ Dcorrection;
        Ac[2]=A[2]+ Dcorrection;
        t1N=Ac[0]+math.pi;
        t2N=Ac[1]+math.pi;
        t3N=Ac[2]+math.pi;
#            
        print "y[0]"
        print Y[0]
        print N[0]
        print A[0]
        print Y[1]
        print N[1]
        print A[1]
        
#            %========calculate intersection for provisional point=========
#         t= Intersection;
#         NX1,NY1 = t.intersect (Y[0],N[0],A[0],Y[1],N[1],A[1]);
#            NX1= N(1)+((Y(2)-Y(1))-(N(2)-N(1))*tan(t2N))/(tan(t1N)-tan(t2N));
#            NY1= Y(1) + (NX1-N(1))*tan(t1N);
        NX1= N[0]+((Y[1]-Y[0])-(N[1]-N[0])*math.tan(t2N))/(math.tan(t1N)-math.tan(t2N));
        NY1= Y[0] + (NX1-N[0])*math.tan(t1N);
        NX1old=NX1;
        NY1old=NY1;
        
        
        print('Provisional Coordinates:');
        print ('N : %0.3f' % NX1);
        print ('Y : %0.3f' % NY1);
            

#            
#            
#         %+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         %+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#         %+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#            
#            
#         %calculations for least squares..........
#            
#            
#            %NX1=round(NX1);
#            %NY1=round(NY1);
#            
#                                    %CN(1): calculated direction from N to point(1)
        k=0;
        CtN=[0]*n;
        print CtN;
        print 'n: ' + str(n);
        while (k<n): 
            print k;
            a=(Y[k]-NY1);
            b=(N[k]-NX1);
            CtN[k]= math.atan(a/b);
#           %check quadrant==========
            if (a>0) and (b<0) :
                CtN[k]=CtN[k]+math.pi;
            elif (a<0) and (b<0) :
                CtN[k]=CtN[k]+math.pi;
            elif (a<0) and (b>0) :
                CtN[k]=CtN[k]+2*math.pi;
#           %=========================

            k=k+1;

#             
#           
#            
#         %    display(degrees2dms(radtodeg(CtN)));
#                     %Mt(1) : Misclosue for direction to point (1)
        k=0;
        Mt=[0]*n;
        while (k<n):
            
            Mt[k]= (A[k]-CtN[k])*3600*180/math.pi;
            k=k+1;
#                                                             %    misclosr vector
#         %    display(degrees2dms(radtodeg(Mt)));
#            
        p=1*180/math.pi*3600;
#    =====      A   Matrix      ==============
#            % unknowns vector... Y N misclosure ....
        i=0;
        Amat= [[0 for x in xrange(3)] for x in xrange(n)];
        while (i<n):
            d=((Y[i]-NY1)**2+(N[i]-NX1)**2);
            
            Amat[i][0]=-p*((N[i]-NX1)/d);
            Amat[i][1]=p*((Y[i]-NY1)/d);
            Amat[i][2]=-1;
            i=i+1;
        Amat = sp.Matrix(Amat);
#         print M[0,1];
        
#         print M.T; 
#         print M.inv();    
#            
        At=Amat.T;
#         %    display (At);
        AtPA=At*Amat;
#         %    display(AtPA);
#            
#         %    display (Mt);
        Mt=sp.Matrix(Mt);
        print Mt.T;
        print At;
        Atl = [[],[],[]];
        (Atl)=At*(Mt);
#         %    display(Atl);
#            
        print('=======================================================');  
        print('Provisional Coordinates:');
        print ('Y : %0.3f' % NY1old );
        print ('N : %0.3f' % NX1old);
        print('=======================================================');  
        
        Xsol= sp.Matrix.inv(AtPA)*Atl;
        print Xsol;
        print 'Y:                %0.3f\n' % (NY1+Xsol[0]);
        print 'N:                %0.3f\n' % (NX1+Xsol[1]);
        print 'Z:                %0.3f\n' % (Xsol[2]);
        
#         %================================================================
#            %          PRINT TO FILE ========================
#            
#          fileID = fopen('C:\Users\Craig\Desktop\test.csv','a');
#         fprintf(fileID,'%6s \n','Misclosure Vector');
#         fprintf(fileID,',%0.3f \n ',Mt);
#         fclose(fileID);
#         
#         %================================================================
#            
#         display('=======================================================');   
#            fprintf('             N Solution vector:\n');
#            fprintf('dY:   %0.3f \ndX:   %0.3f \nDt in DMS:  ',Xsol(1),Xsol(2));
#            fprintf('%0.0f ',degrees2dms(Xsol(3)/3600));
#            format ;
#            fprintf('\n==============    FINAL COORDINATES     ===============\n\n');
#            
#             fprintf('Y:                %0.3f\n',NY1+Xsol(1));
#            fprintf('N:                %0.3f\n',NX1+Xsol(2));
#           
#            fprintf('orientation corr: %0.3f"\n\n',Xsol(3));
#          fprintf('======================================================='); 
#          
#          
#            
#         %display results........................
#            
#            
#            V=(Amat*Xsol)-Mt.';
#               
#            Posteriori=(V.'*V)/(n-3);
#            
#            Ex=Posteriori*((At*Amat)^-1);
#         %    printmat(Ex, 'Covarience Matrix adjusted Parameters', 'dy dx dz ROW4 ROW5', 'dy dx dz BUZZ FUZZ' )
#            
#            fprintf('=======================================================\n'); 
#            fprintf('std dev of parameters: \nsy %0.3fm \nsx %0.3fm  \nsz %0.1f" \n',sqrt(Ex(1,1)),sqrt(Ex(2,2)),sqrt(Ex(3,3)));
#            
#            %================================================================
#            %          PRINT TO FILE ========================
#            
#         fileID = fopen('C:\Users\Craig\Desktop\test.csv','a');
#         fprintf(fileID,'%6s \n','Solution Vector,');
#         fprintf(fileID,'dY:, %0.3f \ndX:, %0.3f \nDt:, %0.3f"\n',Xsol);
#         fprintf(fileID,'Final Coordinates:\n');
#         fprintf(fileID,'Y,%0.3f \n ',NY1+Xsol(1));
#         fprintf(fileID,'N,%0.3f \n ',NX1+Xsol(2));
#         fprintf(fileID,'z",%0.3f \n ',Xsol(3));
#         fprintf(fileID,'std dev of parameters: \nsy, %0.3fm \nsx, %0.3fm  \nsz, %0.1f" \n\n',sqrt(Ex(1,1)),sqrt(Ex(2,2)),sqrt(Ex(3,3))); 
#         fclose(fileID);
#         
#         %================================================================
#          
#            
#            check=At*V;
#         
#            
#            
#            
#            
#            
#            display('=======================================================');
#            
#         end


    

r = Resection();