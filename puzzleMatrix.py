from bcolors import *

class PuzzleMatrix():
	def checkIfDesired(self):
		return self.currentMatrix == self.desiredMatrix

	def changeTile(self, paramX, paramY, alreadyCheckedList, toCheckList):
		done = False
		i = 0
		while i < self.length and done == False:
			j = 0
			while j < self.length and done == False:
				if self.currentMatrix[i][j] == 0:
					if j + paramX < self.length and i + paramY < self.length and j + paramX >= 0 and i + paramY >= 0:
						self.currentMatrix[i][j] = self.currentMatrix[i + paramY][j + paramX]
						self.currentMatrix[i + paramY][j + paramX] = 0
					else:
						self.currentMatrix = None
					done = True
				j += 1
			i += 1

		# CHECK IF IS IN LIST
		for cl in alreadyCheckedList:
			if self.currentMatrix == cl:
				self.currentMatrix = None
		for cl in toCheckList:
			if self.currentMatrix == cl:
				self.currentMatrix = None

	def calculateManhattanScore(self):
		if self.currentMatrix == None:
			return

		self.heuristicValue = 0
		self.scoreValue = 0

		distanceMatrix = [ [ 0 for i in range(self.length) ] for j in range(self.length) ]
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
								distanceMatrix[i][j] = abs(i - ii) + abs(j - jj)
								self.heuristicValue += distanceMatrix[i][j]
							jj += 1
						ii += 1
	
				j += 1
			i += 1
		self.scoreValue = self.heuristicValue + self.attemptNumber

		# print('matrix is:')
		# for array in self.currentMatrix:
		# 	print(Bcolors.GREEN + str(array) + Bcolors.ENDC)
	
		# print('distance matrix is:')
		# for array in distanceMatrix:
		# 	print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

		# print('precedent matrix is:')
		# for array in self.precedentMatrix:
		# 	print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

		print('attemptNumber ' + Bcolors.YELLOW + str(self.attemptNumber) + Bcolors.ENDC
			+ ' + heuristicValue ' + Bcolors.YELLOW + str(self.heuristicValue) + Bcolors.ENDC
			+ ' = score ' + Bcolors.GREEN + str(self.scoreValue) + Bcolors.ENDC)

	def __init__(self, length, attemptNumber, currentMatrix, desiredMatrix):
		self.length = length
		self.attemptNumber = attemptNumber
		self.currentMatrix = [ [ 0 for i in range(self.length) ] for j in range(self.length) ]
		self.desiredMatrix = [ [ 0 for i in range(self.length) ] for j in range(self.length) ]
		self.precedentMatrix = [ [ 0 for i in range(self.length) ] for j in range(self.length) ]
		self.heuristicValue = -1
		self.scoreValue = -1

		i = 0
		while i < self.length:
			self.currentMatrix[i] = currentMatrix[i].copy()
			self.precedentMatrix[i] = currentMatrix[i].copy()
			self.desiredMatrix[i] = desiredMatrix[i].copy()
			i += 1