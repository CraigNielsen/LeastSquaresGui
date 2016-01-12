from math import *

# class Angle():
#     def __init__(self, a, unit = "dms"):
#         # store the angle in radians
#         if unit == "dms":
#             self.m_a = self.dms2rad(a)
#  
#         elif unit == "dec":
#             self.m_a = radians(a)
#              
#         elif unit == "rad":
#             self.m_a = a


def dms2rad( dms):
    return dms2dec(dms) * pi / 180.0

def dms2dec( dms):
    if dms >= 0.0:
        ideg = floor(dms)
        fmin = (dms - ideg)* 100.0
        imin = floor(fmin)
        fsec = (fmin - imin) * 100.0
        
        return ideg + imin / 60.0 + fsec / 3600.0
    
    else:
        return -dms2dec(abs(dms))

def dec2dms( dec):
    degr= u'\N{DEGREE SIGN}'
    
    if dec >= 0.0:
        ideg = int(floor(dec))
        fmin = (dec - ideg)* 60.0
        imin = int(floor(fmin))
        fsec = round(((fmin - imin) * 60.0),2)
        
        return str(ideg) + degr + str(imin) + "'"+str(fsec)+"\""
    
    else:
        return dec2dms(dec+360.)
def rad2dms( rad):
    dec=rad*180./pi
    degr= u'\N{DEGREE SIGN}'
    
    if dec >= 0.0:
        ideg = int(floor(dec))
        fmin = (dec - ideg)* 60.0
        imin = int(floor(fmin))
        fsec = round(((fmin - imin) * 60.0),2)
        
        return str(ideg) + degr + str(imin) + "'"+str(fsec)+"\""
    
    else:
        return dec2dms(dec+360.)


# def rad(self):
#     return self.m_a
# 
# def dec(self):
#     return degrees(self.m_a)
# 
# def dms(self):
#     return self.dec2dms(degrees(self.m_a))


# operators
def __add__ (self, a):
    return Angle(self.m_a + a.m_a, "rad")

def __sub__ (self, a):
    return Angle(self.m_a - a.m_a, "rad")    

def __mul__ (self, a):
    return Angle(self.m_a * a, "rad")

def __div__ (self, a):
    return Angle(self.m_a / a, "rad")


# informal representation or string representation
def __str__():
    return 'A: {0:10.5f}'.format(self.dec2dms(degrees(self.m_a)))

def __repr__(self):
    return '{0:10.5f}'.format(self.dec2dms(degrees(self.m_a)))        

#         
# myang1 = Angle(23.3645)
# print myang1.m_a
# 
# myang2 = Angle(-23.3645)
# print myang2.m_a
# 
# 
# print myang1.rad()
# print myang1.dec()
# print myang1.dms()
