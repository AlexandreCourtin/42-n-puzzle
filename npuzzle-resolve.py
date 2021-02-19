import sys
import argparse

class bcolors:
	RED = '\x1b[1m\x1b[31m'
	YELLOW = '\x1b[1m\x1b[33m'
	GREEN = '\x1b[1m\x1b[32m'
	ENDC = '\x1b[0m'

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
	distanceMatrix = []

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
					distanceMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]
				else:
					if rowCount < length and columnCount < length:
						puzzleMatrix[rowCount][columnCount] = char
						desiredMatrix[rowCount][columnCount] = columnCount + 1 + (rowCount * length)
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
	desiredMatrix[length - 1][length - 1] = 0

	print(bcolors.YELLOW + '===== file summary =====' + bcolors.ENDC)
	print('heuristic function is {}'.format(bcolors.GREEN + args.function + bcolors.ENDC))
	print('length is {}'.format(bcolors.GREEN + str(length) + bcolors.ENDC))
	print('matrix is:')
	for array in puzzleMatrix:
		print(bcolors.GREEN + str(array) + bcolors.ENDC)
	print('desired matrix is:')
	for array in desiredMatrix:
		print(bcolors.GREEN + str(array) + bcolors.ENDC)

	print(bcolors.YELLOW + '\n===== check if only one zero in matrix =====' + bcolors.ENDC)
	zeroNumber = 0
	for array in puzzleMatrix:
		for number in array:
			if int(number) == 0:
				zeroNumber += 1

	if zeroNumber > 1:
		print(bcolors.RED + 'too much zeros' + bcolors.ENDC)
		sys.exit(1)
	elif zeroNumber < 1:
		print(bcolors.RED + 'no zeros' + bcolors.ENDC)
		sys.exit(1)
	else:
		print(bcolors.GREEN + 'all good' + bcolors.ENDC)

	print(bcolors.YELLOW + '\n===== resolving n-puzzle with '
		+ bcolors.GREEN + args.function + bcolors.YELLOW + ' heuristic function =====' + bcolors.ENDC)

	print('matrix is:')
	for array in puzzleMatrix:
		print(bcolors.GREEN + str(array) + bcolors.ENDC)

	print('distance matrix is:')
	for array in distanceMatrix:
		print(bcolors.GREEN + str(array) + bcolors.ENDC)