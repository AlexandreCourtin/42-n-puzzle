import sys
import argparse
import queue
import time

from bcolors import *

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
	startMatrix = []
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
					startMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]
					desiredMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]
				else:
					if rowCount < length and columnCount < length:
						startMatrix[rowCount][columnCount] = int(char)
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
	for array in startMatrix:
		print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

	print(Bcolors.YELLOW + '\n===== check if only one zero in matrix =====' + Bcolors.ENDC)
	zeroNumber = 0
	for array in startMatrix:
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

	def matrix_to_id(matrix):
		result = ''
		for row in matrix:
			for char in row:
				result += str(char)
		return result

	def heuristic(nextMatrix):
		heuristicValue = 0
		i = 0
		while i < length:
			j = 0
			while j < length:
				puzzleNumber = nextMatrix[i][j]

				if puzzleNumber != 0:
					ii = 0
					while ii < length:
						jj = 0
						while jj < length:
							desiredNumber = desiredMatrix[ii][jj]
							if desiredNumber == puzzleNumber:
								heuristicValue += abs(i - ii) + abs(j - jj)
							jj += 1
						ii += 1

				j += 1
			i += 1
		return heuristicValue

	def changeTile(currentMatrix, paramX, paramY):
		changedTileMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]
		i = 0
		while i < length:
			changedTileMatrix[i] = currentMatrix[i].copy()
			i += 1

		isDone = False
		i = 0
		while i < length and not isDone:
			j = 0
			while j < length and not isDone:
				if changedTileMatrix[i][j] == 0:
					if j + paramX < length and i + paramY < length and j + paramX >= 0 and i + paramY >= 0:
						changedTileMatrix[i][j] = changedTileMatrix[i + paramY][j + paramX]
						changedTileMatrix[i + paramY][j + paramX] = 0
					else:
						changedTileMatrix = None
					isDone = True
				j += 1
			i += 1
		return changedTileMatrix

	def neighbors(currentMatrix):
		neighbors_list = [[], [], [], []]
		neighbors_list[0] = changeTile(currentMatrix, 1, 0)
		neighbors_list[1] = changeTile(currentMatrix, -1, 0)
		neighbors_list[2] = changeTile(currentMatrix, 0, 1)
		neighbors_list[3] = changeTile(currentMatrix, 0, -1)
		return neighbors_list
	
	def printMatrix(m):
		for row in m:
			print(row)

	def print_path_from(finalMatrix):
		previousMatrix = came_from[matrix_to_id(finalMatrix)]
		while previousMatrix:
			printMatrix(previousMatrix)
			print(Bcolors.YELLOW + '================' + Bcolors.ENDC)
			previousMatrix = came_from[matrix_to_id(previousMatrix)]

	matrix_queue = queue.Queue()
	matrix_queue.put(startMatrix, 0)

	selected_opened_state_count = 0
	maximum_state_count = 1
	current_state_count = 1

	# id_to_matrix = dict()
	came_from = dict()
	cost_so_far = dict()
	# id_to_matrix[matrix_to_id(startMatrix)] = startMatrix
	came_from[matrix_to_id(startMatrix)] = None
	cost_so_far[matrix_to_id(startMatrix)] = 0

	start_time = time.time()
	while not matrix_queue.empty():
		currentMatrix = matrix_queue.get()
		selected_opened_state_count += 1
		current_state_count -= 1

		if currentMatrix == desiredMatrix:
			print(Bcolors.GREEN + 'win!' + Bcolors.ENDC)
			print_path_from(currentMatrix)
			print('time = ' + Bcolors.GREEN + str(time.time() - start_time) + Bcolors.ENDC)
			print('selected opened state count = ' + Bcolors.GREEN + str(selected_opened_state_count) + Bcolors.ENDC)
			print('maximum state count in memory = ' + Bcolors.GREEN + str(maximum_state_count) + Bcolors.ENDC)
			break

		for nextMatrix in neighbors(currentMatrix):
			if nextMatrix != None:
				currentId = matrix_to_id(currentMatrix)
				nextId = matrix_to_id(nextMatrix)
				new_cost = cost_so_far[currentId] + 1
				next_matrix_heuristic = heuristic(nextMatrix)
				if nextId not in cost_so_far or new_cost < cost_so_far[nextId]:
					cost_so_far[nextId] = new_cost
					new_cost_with_heuristic = new_cost + next_matrix_heuristic
					matrix_queue.put(nextMatrix, -new_cost_with_heuristic)
					came_from[nextId] = currentMatrix
					# id_to_matrix[nextId] = nextMatrix
					current_state_count += 1
					if maximum_state_count < current_state_count:
						maximum_state_count = current_state_count