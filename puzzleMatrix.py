class PuzzleMatrix:
    def __init__(self, length):
        self.length = length
        self.currentMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]
        self.desiredMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]
        self.distanceMatrix = [ [ 0 for i in range(length) ] for j in range(length) ]