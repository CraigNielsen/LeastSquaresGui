'''
Created on Apr 2, 2014

@author: Craig
'''
from LeastSquaresProject.display import dec2dms
from LeastSquaresProject.leastSqr import LeastSqr
from LeastSquaresProject.leastSqrRead import LeastSqrRead
from LeastSquaresProject.observations import ObsSplit
from LeastSquaresProject.precisions import Precisions


if __name__ == '__main__':
    Leas= LeastSqr()
    A,Xdict,provis,OBS,control,unknowns,V,P=Leas.Read('control.csv','observations.csv')
    print"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print OBS
    provis=Leas.adjustProvisional(Xdict,provis, OBS, unknowns)
    print OBS
    A,Xdict,provis,OBS,control,unknowns,V,P=Leas.Iterate(provis, OBS, control, unknowns)
    print OBS
    print "________Calculating>>>>>>>>>>>>>>>>>>>>>>>....................."
    for i in range (500):
        provis=Leas.adjustProvisional(Xdict,provis, OBS, unknowns)
        A,Xdict,provis,OBS,control,unknowns,V,P=Leas.Iterate(provis, OBS, control, unknowns)
    print "________After 500 iterations:"   
    print OBS 
    print Xdict
    print provis
    p1=Precisions(A, Xdict, V, P, unknowns, OBS)
    print A.T*V
    print V.T*V
#     print p1
#     print "--______________   FINISHED   __________________--"
# #     print provis
# # #     print Xdict
# # #     print p1
# #    
# # #     p=Precisions(A, Xdict, V, P, unknowns, OBS)
# # #     print p
# # #     print p1
# # #     provis,OBS=Leas.adjustProvisional(Xdict,provis, OBS, unknowns)
# #     