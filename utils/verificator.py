import sys

from matrix_utils import *

def check_matrix(start_matrix, length):
	for i in range(length * length):
		itsOkay = False
		for row in start_matrix:
			for char in row:
				if int(char) == i:
					if itsOkay:
						print(Bcolors.RED + 'Too many ' + str(i) + ' in matrix' + Bcolors.ENDC)
						sys.exit(1)
					itsOkay = True
		if not itsOkay:
			print(Bcolors.RED + 'There\'s no ' + str(i) + ' in matrix' + Bcolors.ENDC)
			sys.exit(1)
	print(Bcolors.GREEN + 'matrix is well made !' + Bcolors.ENDC)