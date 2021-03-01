class Bcolors:
	def __init__(self, uncolored):
		self.red = ''
		self.yellow = ''
		self.green = ''
		self.endc = ''

		if not uncolored:
			self.red = '\x1b[1m\x1b[31m'
			self.yellow = '\x1b[1m\x1b[33m'
			self.green = '\x1b[1m\x1b[32m'
			self.endc = '\x1b[0m'