'''
Created on Apr 4, 2014

@author: Craig
'''


from sympy.core.function import diff
from sympy.functions.elementary.trigonometric import atan

import sympy as sy


def Linearise(function):
    
    type=function   
    
    x1,x2,y1,y2= sy.symbols('x1,x2,y1,y2')
#     if type=="distance":
#         s = sy.sqrt((x2-x1)**2 + (y2-y1)**2)
#         
#         print diff(x**3 + x, x,2)
    wrt=y2
    a, x = sy.symbols('a, x')

    f=atan((y2-y1)/(x2-x1))
    
    
    test = sum(((wrt-a)**i/sy.factorial(i) * f.diff(wrt, i) for i in range(2)))
    print sy.simplify(test)
    print test
   
    
if __name__ == '__main__':
    Linearise("distance")
    