import time #for time
import sys #for argv
from Sudoku import Sudoku
from BetterSudoku import BetterSudoku
from BestSudoku import BestSudoku

with open(sys.argv[1]) as myfile:
    for line in myfile:
        #problem=Sudoku(line)
        #problem=BetterSudoku(line)
        problem= BestSudoku(line)
        start_time=time.time()
        if problem.BackTrack():
            print "Solution computed"
            print problem
            print "Number of recursive calls: "+str(problem.count)
            print "In ",time.time() - start_time, "seconds"
        else:
            print "No solution"
            print "In ",time.time() - start_time, "seconds"
            print problem.instance
        print 
