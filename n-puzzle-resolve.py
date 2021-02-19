import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("file", type=open, help="The puzzle to solve.")

	args = parser.parse_args()

	if args.file:
		print(args.file.read())