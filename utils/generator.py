import random

from matrix_utils import *
from bcolors import *

def generate_matrix(length, unsolvable):
	print(Bcolors.YELLOW + '===== generate random matrix =====' + Bcolors.ENDC)

	check_length(length)

	start_matrix = make_desired_matrix(length)

	precedent_direction = -1
	for i in range(length * length * length * length):
		tmp = None
		while not tmp:
			random_direction = switcher_inverse.get(precedent_direction)
			while random_direction == switcher_inverse.get(precedent_direction):
				random_direction = random.randint(0, 3)
			direction = switcher_direction.get(random_direction)
			precedent_direction = random_direction
			tmp = change_tile(start_matrix, length, direction[0], direction[1])
		start_matrix = change_tile(start_matrix, length, direction[0], direction[1])
	print(Bcolors.GREEN + 'generated !' + Bcolors.ENDC)

	if unsolvable:
		if start_matrix[0][0] == 0 or start_matrix[0][1] == 0:
			start_matrix[length - 1][length - 1], start_matrix[length - 1][length - 2] = start_matrix[length - 1][length - 2], start_matrix[length - 1][length - 1]
		else:
			start_matrix[0][0], start_matrix[0][1] = start_matrix[0][1], start_matrix[0][0]
		print(Bcolors.RED + 'unsolvable !' + Bcolors.ENDC)
	else:
		print(Bcolors.GREEN + 'solvable !' + Bcolors.ENDC)
	return start_matrix