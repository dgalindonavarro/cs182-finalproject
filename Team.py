class Team():
	def __init__(self, id):
		self.id = id
		self.snakes = []

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


