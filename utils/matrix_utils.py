from switchers import *

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