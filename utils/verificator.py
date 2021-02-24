from matrix_utils import *

def check_zeros_in_matrix(start_matrix):
	zero_number = 0
	for array in start_matrix:
		for number in array:
			if number == 0:
				zero_number += 1

	if zero_number > 1:
		print(Bcolors.RED + 'too much zeros' + Bcolors.ENDC)
		sys.exit(1)
	elif zero_number < 1:
		print(Bcolors.RED + 'no zeros' + Bcolors.ENDC)
		sys.exit(1)
	else:
		print(Bcolors.GREEN + 'all good' + Bcolors.ENDC)