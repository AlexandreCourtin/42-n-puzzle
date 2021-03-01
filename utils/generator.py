import random

from matrix_utils import *
from resolver import *

def generate_matrix(length, unsolvable, bcolors):
	print(bcolors.yellow + '===== generate random matrix =====' + bcolors.endc)

	check_length(length)
	start_matrix = make_desired_matrix(length)

	for i in range(10000):
		tmp = neighbors(start_matrix, length)
		random_tmp = None
		while not random_tmp:
			random_tmp = tmp[random.randint(0, 3)]

		for j in range(length):
			start_matrix[j] = random_tmp[j].copy()
	print(bcolors.green + 'generated !' + bcolors.endc)

	if unsolvable:
		if start_matrix[0][0] == 0 or start_matrix[0][1] == 0:
			start_matrix[length - 1][length - 1], start_matrix[length - 1][length - 2] = start_matrix[length - 1][length - 2], start_matrix[length - 1][length - 1]
		else:
			start_matrix[0][0], start_matrix[0][1] = start_matrix[0][1], start_matrix[0][0]
		print(bcolors.red + 'unsolvable !' + bcolors.endc)
	else:
		print(bcolors.green + 'solvable !' + bcolors.endc)
	return start_matrix