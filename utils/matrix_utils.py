import sys

from switchers import *
from bcolors import *

def check_length(length):
	if length < 3:
		print('size of matrix needs to be greater than 2')
		sys.exit(1)

def change_tile(current_matrix, length, paramX, paramY): # OPTI THIS
	result_matrix = [ [ -1 for i in range(length) ] for j in range(length) ]

	changedTile = False
	savedX = -1
	savedY = -1
	for i in range(length):
		for j in range(length):
			current_matrix_value = current_matrix[i][j]
			if current_matrix_value == 0 and not changedTile:
				if paramX != 0 and j + paramX < length and j + paramX >= 0:
					result_matrix[i][j] = current_matrix[i][j + paramX]
					result_matrix[i][j + paramX] = 0
					savedX = j + paramX
					savedY = i
					changedTile = True
				elif paramY != 0 and i + paramY < length and i + paramY >= 0:
					result_matrix[i][j] = current_matrix[i + paramY][j]
					result_matrix[i + paramY][j] = 0
					savedX = j
					savedY = i + paramY
					changedTile = True
				else:
					return None
			elif i != savedY or j != savedX:
				result_matrix[i][j] = current_matrix_value

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

def print_path_from(finalMatrix, came_from, desired_matrix):
	tab = []
	previous_matrix = came_from[str(finalMatrix)]
	while previous_matrix:
		tab.append(previous_matrix)
		previous_matrix = came_from[str(previous_matrix)]
	for t in tab[::-1]:
		print_matrix(t)
		print(Bcolors.YELLOW + '================' + Bcolors.ENDC)
	print_matrix(desired_matrix)
	print('number of moves = ' + Bcolors.GREEN + str(len(tab))+ Bcolors.ENDC)

def check_row(current_row, desired_row, length):
	result = 0
	checked_numbers = [ 0 for i in range(length) ]
	for i in range(length):
		current_number = current_row[i]
		if current_number not in checked_numbers and current_number != 0:
			checked_numbers[i] = current_number
			for j in range(length):
				desired_number = desired_row[j]
				if current_number == desired_number:
					for ii in reversed(range(length)):
						current_second = current_row[ii]
						if current_second not in checked_numbers and current_second != 0:
							for jj in reversed(range(length)):
								desired_second = desired_row[jj]
								if current_second == desired_second:
									if i < ii and j > jj:
										result += 2
	return result