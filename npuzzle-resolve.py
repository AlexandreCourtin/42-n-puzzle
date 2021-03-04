import sys
import argparse
import time

from file_reader import *
from generator import *
from verificator import *
from bcolors import *

if __name__ == '__main__':
	start_time = time.time()

	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--file', type=open, help='File containing the puzzle to solve.')
	parser.add_argument('-g', '--generate', type=int, help='Generate matrix of choosen length.')
	parser.add_argument('-u', '--unsolvable', action="store_true", default=False, help='Used with -g: Make the generated matrix unsolvable')
	parser.add_argument('-nc', '--nocolors', action="store_true", default=False, help='Every print will be uncolored.')
	parser.add_argument('-he', '--heuristic', type=str, default='manhattan', help='Choose heuristic function between: manhattan | manhattan_linear | hamming')

	try:
		args = parser.parse_args()
	except:
		sys.exit(1)

	bcolors = None
	if args.nocolors:
		bcolors = Bcolors(True)
	else:
		bcolors = Bcolors(False)

	length = 0
	start_matrix = []

	if args.file:
		print(bcolors.yellow + '===== reading file =====' + bcolors.endc)
		start_matrix = read_file_matrix(args.file, bcolors)
		if start_matrix:
			length = len(start_matrix[0])
		else:
			print(bcolors.red + 'Error reading length in file' + bcolors.endc)
			sys.exit(1)
	elif args.generate:
		length = args.generate
		unsolvable = args.unsolvable
		start_matrix = generate_matrix(length, unsolvable, bcolors)
	else:
		print(bcolors.red + 'args error' + bcolors.endc)
		sys.exit(1)

	desired_matrix = [ [ 0 for i in range(length) ] for j in range(length) ]
	print(bcolors.yellow + '\n===== matrix summary =====' + bcolors.endc)
	print('length is {}'.format(bcolors.green + str(length) + bcolors.endc))
	print('matrix is:')
	for array in start_matrix:
		print(bcolors.green + str(array) + bcolors.endc)

	print(bcolors.yellow + '\n===== making desired matrix =====' + bcolors.endc)
	desired_matrix = make_desired_matrix(length)

	print('desired matrix is:')
	for array in desired_matrix:
		print(bcolors.green + str(array) + bcolors.endc)

	print(bcolors.yellow + '\n===== check if matrix is compatible =====' + bcolors.endc)
	check_matrix(start_matrix, desired_matrix, length, bcolors)

	heuristic_type = 'manhattan'
	if args.heuristic == 'manhattan_linear':
		heuristic_type = 'manhattan_linear'
	elif args.heuristic == 'hamming':
		heuristic_type = 'hamming'

	print(bcolors.yellow + '\n===== resolving n-puzzle with '
		+ bcolors.green + heuristic_type + bcolors.yellow + ' heuristic function =====' + bcolors.endc)
	resolve_npuzzle(start_matrix, desired_matrix, start_time, length, heuristic_type, bcolors)