import sys
import argparse
from puzzleMatrix import *

# PUT SCORES IN A LIST THEN SORT THIS LIST
# PUT ALREADY CHECKED BOARD AND SCORES IN A SECOND LIST
# KEEP A RECORD OF THE MATRIX YOU CAME FROM SO YOU CAN RETRACE EVERYTHING TO THE BEGINING

class bcolors:
	RED = '\x1b[1m\x1b[31m'
	YELLOW = '\x1b[1m\x1b[33m'
	GREEN = '\x1b[1m\x1b[32m'
	ENDC = '\x1b[0m'

def calculateManhattanScore(paramCalcMatrix):
	distanceMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]
	heuristicValue = 0
	i = 0
	while i < length:
		j = 0
		while j < length:
			puzzleNumber = paramCalcMatrix[i][j]

			if puzzleNumber != 0:
				ii = 0
				while ii < length:
					jj = 0
					while jj < length:
						desiredNumber = desiredMatrix[ii][jj]
						if desiredNumber == puzzleNumber:
							distanceMatrix[i][j] = (max([ii, i]) - min([ii, i])) + (max([jj, j]) - min([jj, j]))
							heuristicValue += distanceMatrix[i][j]
						jj += 1
					ii += 1

			j += 1
		i += 1

	print('matrix is:')
	for array in paramCalcMatrix:
		print(bcolors.GREEN + str(array) + bcolors.ENDC)

	# print('distance matrix is:')
	# for array in distanceMatrix:
	# 	print(bcolors.GREEN + str(array) + bcolors.ENDC)

	print('attemptNumber ' + bcolors.YELLOW + str(attemptNumber) + bcolors.ENDC
		+ ' + heuristicValue ' + bcolors.YELLOW + str(heuristicValue) + bcolors.ENDC
		+ ' = score ' + bcolors.GREEN + str(attemptNumber + heuristicValue) + bcolors.ENDC)

def changeTile(paramMatrix, paramX, paramY):
	copiedMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]
	i = 0
	while i < length:
		copiedMatrix[i] = paramMatrix[i].copy()
		i += 1

	done = False
	i = 0
	while i < length and done == False:
		j = 0
		while j < length and done == False:
			if j + paramX < length and i + paramY < length and j + paramX >= 0 and i + paramY >= 0 and copiedMatrix[i][j] == 0:
				copiedMatrix[i][j] = copiedMatrix[i + paramY][j + paramX]
				copiedMatrix[i + paramY][j + paramX] = 0
				done = True
			j += 1
		i += 1

	return copiedMatrix

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('file', type=open, help='The puzzle to solve.')
	parser.add_argument('-f', '--function', type=str, default='manhattan-distance', help='Choose heuristic function between: manhattan-distance')

	args = parser.parse_args()

	if not args.file:
		print('file error')
		sys.exit(1)

	print(bcolors.YELLOW + '===== reading file =====' + bcolors.ENDC)

	lineCount = 0
	rowCount = 0
	columnCount = 0
	length = 0
	hasLength = False
	puzzleMatrix = []
	desiredMatrix = []

	while True:
		print('line {}:'.format(lineCount))
		line = args.file.readline().split()

		for char in line:
			if char.isnumeric():
				print(char, end = '|')
				if not hasLength:
					length = int(char)
					hasLength = True
					puzzleMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]
					desiredMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]
				else:
					if rowCount < length and columnCount < length:
						puzzleMatrix[rowCount][columnCount] = int(char)
						columnCount += 1
						if columnCount >= length:
							columnCount = 0
							rowCount += 1
			else:
				break
		print('')

		if not line:
			break

		lineCount += 1

	print(bcolors.YELLOW + '\n===== file summary =====' + bcolors.ENDC)
	print('heuristic function is {}'.format(bcolors.GREEN + args.function + bcolors.ENDC))
	print('length is {}'.format(bcolors.GREEN + str(length) + bcolors.ENDC))
	print('matrix is:')
	for array in puzzleMatrix:
		print(bcolors.GREEN + str(array) + bcolors.ENDC)

	print(bcolors.YELLOW + '\n===== check if only one zero in matrix =====' + bcolors.ENDC)
	zeroNumber = 0
	for array in puzzleMatrix:
		for number in array:
			if number == 0:
				zeroNumber += 1

	if zeroNumber > 1:
		print(bcolors.RED + 'too much zeros' + bcolors.ENDC)
		sys.exit(1)
	elif zeroNumber < 1:
		print(bcolors.RED + 'no zeros' + bcolors.ENDC)
		sys.exit(1)
	else:
		print(bcolors.GREEN + 'all good' + bcolors.ENDC)

	print(bcolors.YELLOW + '\n===== making desired matrix =====' + bcolors.ENDC)
	directionX = 1
	directionY = 0
	x = 0
	y = 0
	i = 1
	while i < length * length:
		desiredMatrix[y][x] = i
		i += 1

		if y + directionY >= length or x + directionX >= length or desiredMatrix[y + directionY][x + directionX] != 0:
			if directionX == 1:
				directionX = 0
				directionY = 1
			elif directionY == 1:
				directionX = -1
				directionY = 0
			elif directionX == -1:
				directionX = 0
				directionY = -1
			elif directionY == -1:
				directionX = 1
				directionY = 0

		x += directionX
		y += directionY

	print('desired matrix is:')
	for array in desiredMatrix:
		print(bcolors.GREEN + str(array) + bcolors.ENDC)

	print(bcolors.YELLOW + '\n===== resolving n-puzzle with '
		+ bcolors.GREEN + args.function + bcolors.YELLOW + ' heuristic function =====' + bcolors.ENDC)

	attemptNumber = 0
	print('attempt number: ' + bcolors.GREEN + str(attemptNumber) + bcolors.ENDC)

	calculateManhattanScore(puzzleMatrix)

	newMatrix = changeTile(puzzleMatrix, 1, 0)
	calculateManhattanScore(newMatrix)

	newMatrix = changeTile(puzzleMatrix, -1, 0)
	calculateManhattanScore(newMatrix)

	newMatrix = changeTile(puzzleMatrix, 0, 1)
	calculateManhattanScore(newMatrix)

	newMatrix = changeTile(puzzleMatrix, 0, -1)
	calculateManhattanScore(newMatrix)