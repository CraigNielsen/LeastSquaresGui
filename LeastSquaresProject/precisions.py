'''
Created on Apr 4, 2014

@author: Craig
'''
from numpy import size, sqrt

from LeastSquaresProject.points import Points

def obsCount(obs):
        count=0
        for i,j in obs.iteritems():
            for k,t in j.iteritems():
                count+=1
                if t.type=="both":
                    count+=1
        return count

def Precisions(A,Xdict,V,P,unknowns,Obs):
    count=obsCount(Obs)
    posteriori=float((V.T*P*V)/(count-size(unknowns)))
    print posteriori
    covarience_mat= posteriori*(A.T*A)**(-1)
    precisions=Points("Precisions of Unknowns")
    i=0
    for name,value in Xdict.iteritems():
        precisions[name]=sqrt(float(covarience_mat[i,i]))
        i+=1
        
    return precisions