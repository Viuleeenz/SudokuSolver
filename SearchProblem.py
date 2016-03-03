class SearchProblem:

    def __init__(self,I):
        self.instance=I
        
        
    def ExhaustiveSearch(self):
        for s in self.enumerateSI():
            if self.isAdmissible():
                return s
        return False

        
    def BackTrack(self,Empty=None):
        self.count+=1
        currentEmpty=self.computeNextEmpty(Empty)
        if self.verbose:
            print "Calling BackTrack on"
            print self
            print "with next empty in: "+str(currentEmpty)
        if currentEmpty==None:
            return self.isAdmissible()
        
        for gamma in self.Gamma(currentEmpty):
            self.setNextEmpty(currentEmpty,gamma)
            if self.verbose:
                print "Trying to set "+str(gamma)+" in "+str(currentEmpty)
            if (not self.isnotExtendible()):
                if self.verbose:
                    print "It seems ok\n\n"
                if self.BackTrack(currentEmpty):
                    return True
            if self.verbose:
                print "It is not ok\n\n"
        if self.verbose:
            print "Finished all alternatives in "+str(currentEmpty)
        self.setNextEmpty(currentEmpty,self.emptySymbol)
        return False


    def BranchandBound(self,Empty=None):
        currentEmpty=self.computeNextEmpty(Empty)
        if currentEmpty==None:
            if self.isAdmissible():
                currentcost=self.cost()
                if currentcost<self.cmin:
                    self.cmin=currentcost
                    self.storeCurrentsol()
            return

        for sigma in self.Sigma(currentEmpty):
            self.setNextEmpty(currentEmpty,sigma)
            if (self.LBound()<self.cmin):
                self.BranchandBound(currentEmpty)

        self.setNextEmpty(currentEmpty, self.emptySymbol)


