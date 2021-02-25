import sys
import argparse
import time

sys.path.append('./utils')

from file_reader import *
from generator import *
from verificator import *
from resolver import *

if __name__ == '__main__':
	start_time = time.time()

	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--file', type=open, help='File containing the puzzle to solve.')
	parser.add_argument('-g', '--generate', type=int, help='Generate matrix of choosen length.')
	parser.add_argument('-u', '--unsolvable', action="store_true", default=False, help='Used with -g: Make the generated matrix unsolvable')
	parser.add_argument('-he', '--heuristic', type=str, default='manhattan', help='Choose heuristic function between: manhattan | manhattan_linear | hamming')

	try:
		args = parser.parse_args()
	except:
		print('args error')
		sys.exit(1)

	length = 0
	start_matrix = []

	if args.file:
		start_matrix = read_file_matrix(args.file)
		length = len(start_matrix[0])
	elif args.generate:
		length = args.generate
		unsolvable = args.unsolvable
		start_matrix = generate_matrix(length, unsolvable)
	else:
		print('args error')
		sys.exit(1)

	desired_matrix = [ [ 0 for i in range(length) ] for j in range(length) ]
	print(Bcolors.YELLOW + '\n===== matrix summary =====' + Bcolors.ENDC)
	print('length is {}'.format(Bcolors.GREEN + str(length) + Bcolors.ENDC))
	print('matrix is:')
	for array in start_matrix:
		print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

	print(Bcolors.YELLOW + '\n===== check if matrix is compatible =====' + Bcolors.ENDC)
	check_matrix(start_matrix, length)

	print(Bcolors.YELLOW + '\n===== making desired matrix =====' + Bcolors.ENDC)
	desired_matrix = make_desired_matrix(length)

	print('desired matrix is:')
	for array in desired_matrix:
		print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

	heuristic_type = 'manhattan'
	if args.heuristic == 'manhattan_linear':
		heuristic_type = 'manhattan_linear'
	elif args.heuristic == 'hamming':
		heuristic_type = 'hamming'

	print(Bcolors.YELLOW + '\n===== resolving n-puzzle with '
		+ Bcolors.GREEN + heuristic_type + Bcolors.YELLOW + ' heuristic function =====' + Bcolors.ENDC)
	resolve_npuzzle(start_matrix, desired_matrix, start_time, length, heuristic_type)