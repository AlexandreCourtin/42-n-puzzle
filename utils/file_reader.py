import sys

from matrix_utils import *

def read_file_matrix(file, bcolors):
	has_length = False
	line_count = 0
	row = 0
	column = 0
	start_matrix = []
	length = 0
	count = 0
	line = file.readline()
	while line:
		line = line.split()
		print('line {}:'.format(line_count))

		for char in line:
			print(char, end = '|')
			if char[0] == '#':
				break
			if not line:
				line = file.readline()
				break
			if not has_length:
				if len(line) == 1 and char.isnumeric():
					length = int(char)
					check_length(length, bcolors)
					has_length = True
					start_matrix = [ [ -1 for i in range(length) ] for j in range(length) ]
				else:
					print(bcolors.red + 'Length reading error' + bcolors.endc)
					sys.exit(1)
			else:
				print('count: ' + str(count))
				if count > length * length:
					print(bcolors.red + 'Too many lines' + bcolors.endc)
					sys.exit(1)
				if len(line) > length:
					print(bcolors.red + 'Line too long' + bcolors.endc)
					sys.exit(1)
				if not char.isnumeric():
					print(bcolors.red + 'File format error' + bcolors.endc)
					sys.exit(1)
				if row < length and column < length:
					start_matrix[row][column] = int(char)
					column += 1
					if column >= length:
						column = 0
						row += 1
			count += 1
		line = file.readline()
		print('')

		line_count += 1
	return start_matrix