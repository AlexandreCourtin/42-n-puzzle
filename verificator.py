import sys
import math

from matrix_utils import *

def check_matrix(matrix, desired_matrix, length, bcolors):
	for i in range(length * length):
		its_okay = False
		for row in matrix:
			for char in row:
				if int(char) == i:
					if its_okay:
						print(bcolors.red + 'Too many ' + str(i) + ' in matrix' + bcolors.endc)
						sys.exit(1)
					its_okay = True

		if not its_okay:
			print(bcolors.red + 'There\'s no ' + str(i) + ' in matrix' + bcolors.endc)
			sys.exit(1)

	def find_zero():
		for i in range(length):
			for j in range(length):
				if matrix[i][j] == 0:
					xi = j
					yi = i
					break
		if length % 2 != 0:
			xf = math.ceil(length / 2)
			yf = math.ceil(length / 2)
		else:
			xf = length / 2 - 1
			yf = length / 2
		d = math.fabs(xf - xi) + math.fabs(yf - yi)
		return d

	def find_inversions():
		matrix_in_row = []
		inversions = 0
		for line in matrix:
			matrix_in_row += line
		desired_in_row = []
		for line in desired_matrix:
			desired_in_row += line
		for i in range(len(matrix_in_row)):
			for j in range(i, len(matrix_in_row)):
				if desired_in_row.index(matrix_in_row[i]) > desired_in_row.index(matrix_in_row[j]):
					matrix_in_row[j], matrix_in_row[i] = matrix_in_row[i], matrix_in_row[j]
					inversions += 1
		return inversions

	is_valid = find_zero() % 2 == find_inversions() % 2

	if is_valid:
		print(bcolors.green + 'matrix is well made !' + bcolors.endc)
	else:
		print('This npuzzle is ' + bcolors.red + 'unsolvable !' + bcolors.endc)
		sys.exit(1)
