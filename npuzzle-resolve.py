import sys
import argparse
import queue
import time

sys.path.append('./utils')

from file_reader import *
from generator import *
from verificator import *
from resolver import *

switcher_direction = {
	0: [1, 0],
	1: [-1, 0],
	2: [0, 1],
	3: [0, -1],
}
switcher_inverse = {
	0: 1,
	1: 0,
	2: 3,
	3: 2,
}
switcher_clockwise = {
	'[1, 0]': [0, -1],
	'[-1, 0]': [0, 1],
	'[0, 1]': [1, 0],
	'[0, -1]': [-1, 0],
}

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--file', type=open, help='File containing the puzzle to solve.')
	parser.add_argument('-g', '--generate', type=int, help='Generate matrix of choosen length.')
	parser.add_argument('-u', '--unsolvable', action="store_true", default=False, help='Used with -g: Make the generated matrix unsolvable')
	# parser.add_argument('-f', '--function', type=str, default='manhattan-distance', help='Choose heuristic function between: manhattan-distance')

	args = parser.parse_args()

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

	print(Bcolors.YELLOW + '\n===== check if only one zero in matrix =====' + Bcolors.ENDC)
	check_zeros_in_matrix(start_matrix)

	print(Bcolors.YELLOW + '\n===== making desired matrix =====' + Bcolors.ENDC)
	desired_matrix = make_desired_matrix(length)

	print('desired matrix is:')
	for array in desired_matrix:
		print(Bcolors.GREEN + str(array) + Bcolors.ENDC)

	print(Bcolors.YELLOW + '\n===== resolving n-puzzle with '
		+ Bcolors.GREEN + 'manhattan-distance' + Bcolors.YELLOW + ' heuristic function =====' + Bcolors.ENDC)

	matrix_queue = queue.Queue()
	matrix_queue.put(start_matrix, 0)

	selected_opened_state_count = 0
	maximum_state_count = 1
	current_state_count = 1

	came_from = dict()
	cost_so_far = dict()
	came_from[matrix_to_id(start_matrix)] = None
	cost_so_far[matrix_to_id(start_matrix)] = 0

	start_time = time.time()
	while not matrix_queue.empty():
		current_matrix = matrix_queue.get()
		selected_opened_state_count += 1
		current_state_count -= 1

		if current_matrix == desired_matrix:
			print(Bcolors.GREEN + 'win!' + Bcolors.ENDC)
			print_path_from(current_matrix, came_from, desired_matrix)
			print('time = ' + Bcolors.GREEN + str(time.time() - start_time) + Bcolors.ENDC)
			print('selected opened state count = ' + Bcolors.GREEN + str(selected_opened_state_count) + Bcolors.ENDC)
			print('maximum state count in memory = ' + Bcolors.GREEN + str(maximum_state_count) + Bcolors.ENDC)
			break

		for next_matrix in neighbors(current_matrix, length):
			if next_matrix != None:
				current_id = matrix_to_id(current_matrix)
				next_id = matrix_to_id(next_matrix)
				new_cost = cost_so_far[current_id] + 1
				next_matrix_heuristic = heuristic(next_matrix, desired_matrix, length)
				if next_id not in cost_so_far or new_cost < cost_so_far[next_id]:
					cost_so_far[next_id] = new_cost
					new_cost_with_heuristic = new_cost + next_matrix_heuristic
					matrix_queue.put(next_matrix, -new_cost_with_heuristic)
					came_from[next_id] = current_matrix
					current_state_count += 1
					if maximum_state_count < current_state_count:
						maximum_state_count = current_state_count