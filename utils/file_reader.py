from matrix_utils import *
from bcolors import *

def read_file_matrix(file):
	print(Bcolors.YELLOW + '===== reading file =====' + Bcolors.ENDC)

	has_length = False
	line_count = 0
	row = 0
	column = 0
	start_matrix = []
	length = 0
	while True:
		print('line {}:'.format(line_count))
		line = file.readline().split()

		for char in line:
			if char.isnumeric():
				print(char, end = '|')
				if not has_length:
					length = int(char)
					check_length(length)
					has_length = True
					start_matrix = [ [ 0 for i in range(length) ] for j in range(length) ]
				else:
					if row < length and column < length:
						start_matrix[row][column] = int(char)
						column += 1
						if column >= length:
							column = 0
							row += 1
			else:
				break
		print('')

		if not line:
			break

		line_count += 1
	return start_matrix