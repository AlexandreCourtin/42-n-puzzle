from bcolors import *

class PuzzleMatrix():
	def calculateId(self):
		self.matrixId = ''
		for row in self.currentMatrix:
			for char in row:
				self.matrixId += str(char)

	def changeTile(self, paramX, paramY):
		done = False
		i = 0
		while i < self.length and done == False:
			j = 0
			while j < self.length and done == False:
				if j + paramX < self.length and i + paramY < self.length and j + paramX >= 0 and i + paramY >= 0 and self.currentMatrix[i][j] == 0:
					self.currentMatrix[i][j] = self.currentMatrix[i + paramY][j + paramX]
					self.currentMatrix[i + paramY][j + paramX] = 0
					done = True
				j += 1
			i += 1

		self.precedentId = self.matrixId
		self.calculateId()

	def calculateManhattanScore(self, attemptNumber):
		distanceMatrix = [ [ 0 for i in range(self.length) ] for j in range(self.length) ]
		heuristicValue = 0
		i = 0
		while i < self.length:
			j = 0
			while j < self.length:
				puzzleNumber = self.currentMatrix[i][j]
	
				if puzzleNumber != 0:
					ii = 0
					while ii < self.length:
						jj = 0
						while jj < self.length:
							desiredNumber = self.desiredMatrix[ii][jj]
							if desiredNumber == puzzleNumber:
								distanceMatrix[i][j] = (max([ii, i]) - min([ii, i])) + (max([jj, j]) - min([jj, j]))
								heuristicValue += distanceMatrix[i][j]
							jj += 1
						ii += 1
	
				j += 1
			i += 1
	
		print('matrix is:')
		for array in self.currentMatrix:
			print(Bcolors.GREEN + str(array) + Bcolors.ENDC)
	
		print('distance matrix is:')
		for array in distanceMatrix:
			print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

		print('matrix id is: ' + Bcolors.GREEN + str(self.matrixId) + Bcolors.ENDC)
		print('precendent id is: ' + Bcolors.GREEN + str(self.precedentId) + Bcolors.ENDC)

		print('attemptNumber ' + Bcolors.YELLOW + str(attemptNumber) + Bcolors.ENDC
			+ ' + heuristicValue ' + Bcolors.YELLOW + str(heuristicValue) + Bcolors.ENDC
			+ ' = score ' + Bcolors.GREEN + str(attemptNumber + heuristicValue) + Bcolors.ENDC)
	
	def __init__(self, length, currentMatrix, desiredMatrix):
		self.length = length
		self.currentMatrix = [ [ 0 for i in range(self.length) ] for j in range(self.length) ]
		self.desiredMatrix = [ [ 0 for i in range(self.length) ] for j in range(self.length) ]

		i = 0
		while i < self.length:
			self.currentMatrix[i] = currentMatrix[i].copy()
			self.desiredMatrix[i] = desiredMatrix[i].copy()
			i += 1

		self.precedentId = 'none'
		self.calculateId()