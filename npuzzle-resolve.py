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

	line_count = 0
	row = 0
	column = 0
	length = 0
	has_length = False
	start_matrix = []
	desired_matrix = []

	while True:
		print('line {}:'.format(line_count))
		line = args.file.readline().split()

		for char in line:
			if char.isnumeric():
				print(char, end = '|')
				if not has_length:
					length = int(char)
					has_length = True
					start_matrix = [ [ 0 for i in range(length) ] for j in range(length) ]
					desired_matrix = [ [ 0 for i in range(length) ] for j in range(length) ]
				else:
					if row < length and column < length:
						start_matrix[row][column] = int(char)
						column += 1
						if column >= length:
							column = 0
							row += 1
			else:
				break
		print('')

		if not line:
			break

		line_count += 1

	print(Bcolors.YELLOW + '\n===== file summary =====' + Bcolors.ENDC)
	print('heuristic function is {}'.format(Bcolors.GREEN + args.function + Bcolors.ENDC))
	print('length is {}'.format(Bcolors.GREEN + str(length) + Bcolors.ENDC))
	print('matrix is:')
	for array in start_matrix:
		print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

	print(Bcolors.YELLOW + '\n===== check if only one zero in matrix =====' + Bcolors.ENDC)
	zero_number = 0
	for array in start_matrix:
		for number in array:
			if number == 0:
				zero_number += 1

	if zero_number > 1:
		print(Bcolors.RED + 'too much zeros' + Bcolors.ENDC)
		sys.exit(1)
	elif zero_number < 1:
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
		desired_matrix[y][x] = i
		i += 1

		if y + directionY >= length or x + directionX >= length or desired_matrix[y + directionY][x + directionX] != 0:
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
	for array in desired_matrix:
		print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

	print(Bcolors.YELLOW + '\n===== resolving n-puzzle with '
		+ Bcolors.GREEN + args.function + Bcolors.YELLOW + ' heuristic function =====' + Bcolors.ENDC)

	def matrix_to_id(matrix):
		result = ''
		for row in matrix:
			for char in row:
				result += str(char)
		return result

	def heuristic(next_matrix):
		heuristic_value = 0
		i = 0
		while i < length:
			j = 0
			while j < length:
				next_matrix_value = next_matrix[i][j]
				if next_matrix_value != 0:
					ii = 0
					while ii < length:
						jj = 0
						while jj < length:
							desiredNumber = desired_matrix[ii][jj]
							if desiredNumber == next_matrix_value:
								heuristic_value += abs(i - ii) + abs(j - jj)
							jj += 1
						ii += 1

				j += 1
			i += 1
		return heuristic_value

	def change_tile(current_matrix, paramX, paramY):
		result_matrix = [ [ 0 for i in range(length) ] for j in range(length) ]
		i = 0
		while i < length:
			result_matrix[i] = current_matrix[i].copy()
			i += 1

		done = False
		i = 0
		while i < length and not done:
			j = 0
			while j < length and not done:
				if result_matrix[i][j] == 0:
					if j + paramX < length and i + paramY < length and j + paramX >= 0 and i + paramY >= 0:
						result_matrix[i][j] = result_matrix[i + paramY][j + paramX]
						result_matrix[i + paramY][j + paramX] = 0
					else:
						result_matrix = None
					done = True
				j += 1
			i += 1
		return result_matrix

	def neighbors(current_matrix):
		neighbors_list = [[], [], [], []]
		neighbors_list[0] = change_tile(current_matrix, 1, 0)
		neighbors_list[1] = change_tile(current_matrix, -1, 0)
		neighbors_list[2] = change_tile(current_matrix, 0, 1)
		neighbors_list[3] = change_tile(current_matrix, 0, -1)
		return neighbors_list
	
	def print_matrix(m):
		for row in m:
			print(row)

	def print_path_from(finalMatrix):
		tab = []
		previous_matrix = came_from[matrix_to_id(finalMatrix)]
		while previous_matrix:
			tab.append(previous_matrix)
			previous_matrix = came_from[matrix_to_id(previous_matrix)]
		tab = tab[::-1]
		for t in tab:
			print_matrix(t)
			print(Bcolors.YELLOW + '================' + Bcolors.ENDC)
		print_matrix(desired_matrix)

	matrix_queue = queue.Queue()
	matrix_queue.put(start_matrix, 0)

	selected_opened_state_count = 0
	maximum_state_count = 1
	current_state_count = 1

	# id_to_matrix = dict()
	came_from = dict()
	cost_so_far = dict()
	# id_to_matrix[matrix_to_id(start_matrix)] = start_matrix
	came_from[matrix_to_id(start_matrix)] = None
	cost_so_far[matrix_to_id(start_matrix)] = 0

	start_time = time.time()
	while not matrix_queue.empty():
		current_matrix = matrix_queue.get()
		selected_opened_state_count += 1
		current_state_count -= 1

		if current_matrix == desired_matrix:
			print(Bcolors.GREEN + 'win!' + Bcolors.ENDC)
			print_path_from(current_matrix)
			print('time = ' + Bcolors.GREEN + str(time.time() - start_time) + Bcolors.ENDC)
			print('selected opened state count = ' + Bcolors.GREEN + str(selected_opened_state_count) + Bcolors.ENDC)
			print('maximum state count in memory = ' + Bcolors.GREEN + str(maximum_state_count) + Bcolors.ENDC)
			break

		for next_matrix in neighbors(current_matrix):
			if next_matrix != None:
				current_id = matrix_to_id(current_matrix)
				next_id = matrix_to_id(next_matrix)
				new_cost = cost_so_far[current_id] + 1
				next_matrix_heuristic = heuristic(next_matrix)
				if next_id not in cost_so_far or new_cost < cost_so_far[next_id]:
					cost_so_far[next_id] = new_cost
					new_cost_with_heuristic = new_cost + next_matrix_heuristic
					matrix_queue.put(next_matrix, -new_cost_with_heuristic)
					came_from[next_id] = current_matrix
					# id_to_matrix[next_id] = next_matrix
					current_state_count += 1
					if maximum_state_count < current_state_count:
						maximum_state_count = current_state_count