from matrix_utils import *

def heuristic(next_matrix, desired_matrix, length): # OPTI THIS
	heuristic_value = 0
	for i in range(length):
		for j in range(length):
			next_matrix_value = next_matrix[i][j]
			if next_matrix_value != 0:
				for ii in range(length):
					for jj in range(length):
						desiredNumber = desired_matrix[ii][jj]
						if desiredNumber == next_matrix_value:
							heuristic_value += abs(i - ii) + abs(j - jj)

	return heuristic_value

def neighbors(current_matrix, length): # OPTI THIS
	neighbors_list = [[], [], [], []]
	for d in range(4):
		current_direction = switcher_direction.get(d)
		neighbors_list[d] = change_tile(current_matrix, length, current_direction[1], current_direction[0])
	return neighbors_list