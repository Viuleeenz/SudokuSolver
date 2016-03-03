from SearchProblem import SearchProblem
import math

class Sudoku(SearchProblem):
    """Basic sudoku class"""

    emptySymbol=0   #empty cell

    def __init__(self,line,verbose=False):
        self.verbose=verbose
        self.count=0
        self.n=int(math.sqrt(len(line)))  #side of the grid
        self.sn=int(math.sqrt(self.n))    #side of a sub-grid
        self.instance=[]   #instance
        self.partial=[]   #working copy of the instance
        line=line.replace('\n','')  #trailing \n
        col=0
        ROW=[]
        for symbol in line:
            ROW.append(int(symbol))
            col=(col+1)%self.n
            if col==0:  #completed row
                self.instance.append(ROW)
                self.partial.append(list(ROW))
                ROW=[]
        
    def enumerateSI(self,row=0,col=0):
        if (row==self.n):
            yield self.partial
        else:
            nextrow=row;
            nextcol=col+1;
            if (nextcol==self.n):
                nextcol=0;
                nextrow=nextrow+1
            for i in range(1,self.n+1):
                self.partial[row][col]=i;
                for r in self.enumerateSI(nextrow,nextcol):
                    yield r
        
    def isAdmissible(self,solution=None):  #check if solution is admissible for self.instance
        if solution==None:
            solution=self.partial

        if self.verbose:
            print "Calling isAdmissible on"
            print self
        if self.verbose:
            print "Checking solution is compatible with instance" 
        for row in range(self.n):
            for col in range(self.n):
                if ((self.instance[row][col]!=0) and (self.instance[row][col]!=solution[row][col])):
                    if self.verbose:
                        print "Fixed cell changed "+str(row)+str(col)
                    return False
        if self.verbose:
            print "Solution compatible with instance" 

        if self.verbose:
            print "Looking for repetitions in rows"
        for row in range(self.n):
            seenVals=set()
            for col in range(self.n):
                val=solution[row][col]
                if (val!=0) and (val in seenVals):
                    if self.verbose:
                        print "Repetition in row "+str(row)+str(col)
                    return False
                seenVals.add(val)
        if self.verbose:
            print "No repetition found in rows"

        if self.verbose:
            print "Looking for repetitions in cols"
        for col in range(self.n):
            seenVals=set()
            for row in range(self.n):
                val=solution[row][col]
                if (val!=0) and (val in seenVals):
                    if self.verbose:
                        print "Repetition in col "+str(row)+str(col)
                    return False
                seenVals.add(val)
        if self.verbose:
            print "No repetition found in cols"

        if self.verbose:
            print "Looking for repetitions in sub-grids"
        sn=int(math.sqrt(self.n))
        for cornerRow in range(0,self.n,sn):
            for cornerCol in range(0,self.n,sn):
                seenVals=set()
                for row in range(sn):
                    for col in range(sn):
                        val=solution[cornerRow+row][cornerCol+col]
                        if (val!=0 and val in seenVals):
                            if self.verbose:
                                 print "Repetition in sub-grid "+str(cornerRow+row)+str(cornerCol+col)
                            return False
                        seenVals.add(val)
        if self.verbose:
            print "No repetition found in subgrids"
                
        if self.verbose:
            print "It is admissible"

        return True
            

    def setNextEmpty(self,current,digit):
        self.partial[current[0]][current[1]]=digit

    def computeNextEmpty(self,current):
        if current==None:
            currentRow=0
            currentCol=0
        else:
            currentRow=current[0]
            currentCol=current[1]

        if(self.partial[currentRow][currentCol]!=0):
            for col in range(currentCol+1,self.n):
                if self.partial[currentRow][col]==0:
                    return [currentRow,col]
            for row in range(currentRow+1,self.n):
                for col in range(self.n):
                    if self.partial[row][col]==0:
                        return [row,col]
            return None
        else:
            return [currentRow,currentCol]
        

    def isnotExtendible(self):
        return not self.isAdmissible()

    def Gamma(self,current):
        for i in range(1,self.n+1):
            yield i
        

    def __str__(self):
        s=""
        for row in range(self.n):
            for col in range(self.n):
                if self.instance[row][col]==0:
                    s=s+' . '
                else:
                    s=s+" "+str(self.instance[row][col])+" "
            s=s+"    "
            for col in range(self.n):
                if self.partial[row][col]==0:
                    s=s+' . '
                else:
                    s=s+" "+str(self.partial[row][col])+" "
            s=s+"\n"
        return s