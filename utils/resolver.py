import sys
import time
import math

from matrix_utils import *

def manhattan_heuristic(next_matrix, desired_matrix, length): # OPTI THIS
	heuristic_value = 0
	for i in range(length):
		for j in range(length):
			next_matrix_value = next_matrix[i][j]
			if next_matrix_value != 0 and next_matrix_value != desired_matrix[i][j]:
				for ii in range(length):
					for jj in range(length):
						desiredNumber = desired_matrix[ii][jj]
						if desiredNumber == next_matrix_value:
							heuristic_value += abs(i - ii) + abs(j - jj)
	return heuristic_value

def manhattan_linear_heuristic(next_matrix, desired_matrix, length): # OPTI THIS
	heuristic_value = manhattan_heuristic(next_matrix, desired_matrix, length)

	def invert_matrix(matrix, length):
		inverted_matrix = [ [ 0 for i in range(length) ] for j in range(length) ]
		for i in range(length):
			for j in range(length):
				inverted_matrix[i][j] = matrix[j][i]
		return inverted_matrix

	invert_current = invert_matrix(next_matrix, length)
	invert_desired = invert_matrix(desired_matrix, length)

	for i in range(length):
		heuristic_value += check_row(next_matrix[i], desired_matrix[i], length)
		heuristic_value += check_row(invert_current[i], invert_desired[i], length)
	return heuristic_value

def hamming_heuristic(next_matrix, desired_matrix, length): # OPTI THIS
	heuristic_value = 0
	for i in range(length):
		for j in range(length):
			if next_matrix[i][j] != desired_matrix[i][j]:
				heuristic_value += 1
	return heuristic_value

def neighbors(current_matrix, length): # OPTI THIS
	neighbors_list = [ [ [ -1 for i in range(length) ] for j in range(length) ] for x in range(4) ]

	changedTile = False
	savedX = [-1, -1, -1, -1]
	savedY = [-1, -1, -1, -1]
	for i in range(length):
		for j in range(length):
			if current_matrix[i][j] == 0 and not changedTile:
				for x in range(4):
					current_direction = switcher_direction.get(x)
					if current_direction[0] != 0 and j + current_direction[0] < length and j + current_direction[0] >= 0:
						neighbors_list[x][i][j] = current_matrix[i][j + current_direction[0]]
						neighbors_list[x][i][j + current_direction[0]] = 0
						savedX[x] = j + current_direction[0]
						savedY[x] = i
					elif current_direction[1] != 0 and i + current_direction[1] < length and i + current_direction[1] >= 0:
						neighbors_list[x][i][j] = current_matrix[i + current_direction[1]][j]
						neighbors_list[x][i + current_direction[1]][j] = 0
						savedX[x] = j
						savedY[x] = i + current_direction[1]
					else:
						neighbors_list[x] = None
				changedTile = True
			else:
				for x in range(4):
					if neighbors_list[x]:
						current_direction = switcher_direction.get(x)
						if i != savedY[x] or j != savedX[x]:
							neighbors_list[x][i][j] = current_matrix[i][j]

	return neighbors_list

def get_heuristic_score(elem):
	return elem[1]

def resolve_npuzzle(start_matrix, desired_matrix, start_time, length, heuristic_type): # OPTI THIS
	matrix_queue = [[start_matrix, 0]]

	selected_opened_state_count = 0
	maximum_state_count = 1
	current_state_count = 1

	came_from = dict()
	cost_so_far = dict()
	came_from[str(start_matrix)] = None
	cost_so_far[str(start_matrix)] = 0

	while len(matrix_queue) > 0:
		current_matrix = matrix_queue.pop(0)[0]
		current_id = str(current_matrix)
		selected_opened_state_count += 1
		current_state_count -= 1

		if current_matrix == desired_matrix:
			print(Bcolors.GREEN + 'win !' + Bcolors.ENDC)
			print_path_from(current_matrix, came_from, desired_matrix)
			print('time = ' + Bcolors.GREEN + str(time.time() - start_time) + Bcolors.ENDC)
			print('selected opened state count = ' + Bcolors.GREEN + str(selected_opened_state_count) + Bcolors.ENDC)
			print('maximum state count in memory = ' + Bcolors.GREEN + str(maximum_state_count) + Bcolors.ENDC)
			sys.exit(0)

		for next_matrix in neighbors(current_matrix, length):
			if next_matrix != None:
				next_id = str(next_matrix)
				new_cost = cost_so_far[current_id] + 1

				# if next_id in cost_so_far and new_cost < cost_so_far[next_id]:
				# 	for matrix in matrix_queue:
				# 		if matrix[0] == next_matrix:
				# 			matrix_queue.remove(matrix)
				# 			break

				if next_id not in cost_so_far or new_cost < cost_so_far[next_id]:
					cost_so_far[next_id] = new_cost
					came_from[next_id] = current_matrix
					current_state_count += 1

					if heuristic_type == 'manhattan_linear':
						next_matrix_heuristic = manhattan_linear_heuristic(next_matrix, desired_matrix, length)
					elif heuristic_type == 'hamming':
						next_matrix_heuristic = hamming_heuristic(next_matrix, desired_matrix, length)
					else:
						next_matrix_heuristic = manhattan_heuristic(next_matrix, desired_matrix, length)

					new_cost_with_heuristic = new_cost + next_matrix_heuristic
					matrix_queue.append([next_matrix, new_cost_with_heuristic])
					matrix_queue.sort(key=get_heuristic_score)

		if maximum_state_count < current_state_count:
			maximum_state_count = current_state_count

	print('This npuzzle is ' + Bcolors.RED + 'unsolvable !' + Bcolors.ENDC)
