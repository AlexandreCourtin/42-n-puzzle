import sys
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('file', type=open, help='The puzzle to solve.')
	parser.add_argument('-f', '--function', type=str, default='manhattan-distance', help='Choose heuristic function between: manhattan-distance')

	args = parser.parse_args()

	if not args.file:
		print('file error')
		sys.exit(1)

	print('===== reading file =====')

	count = 0
	length = 0
	hasLength = False
	while True:
		print('line {}:'.format(count))
		line = args.file.readline().split()

		for char in line:
			if char.isnumeric():
				print(char, end = '|')
				if not hasLength:
					length = int(char)
					hasLength = True
			else:
				break
		print('')

		if not line:
			break

		count += 1

	print('===== file summary =====')
	print('length is {}'.format(length))