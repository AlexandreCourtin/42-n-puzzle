from switchers import *
from bcolors import *

def check_length(length):
	if length < 2:
		print('size of matrix needs to be greater than 1')
		sys.exit(1)

def change_tile(current_matrix, length, paramX, paramY):
	result_matrix = [ [ 0 for i in range(length) ] for j in range(length) ]
	for i in range(length):
		result_matrix[i] = current_matrix[i].copy()

	for i in range(length):
		for j in range(length):
			if result_matrix[i][j] == 0:
				if j + paramX < length and i + paramY < length and j + paramX >= 0 and i + paramY >= 0:
					result_matrix[i][j] = result_matrix[i + paramY][j + paramX]
					result_matrix[i + paramY][j + paramX] = 0
				else:
					result_matrix = None
				return result_matrix
	return result_matrix

def make_desired_matrix(length):
	new_desired_matrix = [ [ 0 for i in range(length) ] for j in range(length) ]
	d = switcher_direction.get(2)
	x = 0
	y = 0
	for i in range((length * length) - 1):
		new_desired_matrix[y][x] = i + 1

		if y + d[0] >= length or x + d[1] >= length or new_desired_matrix[y + d[0]][x + d[1]]:
			d = switcher_clockwise.get(str(d))

		x += d[1]
		y += d[0]
	return new_desired_matrix

def print_matrix(m):
	for row in m:
		print(row)

def matrix_to_id(matrix):
	result = ''
	for row in matrix:
		for char in row:
			result += str(char)
	return result

def print_path_from(finalMatrix, came_from, desired_matrix):
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