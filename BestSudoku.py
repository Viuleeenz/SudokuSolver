from Sudoku import Sudoku
import math

class BestSudoku(Sudoku):
	def __init__(self,line):
		Sudoku.__init__(self,line)
		self.conflict=[]
		for x in range(self.n):
			self.conflict.append([])

		for x in range(self.n): # inizializzo matrice dei conflitti
			for y in range(self.n):
				self.conflict[x].append([])

				""" inizializza la sottogriglia dei confitti"""
		for row in range(self.n):
			for col in range(self.n):
				for x in range(self.sn):
					for y in self.instance[(row/self.sn)*self.sn+x][(col/self.sn)*self.sn:(col/self.sn)*self.sn+self.sn]:
						if (y!=0 and y!= self.instance[row][col]):
							self.conflict[row][col].append(y)

				""" inizializza la colonna dei confitti"""
				k = ((row/self.sn)*self.sn)+(row%self.sn)+1
				while((row/self.sn) == (k/self.sn)):
					k=k+1
				if(k<=self.n):
					while( k < self.n):
						if(self.instance[k][col]!=0):
							self.conflict[row][col].append(self.instance[k][col])
						k=k+1

				k = ((row/self.sn)*self.sn)+(row%self.sn)-1
				while ((row/self.sn)==(k/self.sn)):
					k=k-1
				if(k > 0):
					while (k>0):
						if(self.instance[k][col]!=0):
							self.conflict[row][col].append(self.instance[k][col])
						k=k-1
					if(self.instance[k][col]!=0):
						self.conflict[row][col].append(self.instance[k][col])

				"""inizializza la riga dei confitti"""
				k = ((col/self.sn)*self.sn)+(col%self.sn)+1
				while((col/self.sn) == (k/self.sn)):
					k=k+1
				if(k<=self.n):
					while( k < self.n):
						if(self.instance[row][k]!=0):
							self.conflict[row][col].append(self.instance[row][k])
						k=k+1

				k = ((col/self.sn)*self.sn)+(col%self.sn)-1
				while ((col/self.sn)==(k/self.sn)):
					k=k-1
				if(k > 0):
					while (k>0):
						if(self.instance[row][k]!=0):
							self.conflict[row][col].append(self.instance[row][k])
						k=k-1
					if(self.instance[row][k]!=0):
						self.conflict[row][col].append(self.instance[row][k])
					

	def computeNextEmpty(self,current):
		"""
		Calcolare la prossima cella su cui lavorare
		"""
		if current==None:
			currentRow=0
			currentCol=0
		else:
			currentRow=current[0]
			currentCol=current[1]

		flag=0
		maxForb=0
		if(self.partial[currentRow][currentCol]!=0):
			for x in range(self.n):
				for y in range(self.n):
					if self.partial[x][y] == 0:
						if(len(set(self.conflict[x][y])) > maxForb):
							maxRow=x
							maxCol=y
							maxForb = len(set(self.conflict[x][y]))
			if(maxForb == 0 ):
				return None
			else:
				return [maxRow,maxCol]
		else:
			return [currentRow,currentCol]

	def Gamma(self,current):
		"""
		Scegliere il valore da provare nella casella corrente in base ai conflitti rilevati
		"""
		for i in range(1,self.n+1): # +1 because we have to check 0-9 sequence 
			if not i in set(self.conflict[current[0]][current[1]]):
				yield i

	def setNextEmpty(self,current,digit):
		"""
		Aggiornare le liste dei conflitti ad ogni inserimento di un nuovo valore
		"""
		olDigit = self.partial[current[0]][current[1]]
		row = current[0]
		col = current[1]


		if(olDigit != self.emptySymbol):  #remove old symbol
			for x in range(self.sn): #update subMatrix
				for y in range(self.sn):
					if( self.partial[row][col]!=self.partial[(row/self.sn)*self.sn+x][col/self.sn*self.sn+y]):
						self.conflict[row/self.sn*self.sn+x][col/self.sn*self.sn+y].remove(olDigit)

			k = ((row/self.sn)*self.sn)+(row%self.sn)+1 #update col
			while((row/self.sn) == (k/self.sn)):
				k=k+1
			if(k<=self.n):
				while( k < self.n):
					self.conflict[k][col].remove(olDigit)
					k=k+1

			k = ((row/self.sn)*self.sn)+(row%self.sn)-1
			while ((row/self.sn)==(k/self.sn)):
				k=k-1
			if(k > 0):
				while (k>0):
					self.conflict[k][col].remove(olDigit)
					k=k-1	
				self.conflict[k][col].remove(olDigit)


			k = ((col/self.sn)*self.sn)+(col%self.sn)+1 #update row
			while((col/self.sn) == (k/self.sn)):
				k=k+1
			if(k<=self.n):
				while( k < self.n):
					self.conflict[row][k].remove(olDigit)
					k=k+1

			k = ((col/self.sn)*self.sn)+(col%self.sn)-1
			while ((col/self.sn)==(k/self.sn)):
				k=k-1
			if(k > 0):
				while (k>0):
					self.conflict[row][k].remove(olDigit)
					k=k-1
				self.conflict[row][k].remove(olDigit)




		self.partial[row][col]=digit




		if(digit != self.emptySymbol): #append new symbol
			for x in range(self.sn): #update subMatrix
				for y in range(self.sn):
					if( self.partial[row][col]!=self.partial[(row/self.sn)*self.sn+x][col/self.sn*self.sn+y]):
						self.conflict[row/self.sn*self.sn+x][col/self.sn*self.sn+y].append(digit)


			k = ((row/self.sn)*self.sn)+(row%self.sn)+1 #update col
			while((row/self.sn) == (k/self.sn)):
				k=k+1
			if(k<=self.n):
				while( k < self.n):
					self.conflict[k][col].append(digit)
					k=k+1

			k = ((row/self.sn)*self.sn)+(row%self.sn)-1
			while ((row/self.sn)==(k/self.sn)):
				k=k-1
			if(k > 0):
				while (k>0):
					self.conflict[k][col].append(digit)
					k=k-1	
				self.conflict[k][col].append(digit)


			k = ((col/self.sn)*self.sn)+(col%self.sn)+1 #update row
			while((col/self.sn) == (k/self.sn)):
				k=k+1
			if(k<=self.n):
				while( k < self.n):
					self.conflict[row][k].append(digit)
					k=k+1

			k = ((col/self.sn)*self.sn)+(col%self.sn)-1
			while ((col/self.sn)==(k/self.sn)):
				k=k-1
			if(k > 0):
				while (k>0):
					self.conflict[row][k].append(digit)
					k=k-1
				self.conflict[row][k].append(digit)














