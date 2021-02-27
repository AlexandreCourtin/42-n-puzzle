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

	inversions = 0
	checked_numbers = [ 0 for i in range(length * length) ]
	for i in range(length * length):
		current_number = matrix_in_row[i]
		if current_number not in checked_numbers and current_number != 0:
			checked_numbers[i] = current_number
			for j in range(length * length):
				desired_number = desired_in_row[j]
				if current_number == desired_number:
					for ii in reversed(range(length * length)):
						current_second = matrix_in_row[ii]
						if current_second not in checked_numbers and current_second != 0:
							for jj in reversed(range(length * length)):
								desired_second = desired_in_row[jj]
								if current_second == desired_second:
									if i < ii and j > jj:
										inversions += 1

	print(inversions)
	print(matrix_in_row)
	print(desired_in_row)

	if not (length % 2 != 0 and inversions % 2 == 0):
		print('This npuzzle is ' + Bcolors.RED + 'unsolvable !' + Bcolors.ENDC)
		sys.exit(1)

	print(Bcolors.GREEN + 'matrix is well made !' + Bcolors.ENDC)