import sys
import argparse
from bcolors import *
from puzzleMatrix import *

def getHeur(elem):
	return elem.heuristicValue

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('file', type=open, help='The puzzle to solve.')
	parser.add_argument('-f', '--function', type=str, default='manhattan-distance', help='Choose heuristic function between: manhattan-distance')

	args = parser.parse_args()

	if not args.file:
		print('file error')
		sys.exit(1)

	print(Bcolors.YELLOW + '===== reading file =====' + Bcolors.ENDC)

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

	print(Bcolors.YELLOW + '\n===== file summary =====' + Bcolors.ENDC)
	print('heuristic function is {}'.format(Bcolors.GREEN + args.function + Bcolors.ENDC))
	print('length is {}'.format(Bcolors.GREEN + str(length) + Bcolors.ENDC))
	print('matrix is:')
	for array in puzzleMatrix:
		print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

	print(Bcolors.YELLOW + '\n===== check if only one zero in matrix =====' + Bcolors.ENDC)
	zeroNumber = 0
	for array in puzzleMatrix:
		for number in array:
			if number == 0:
				zeroNumber += 1

	if zeroNumber > 1:
		print(Bcolors.RED + 'too much zeros' + Bcolors.ENDC)
		sys.exit(1)
	elif zeroNumber < 1:
		print(Bcolors.RED + 'no zeros' + Bcolors.ENDC)
		sys.exit(1)
	else:
		print(Bcolors.GREEN + 'all good' + Bcolors.ENDC)

	print(Bcolors.YELLOW + '\n===== making desired matrix =====' + Bcolors.ENDC)
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
		print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

	print(Bcolors.YELLOW + '\n===== resolving n-puzzle with '
		+ Bcolors.GREEN + args.function + Bcolors.YELLOW + ' heuristic function =====' + Bcolors.ENDC)

	attemptNumber = 0
	alreadyCheckedList = []
	toCheckList = []
	print('attempt number: ' + Bcolors.GREEN + str(attemptNumber) + Bcolors.ENDC)

	alreadyCheckedList.append(puzzleMatrix)

	firstMatrix = PuzzleMatrix(length, puzzleMatrix, desiredMatrix)
	firstMatrix.changeTile(1, 0, alreadyCheckedList)
	firstMatrix.calculateManhattanScore(attemptNumber)

	secondMatrix = PuzzleMatrix(length, puzzleMatrix, desiredMatrix)
	secondMatrix.changeTile(-1, 0, alreadyCheckedList)
	secondMatrix.calculateManhattanScore(attemptNumber)

	thirdMatrix = PuzzleMatrix(length, puzzleMatrix, desiredMatrix)
	thirdMatrix.changeTile(0, 1, alreadyCheckedList)
	thirdMatrix.calculateManhattanScore(attemptNumber)

	fourthMatrix = PuzzleMatrix(length, puzzleMatrix, desiredMatrix)
	fourthMatrix.changeTile(0, -1, alreadyCheckedList)
	fourthMatrix.calculateManhattanScore(attemptNumber)

	if firstMatrix.currentMatrix != None:
		toCheckList.append(firstMatrix)
	if secondMatrix.currentMatrix != None:
		toCheckList.append(secondMatrix)
	if thirdMatrix.currentMatrix != None:
		toCheckList.append(thirdMatrix)
	if fourthMatrix.currentMatrix != None:
		toCheckList.append(fourthMatrix)

	print('alreadyCheckedList')
	for cm in alreadyCheckedList:
		print(Bcolors.GREEN + str(cm) + Bcolors.ENDC)

	print('toCheckList')
	for cm in toCheckList:
		print(Bcolors.GREEN + str(cm.heuristicValue) + Bcolors.ENDC)

	toCheckList.sort(key=getHeur)
	print('sorted toCheckList')
	for cm in toCheckList:
		print(Bcolors.GREEN + str(cm.heuristicValue) + Bcolors.ENDC)