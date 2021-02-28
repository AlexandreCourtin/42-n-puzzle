import sys

from matrix_utils import *

def check_matrix(matrix, desired_matrix, length):
	for i in range(length * length):
		its_okay = False
		for row in matrix:
			for char in row:
				if int(char) == i:
					if its_okay:
						print(Bcolors.RED + 'Too many ' + str(i) + ' in matrix' + Bcolors.ENDC)
						sys.exit(1)
					its_okay = True

		if not its_okay:
			print(Bcolors.RED + 'There\'s no ' + str(i) + ' in matrix' + Bcolors.ENDC)
			sys.exit(1)

	matrix_in_row = []
	desired_in_row = []
	for i in range(length):
		for j in range(length):
			matrix_in_row.append(matrix[i][j])
			desired_in_row.append(desired_matrix[i][j])

	def convert_desired(desired_in_row, length):
		result = [ -1 for i in range(length * length) ]
		for i in range(length * length):
			result[i] = i + 1
		return result

	def convert_row(matrix_in_row, desired_in_row, length):
		result = [ -1 for i in range(length * length) ]
		converted = convert_desired(desired_in_row, length)
		for i in range(length * length):
			for j in range(length * length):
				if matrix_in_row[i] == desired_in_row[j]:
					result[i] = converted[j]
		return result

	print('matrix_in_row')
	print(matrix_in_row)
	print('desired_in_row')
	print(desired_in_row)
	print('convert_desired(length)')
	print(convert_desired(desired_in_row, length))
	print('convert_row(matrix_in_row, desired_in_row, length)')
	print(convert_row(matrix_in_row, desired_in_row, length))

	converted = convert_row(matrix_in_row, desired_in_row, length)
	inversions = 0
	for i, tile in enumerate(converted):
		for _, after in enumerate(converted[i + 1:]):
			if tile > after and tile != 0 and after != 0:
				inversions += 1

	print('inversions: ' + str(inversions))

	is_valid = False
	if length % 2 != 0:
		if inversions % 2 == 0:
			is_valid = True
	else:
		i = 0
		zero_row = -1
		while i < length and zero_row == -1:
			j = 0
			while j < length and zero_row == -1:
				if matrix[i][j] == 0:
					zero_row = i
				j += 1
			i += 1

		if inversions % 2 == 0 and (length - (zero_row + 1)) % 2 != 0:
			is_valid = True
		elif inversions % 2 != 0 and (length - (zero_row + 1)) % 2 == 0:
			is_valid = True

	if is_valid:
		print(Bcolors.GREEN + 'matrix is well made !' + Bcolors.ENDC)
	else:
		print('This npuzzle is ' + Bcolors.RED + 'unsolvable !' + Bcolors.ENDC)
		sys.exit(1)
