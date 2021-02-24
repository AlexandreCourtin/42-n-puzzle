import sys
import queue
import time

from matrix_utils import *

def heuristic(next_matrix, desired_matrix, length): # OPTI THIS
	heuristic_value = 0
	for i in range(length):
		for j in range(length):
			next_matrix_value = next_matrix[i][j]
			if next_matrix_value != 0:
				for ii in range(length):
					for jj in range(length):
						desiredNumber = desired_matrix[ii][jj]
						if desiredNumber == next_matrix_value:
							heuristic_value += abs(i - ii) + abs(j - jj)

	return heuristic_value

def neighbors(current_matrix, length): # OPTI THIS
	neighbors_list = [[], [], [], []]
	for d in range(4):
		current_direction = switcher_direction.get(d)
		neighbors_list[d] = change_tile(current_matrix, length, current_direction[1], current_direction[0])
	return neighbors_list

def resolve_npuzzle(start_matrix, desired_matrix, start_time, length):
	matrix_queue = queue.Queue()
	matrix_queue.put(start_matrix, 0)

	selected_opened_state_count = 0
	maximum_state_count = 1
	current_state_count = 1

	came_from = dict()
	cost_so_far = dict()
	came_from[matrix_to_id(start_matrix)] = None
	cost_so_far[matrix_to_id(start_matrix)] = 0

	while not matrix_queue.empty():
		current_matrix = matrix_queue.get()
		selected_opened_state_count += 1
		current_state_count -= 1

		if current_matrix == desired_matrix:
			print(Bcolors.GREEN + 'win !' + Bcolors.ENDC)
			print_path_from(current_matrix, came_from, desired_matrix)
			print('time = ' + Bcolors.GREEN + str(time.time() - start_time) + Bcolors.ENDC)
			print('selected opened state count = ' + Bcolors.GREEN + str(selected_opened_state_count) + Bcolors.ENDC)
			print('maximum state count in memory = ' + Bcolors.GREEN + str(maximum_state_count) + Bcolors.ENDC)
			sys.exit(0)

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
	print('This npuzzle is ' + Bcolors.RED + 'unsolvable !' + Bcolors.ENDC)