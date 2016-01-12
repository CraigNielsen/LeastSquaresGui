'''
Created on Mar 17, 2014

@author: 01410541
'''

from numpy import float64, pi
import xlrd

from LeastSquaresProject.display import dec2dms
from point import Point



class Points(dict):
    '''
    classdocs
    '''
    def __init__(self,name="unnamed"):
        if name=="unnamed":self.name="unnamed"
        else:
            self.name=name
        
    def read(self, filename):
        c0=0#Code
        c1=1#Station    #COLUMNS FOR FILE INPUT: first column in excell is c0
        c2=2#Target
        c3=3#direction
        c4=4#distance
        if filename[-3:]=="csv":
            f = open(filename, 'r')    
            f.readline()
            for line in f:
                sp = line.split(',')
                name = sp[c0]
                x = float64(sp[c2])
                y = float64(sp[c1])
                h = float64(sp[c3])
                if float64(sp[5])==1.:
                    k=True
                else :
                    k=False
                self[name] = Point(x, y, h, k,name)
            return
        elif filename[-4:]=="xlsx":
            workbook = xlrd.open_workbook(str(filename))
            worksheet = workbook.sheet_by_name('Sheet1')
            num_rows = worksheet.nrows - 1
            num_cells = worksheet.ncols - 1
            curr_row = -1
            f=[]
            while curr_row < num_rows:
                curr_row += 1
                row = worksheet.row(curr_row)
                print 'Row Count:', curr_row+1
                curr_cell = -1
                sp=[]
                while curr_cell < num_cells:
                    curr_cell += 1
                    # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                    cell_type = worksheet.cell_type(curr_row, curr_cell)
                    cell_value = worksheet.cell_value(curr_row, curr_cell)
                    sp.append(cell_value) 
                f.append(sp)
            for line in f:
                
                name = line[0]
                x = float64(line[2])
                y = float64(line[1])
                h = float64(line[3])
                if float64(line[5])==1.:
                    k=True
                else :
                    k=False
                self[name] = Point(x, y, h, k,name)
            return
                


    def add(self,name,x,y,h,k):
        if not name in self:
#             print "New "+self.name+" Point: "+ str(name)
            self[name] = Point(x, y, h,k,name)
        elif name in self:
            print "point: '" + str(name) + "' already exists... Calculating mean"
            self[name].x = (self[name].x + x)/2
            self[name].y = (self[name].y + y)/2
            self[name].h = (self[name].h + h)/2
    
    def replace (self,name,x,y,h,k):
        if not name in self:
            print "Cannot Replace, It doesn't Exist"
            return
        print "replacing: " + name
        self[name].x = x
        self[name].y = y
        self[name].h = h
        self[name].k = k
    def Totalcopy(self):
        copy=Points(self.name)
        for x,j in self.iteritems():
            copy[x]=Point(j.x, j.y, j.h, j.known, j.name)
        return copy
            
#     def ChangeVariable(self,name,variable,x,y,h):
#         if not name in self:
#             print "New Point: "+ str(name)
#             self[name] = Point(x, y, h,k,name)
#         if variable=="x":
#             self[name].ChangeVariable("x",x)
#         if variable=="y":
#             self[name].ChangeVariable("y",y)
#         if variable=="h":
#             self[name].ChangeVariable("h",h)
    def __str__(self):
            print "________"+self.name+"___________________________________\n"
            for x,y in self.iteritems():
                print "___"+x+":___"
                if isinstance(y, float):
                    print round( y,4)
                else:
                    print y           
                          
            print"________________________________________________"
            return " "            
        
        
        
