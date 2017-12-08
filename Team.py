class Team():
	def __init__(self, id):
		self.id = id
		self.snakes = []

	# Equality check
	def __eq__( self, other ):
		if other == None:
			return False
		if not self.id == other.id: return False
		if not len(self.snakes) == len(other.snakes): return False
		for snake in xrange(len(self.snakes)):
			if not self.snakes[snake] == other.snakes[snake]: return False
		return True

	# Make class hashable for q learning state value pairs
	def __hash__(self):
		return hash(hash(self.id) + 13 * hash(tuple(self.snakes)))

	# Return current score of team, which is equal to the sum of snake lengths
	# plus the lengths of their "eaten" lists
	def getScore(self):
		score = 0
		for snake in self.snakes:
			score += snake.length + len(snake.eaten)
		return score


	# Update a member of the team
	def updateSnake(self, snake_id, index):
		self.snakes[snake_id].updateSnake(index)


